# import pygame#引入game模块
# import math
import numpy as np

import men_draw
#
# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化

# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("破壁")#设定窗口的标题
# pygame.mouse.set_visible(False)
# font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量
#
# '''2023年重大更新，引入空间方块占用张量'''
# block_input_tensorx=[0 for i in range(10) ]
# block_input_tensory=[0 for i in range(10) ]
# block_input_tensorz=[0 for i in range(10) ]
# block_input_tensor=[block_input_tensorx,block_input_tensory,block_input_tensorz]
#
#
# '''显示设定'''
e=100#打算做成体素化的游戏，这个就当成单位长度
PI=3.1415926535897932384626
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
# scl=1000#中轴线的长度
# ccd=900#人物与摄像机的距离
# basehigh=250
# x1=1;y1=0;z1=0#初始视角方向
# x0=e;y0=e;z0=2*e;
# BLACK=(0,0,0)
# WHITE=(255,255,255)
# theata=0;fai=0;
#
# '''运动设定'''
# rusht=0
# jumpt=0
# fall=False
# fallt=0
# speed=10
# ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
# g=20
# widelimit=math.atan(mousex0/scl)#视线广角极限
# uplimit=math.atan(mousey0/scl)#视线仰角极限
# couplimit=math.atan(mousey0/(scl**2+mousex0**2)**0.5)#屏幕四角的仰角极限
# cowidelimit=math.atan(mousex0/(scl**2+mousey0**2)**0.5)#屏幕四角的广角极限
# '''空间设定'''
# room=[4000,1000,600]
# d=[[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]]


'''函数集'''
def sign(a):
    if a>0:
        b=1;
    elif a==0:
        b=0;
    else:
        b=-1
    return b

def block_tensor_create(lenth):
    a = []
    lenth = lenth

    for i in range(lenth):
        a.append([])

    for i in range(lenth):
        for j in range(lenth):
            a[i].append([])

    for i in range(lenth):
        for j in range(lenth):
            for z in range(lenth):
                a[i][j].append(0)

    return a

#将原来的二叉树形的顶点坐标存储格式转换为 方便mencreate的格式
def block_no_men_transfer(d, k):
    # norvec=[上，前，左，下，后，右]
    if k==0:
        return [d[0][0][1],d[1][0][1],d[1][1][1],d[0][1][1]]
    elif k==1:
        return [d[1][0][0], d[1][1][0], d[1][1][1], d[1][0][1]]
    elif k==2:
        return [d[1][1][0], d[0][1][0], d[0][1][1], d[1][1][1]]
    elif k==3:
        return [d[1][0][0], d[0][0][0], d[0][1][0], d[1][1][0]]
    elif k==4:
        return [d[0][0][0], d[0][0][1], d[0][1][1], d[0][1][0]]
    elif k==5:
        return [d[1][0][0], d[1][0][1], d[0][0][1], d[0][0][0]]

def tnr_block_judge(block_input_tensor ,pos):
    tnr_block = [0, 0, 0, 0, 0, 0]
    for k in range(6):
        if k == 0:
            if block_input_tensor[pos[0]][pos[1]][pos[2]+1]:
                tnr_block[0] = 1
        if k == 1:
            if block_input_tensor[pos[0]+1][pos[1]][pos[2]]:
                tnr_block[1] = 1
        if k == 2:
            if block_input_tensor[pos[0]][pos[1]+1][pos[2]]:
                tnr_block[2] = 1
        if k == 3:
            if block_input_tensor[pos[0]][pos[1]][pos[2]-1]:
                tnr_block[3] = 1
        if k == 4:
            if block_input_tensor[pos[0]-1][pos[1]][pos[2]]:
                tnr_block[4] = 1
        if k == 5:
            if block_input_tensor[pos[0]][pos[1]-1][pos[2]]:
                tnr_block[5] = 1

    return tnr_block

def blockload(d,pos,mencolor,linecolor,block_input_tensor,screen,x0,y0,z0,x1,y1,z1):

    midpoint=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    #centerpoint=[0.5 * (d[1][0][0][0] + d[0][0][0][0]), 0.5 * (d[0][1][0][1]+d[0][0][0][1]), 0.5 * (d[0][0][0][2] + d[0][0][1][2])]
    #midv=[centerpoint[0]-x0,centerpoint[1]-y0,centerpoint[2]-z0]

    #rayvec=[东方向量，北方向量，天空岛向量]
    rayvec = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for k in range(3):#面向东方：
        rayvec[0][k]=d[1][0][0][k]-d[0][0][0][k]
    for k in range(3):#面向北方：
        rayvec[1][k]=d[0][1][0][k]-d[0][0][0][k]
    for k in range(3):#面向天空（岛）：
        rayvec[2][k]=d[0][0][1][k]-d[0][0][0][k]

    #norvec=[上的方向向量，前的方向向量，左的方向向量，下的方向向量，后的方向向量，右的方向向量]
    #所有的方向向量相对于正方体朝外
    norvec = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # tnr_block相邻有无方块放置

    for k in range(3):
        norvec[k]=men_draw.vecpro(rayvec[k],rayvec[(k+1)%3])

    for k in range(3):
        norvec[k+3]=[-norvec[k][0],-norvec[k][1],-norvec[k][2]]

    ''' 2023年优化：为了减少渲染面的次数，若某一面被其他的方块遮住，那也就跳过，不作渲染.'''
    tnr_block=tnr_block_judge(block_input_tensor,pos)

    #midpoint=[上面中心点的坐标，前面中心点的坐标，左面中心点的坐标，下面中心点的坐标，后面中心点的坐标，右面中心点的坐标]
    midpoint[0]=[0.25*(d[1][0][1][0]+d[0][0][1][0]+d[0][1][1][0]+d[1][1][1][0]),0.25*(d[1][0][1][1]+d[0][0][1][1]+d[0][1][1][1]+d[1][1][1][1]),0.25*(d[1][0][1][2]+d[0][0][1][2]+d[0][1][1][2]+d[1][1][1][2])]
    midpoint[1] = [0.25*(d[1][0][0][0]+d[1][0][1][0]+d[1][1][0][0]+d[1][1][1][0]), 0.25*(d[1][0][0][1]+d[1][0][1][1]+d[1][1][0][1]+d[1][1][1][1]), 0.25*(d[1][0][0][2]+d[1][0][1][2]+d[1][1][0][2]+d[1][1][1][2])]
    midpoint[2] = [0.25 * (d[0][1][0][0] + d[0][1][1][0]+d[1][1][0][0]+d[1][1][1][0]), 0.25 * (d[0][1][0][1] + d[0][1][1][1]+d[1][1][0][1]+d[1][1][1][1]),0.25 * (d[0][1][0][2] + d[0][1][1][2]+d[1][1][0][2]+d[1][1][1][2])]
    midpoint[3] = [0.25*(d[1][0][0][0]+d[0][0][0][0]+d[0][1][0][0]+d[1][1][0][0]),0.25*(d[1][0][0][1]+d[0][0][0][1]+d[0][1][0][1]+d[1][1][0][1]),0.25*(d[1][0][0][2]+d[0][0][0][2]+d[0][1][0][2]+d[1][1][0][2])]
    midpoint[4] = [0.25*(d[0][0][0][0]+d[0][0][1][0]+d[0][1][0][0]+d[0][1][1][0]), 0.25*(d[0][0][0][1]+d[0][0][1][1]+d[0][1][0][1]+d[0][1][1][1]), 0.25*(d[0][0][0][2]+d[0][0][1][2]+d[0][1][0][2]+d[0][1][1][2])]
    midpoint[5] = [0.25 * (d[0][0][0][0] + d[0][0][1][0]+d[1][0][0][0]+d[1][0][1][0]), 0.25 * (d[0][0][0][1] + d[0][0][1][1]+d[1][0][0][1]+d[1][0][1][1]),0.25 * (d[0][0][0][2] + d[0][0][1][2]+d[1][0][0][2]+d[1][0][1][2])]

    #由于正方体的六个面中只能看到三个面，所以要找到某种方法来判断哪三个不可见
    #将摄像机为起点，某一面的中心点作为终点，做向量；如果与该面的法向量(向外)的方向一致(<90°),则认为是不可见的。

    for i in range(6):
        if tnr_block[i]==0  and men_draw.line_draw.angle(norvec[i][0],norvec[i][1],norvec[i][2],midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0)>PI/2 :
        #     ''' 2023年优化：为了减少渲染面的次数，若某一面被其他的方块遮住，那也就跳过，不作渲染.'''
            men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen,x0, y0, z0, x1, y1, z1)
    #
    #     #小优化：由于方块方向规整，判断符号也能反应是否一致，为此避免角度运算
    #
    #
    #     if tnr_block[i]==0 and np.sign(norvec[i][0])*np.sign(midpoint[i][0]-x0)+np.sign(norvec[i][1])*np.sign(midpoint[i][1]-y0)+np.sign(norvec[i][2])*np.sign(midpoint[i][2]-z0)<0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), wallcolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    # x_forward=np.sign(x1)
    # y_forward=np.sign(y1)
    # z_forward=np.sign(z1)
    #
    # for i in range(6):
    #     # 小优化：由于方块方向规整，判断符号也能反应是否一致，为此避免角度运算
    #
    #     if i==0 and z_forward<0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==1 and x_forward<0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==2 and y_forward<0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==3 and z_forward>0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==4 and x_forward>0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==5 and y_forward>0 and tnr_block[i]==0 :
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
def creature_cube_load(d,mencolor,linecolor,screen,x0,y0,z0,x1,y1,z1):
    pass
    # x_forward=np.sign(x1)
    # y_forward=np.sign(y1)
    # z_forward=np.sign(z1)
    #
    # for i in range(6):
    #     # if tnr_block[i]==0  and men_draw.line_draw.angle(norvec[i][0],norvec[i][1],norvec[i][2],midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0)>PI/2 :
    #     #     ''' 2023年优化：为了减少渲染面的次数，若某一面被其他的方块遮住，那也就跳过，不作渲染.'''
    #     #     men_draw.mencreate(block_no_men_transfer(d, i), wallcolor, linecolor, screen,x0, y0, z0, x1, y1, z1)
    #
    #     # 小优化：由于方块方向规整，判断符号也能反应是否一致，为此避免角度运算
    #
    #     if i==0 and z_forward<0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==1 and x_forward<0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==2 and y_forward<0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==3 and z_forward>0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==4 and x_forward>0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    #     if i==5 and y_forward>0:
    #         men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)
    midpoint = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # rayvec=[前方向量，左边向量，头顶向量]
    rayvec = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for k in range(3):  # 面向东方：
        rayvec[0][k] = d[1][0][0][k] - d[0][0][0][k]
    for k in range(3):  # 面向北方：
        rayvec[1][k] = d[0][1][0][k] - d[0][0][0][k]
    for k in range(3):  # 面向天空（岛）：
        rayvec[2][k] = d[0][0][1][k] - d[0][0][0][k]

    # norvec=[上的方向向量，前的方向向量，左的方向向量，下的方向向量，后的方向向量，右的方向向量]
    # 所有的方向向量相对于正方体朝外
    norvec = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # tnr_block相邻有无方块放置

    for k in range(3):
        norvec[k] = men_draw.vecpro(rayvec[k], rayvec[(k + 1) % 3])

    for k in range(3):
        norvec[k + 3] = [-norvec[k][0], -norvec[k][1], -norvec[k][2]]


    # midpoint=[上面中心点的坐标，前面中心点的坐标，左面中心点的坐标，下面中心点的坐标，后面中心点的坐标，右面中心点的坐标]
    midpoint[0] = [0.25 * (d[1][0][1][0] + d[0][0][1][0] + d[0][1][1][0] + d[1][1][1][0]),
                   0.25 * (d[1][0][1][1] + d[0][0][1][1] + d[0][1][1][1] + d[1][1][1][1]),
                   0.25 * (d[1][0][1][2] + d[0][0][1][2] + d[0][1][1][2] + d[1][1][1][2])]
    midpoint[1] = [0.25 * (d[1][0][0][0] + d[1][0][1][0] + d[1][1][0][0] + d[1][1][1][0]),
                   0.25 * (d[1][0][0][1] + d[1][0][1][1] + d[1][1][0][1] + d[1][1][1][1]),
                   0.25 * (d[1][0][0][2] + d[1][0][1][2] + d[1][1][0][2] + d[1][1][1][2])]
    midpoint[2] = [0.25 * (d[0][1][0][0] + d[0][1][1][0] + d[1][1][0][0] + d[1][1][1][0]),
                   0.25 * (d[0][1][0][1] + d[0][1][1][1] + d[1][1][0][1] + d[1][1][1][1]),
                   0.25 * (d[0][1][0][2] + d[0][1][1][2] + d[1][1][0][2] + d[1][1][1][2])]
    midpoint[3] = [0.25 * (d[1][0][0][0] + d[0][0][0][0] + d[0][1][0][0] + d[1][1][0][0]),
                   0.25 * (d[1][0][0][1] + d[0][0][0][1] + d[0][1][0][1] + d[1][1][0][1]),
                   0.25 * (d[1][0][0][2] + d[0][0][0][2] + d[0][1][0][2] + d[1][1][0][2])]
    midpoint[4] = [0.25 * (d[0][0][0][0] + d[0][0][1][0] + d[0][1][0][0] + d[0][1][1][0]),
                   0.25 * (d[0][0][0][1] + d[0][0][1][1] + d[0][1][0][1] + d[0][1][1][1]),
                   0.25 * (d[0][0][0][2] + d[0][0][1][2] + d[0][1][0][2] + d[0][1][1][2])]
    midpoint[5] = [0.25 * (d[0][0][0][0] + d[0][0][1][0] + d[1][0][0][0] + d[1][0][1][0]),
                   0.25 * (d[0][0][0][1] + d[0][0][1][1] + d[1][0][0][1] + d[1][0][1][1]),
                   0.25 * (d[0][0][0][2] + d[0][0][1][2] + d[1][0][0][2] + d[1][0][1][2])]

    # 由于正方体的六个面中只能看到三个面，所以要找到某种方法来判断哪三个不可见
    # 将摄像机为起点，某一面的中心点作为终点，做向量；如果与该面的法向量(向外)的方向一致(<90°),则认为是不可见的。

    for i in range(6):
        # if tnr_block[i]==0  and men_draw.line_draw.angle(norvec[i][0],norvec[i][1],norvec[i][2],midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0)>PI/2 :
        #     ''' 2023年优化：为了减少渲染面的次数，若某一面被其他的方块遮住，那也就跳过，不作渲染.'''
        #     men_draw.mencreate(block_no_men_transfer(d, i), wallcolor, linecolor, screen,x0, y0, z0, x1, y1, z1)

        # 小优化：由于方块方向规整，判断符号也能反应是否一致，为此避免角度运算

        if  (norvec[i][0]) * (midpoint[i][0] - x0) + (norvec[i][1]) * (
                midpoint[i][1] - y0) + (norvec[i][2]) * (midpoint[i][2] - z0) < 0:
            men_draw.mencreate(block_no_men_transfer(d, i), mencolor, linecolor, screen, x0, y0, z0, x1, y1, z1)


#blockinput调用格式([5,2,1],[1,1,1],(255,0,0),(0,0,255),block_input_tensor,x0,y0,z0,x1,y1,z1)
#block_input_tensor,用来辅助不显示被遮住的面，提升渲染效率
def blockinput(pos,volume,mencolor,linecolor,block_input_tensor,screen,x0,y0,z0,x1,y1,z1):
    blockload(men_draw.blockcreate(volume[0]*e,volume[1]*e,volume[2]*e, [pos[0]*e,pos[1]*e,pos[2]*e], 1, 0, 0),pos,mencolor, linecolor,block_input_tensor,screen,x0,y0,z0,x1,y1,z1)


# def eyeopen():
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#         men_draw.floorload(men_draw.floorcreate(10*e, 10*e,10, 10, 0, 0, 0), (255, 255, 255),screen,x0,y0,z0,x1,y1,z1)
#
#         block_input_tensor[0][5]=1;block_input_tensor[1][2]=1;block_input_tensor[2][1]=1
#
#         #block_input_tensor[1][1]=1;
#         block_input_tensor[0][6]=1;
#
#         blockinput([5,2,1],[1,1,1],(255,0,0),(0,0,255),block_input_tensor,x0,y0,z0,x1,y1,z1)
#         blockinput([6, 2, 1], [1, 1, 1], (0, 0, 255), (0, 0, 255), block_input_tensor, x0, y0, z0, x1, y1, z1)
#         blockinput([5, 1, 1], [1, 1, 1], (0, 255, 0), (0, 0, 255), block_input_tensor, x0, y0, z0, x1, y1, z1)
#


# gamegoing=False#决定整个进程是否会继续的变量
#
# while gamegoing:#在游戏进行当中
#
#     mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
#     mousey = pygame.mouse.get_pos()[1]
#     theata = -(mousex - mousex0) / (mousex0 / 270) * PI / 180
#     fai = -(mousey - mousey0) / (mousey0 / 89) * PI / 180
#     x1 = math.cos(fai) * math.cos(theata)
#     y1 = math.cos(fai) * math.sin(theata)
#     z1 = math.sin(fai)
#
#
#     for event in pygame.event.get():#遍历所有捕捉到的事件
#         if event.type==pygame.QUIT:#按X按钮退出
#             gamegoing=False
#         if event.type==pygame.KEYDOWN:#按下按键
#             if event.key==pygame.K_w:#表示按下了w键
#                 ahead_kd=True
#             elif event.key==pygame.K_s:
#                 back_kd=True
#             elif event.key==pygame.K_a:
#                 left_kd=True
#             elif event.key == pygame.K_d:
#                 right_kd=True
#             elif event.key==pygame.K_SPACE:
#                 up_Kd=True
#             elif event.key==pygame.K_x:
#                 down_Kd=True
#             elif event.key==pygame.K_n:
#                 pygame.mouse.set_visible(True)
#             elif event.key==pygame.K_r:#视角定
#                 pygame.mouse.set_pos(mousex0,mousey0)
#             # elif event.key==pygame.K_p:#瞬间传送
#             #     x0=1891
#             #     y0=764
#             #     z0=300
#             #
#             # elif event.key==pygame.K_q:
#             #     [newx1, newy1, newz1] = men_draw.postrans(0, 0, 0, scl, 1 * mousex0, 1 * mousey0, x1, y1, z1)
#             #     r = men_draw.line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#             #     x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             # elif event.key==pygame.K_e:
#             #     [newx1, newy1, newz1] = men_draw.postrans(0, 0, 0, scl, -1 * mousex0, 1 * mousey0, x1, y1, z1)
#             #     r = men_draw.line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#             #     x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             # elif event.key==pygame.K_z:
#             #     [newx1, newy1, newz1] = men_draw.postrans(0, 0, 0, scl, 1 * mousex0, -1 * mousey0, x1, y1, z1)
#             #     r = men_draw.line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#             #     x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             # elif event.key==pygame.K_c:
#             #     [newx1, newy1, newz1] = men_draw.postrans(0, 0, 0, scl, -1 * mousex0, -1 * mousey0, x1, y1, z1)
#             #     r = men_draw.line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#             #     x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             elif event.key==pygame.K_ESCAPE:
#                 gamegoing=False
#         if event.type==pygame.KEYUP:
#             if event.key==pygame.K_w:#表示松开了w键
#                 ahead_kd=False
#             elif event.key==pygame.K_s:
#                 back_kd=False
#             elif event.key==pygame.K_a:
#                 left_kd=False
#             elif event.key == pygame.K_d:
#                 right_kd=False
#             elif event.key==pygame.K_SPACE:
#                 up_Kd=False
#             elif event.key==pygame.K_x:
#                 down_Kd=False
#             elif event.key== pygame.K_n:
#                 pygame.mouse.set_visible(False)
#         if  event.type==pygame.MOUSEBUTTONDOWN:
#             if speed==1:
#                 speed=10
#             else:
#                 speed=1
#         if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:
#             eyeopen()
#
#     r=men_draw.line_draw.sqr(x1**2+y1**2)
#     if ahead_kd:
#         x0 += x1 * speed/r;
#         y0 += y1 * speed/r;
#         eyeopen()
#     if back_kd:
#         x0 -= x1 * speed/r;
#         y0 -= y1 * speed/r
#         eyeopen()
#     if left_kd:
#         y0 += x1 * speed/r;
#         x0 -= y1 * speed/r
#         eyeopen()
#     if right_kd:
#         y0 -= speed * x1/r;
#         x0 += y1 * speed/r
#         eyeopen()
#     if up_Kd:
#         z0+=speed
#         eyeopen()
#     if down_Kd:
#         z0-=speed
#         eyeopen()
#
#
#     # 绘制十字架
#     pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
#     pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)
#
#     pygame.display.update()#更新显示的画面
#     timer.tick(60)#表示每秒播放60帧

# pygame.quit()#及时退出game模块好习惯