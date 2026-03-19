# import copy
# from typing import List
# import pygame#引入game模块
# import math


#如果有警告显示没有使用painter_algorithm,请无视它。
import painter_algorithm


#
# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化
#
# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("破壁")#设定窗口的标题
# pygame.mouse.set_visible(False)
# font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量

'''2023年重大更新，引入空间方块占用张量'''

# block_input_tensor=painter_algorithm.block_create.block_tensor_create(10)
# shot_block=[]


'''显示设定'''
e=100#打算做成体素化的游戏，这个就当成单位长度
PI=3.1415926535897932384626
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
# boundaryx=25
# boundaryy=25
# scl=1000#中轴线的长度
# ccd=900#人物与摄像机的距离
# basehigh=250
# x1=1;y1=0;z1=0
# x0=1*e;y0=1*e;z0=4.5*e;
# theata=0;fai=0;
# world_lenth=30
'''颜色设定'''

# BLACK=(0,0,0)
# RED=(255,0,0)
# GREEN=(0,255,0)
# BLUE=(0,0,255)
# YELLOW=(255,255,0)
# WHITE_PINK=(221,164,226)
# PINK=(232,139,247)
# SKYBLUE=(0,255,255)
# WHITE=(255,255,255)
# BROWN=(120,80,0)


'''运动设定'''
# speed=11
# rusht=0
# jumpt=0
# fall=False
# fallt=0
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

def shot_to_detect(block_input_tensor,x0,y0,z0,x1,y1,z1,e,world_lenth):

    pause_pos=[x0,y0,z0]
    forward=[x1,y1,z1]
    previous_pos=[]

    startx=int(x0/e);    starty=int(y0/e);    startz=int(z0/e)
    # print('X0,Y0,Z0',[x0,y0,z0])
    forward_x=sign(x1);    forward_y = sign(y1);    forward_z = sign(z1)

    step_limit=13
    step=0

    while   block_input_tensor[startx][starty][startz]==0  and step<step_limit  :

        delta_lst=[abs((startx+forward_x*((sign(x1)+1)/2))*e-pause_pos[0]),abs((starty+forward_y*((sign(y1)+1)/2))*e-pause_pos[1]),abs((startz+forward_z*((sign(z1)+1)/2))*e-pause_pos[2])]

        adequate_step=[0 for i in range(len(pause_pos))]
        for i in range(len(pause_pos)):

            if forward[i]>0:
                adequate_step[i] = abs(delta_lst[i] / forward[i])
            elif forward[i]<0:
                adequate_step[i]=abs(delta_lst[i]/forward[i])
            else:
                adequate_step[i]=pow(2,32)

        closest=adequate_step.index(min(adequate_step))

        Enough_step=min(adequate_step)

        # print('closet:',closest)
        for i in range(len(pause_pos)):
            if i== closest:
                pause_pos[i]=pause_pos[i]+(delta_lst[closest]+1)*sign(forward[closest])
            else:
                pause_pos[i]=pause_pos[i]+Enough_step*forward[i]

        # print('pause_pos',pause_pos)

        previous_pos=[startx,starty,startz]

        startx = int(pause_pos[0] / e);
        starty = int(pause_pos[1] / e);
        startz = int(pause_pos[2] / e)

        if  startx<world_lenth and starty<world_lenth and startz<world_lenth:
            step += 1
        else:
            return 0

        # print(startx,starty,startz,block_input_tensor[startx][starty][startz])
        # print('################')


    if step==step_limit :
        return 0
    if step==1:#再靠近一点就会爆炸
        previous_pos=0

    return [ [startx,starty,startz],previous_pos]

def delete_block(divid_lst,targitpos):

    for i in range(len(divid_lst)):
        if divid_lst[i].center_pos==targitpos:
                divid_lst.pop(i)
    return divid_lst


def add_block(divid_lst,targitpos,blockcolor,linecolor,block_id,hardness):
    if block_id==1:
        divid_lst.append(painter_algorithm.Block(targitpos,blockcolor,linecolor,True,hardness))
    elif block_id==2:
        #divid_lst.append(Men_series([16, 13, 1], [1, 1, 2], [16, 13, 1], GRASS([16, 13, 1], [1, 1, 2], e), True, 1))
        pass
    return divid_lst


# def shows(draw_string,pos,screen):#显示操作提示语句
#     text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
#
# def C_shows(draw_string,pos,screen):#显示操作提示语句
#     game_font = pygame.font.SysFont("SimHei", 30)
#     text = game_font.render(draw_string ,False, (255, 255, 0))
#     #text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置


def wall_preshape(div_lst, worldlenth):

    air_wall=painter_algorithm.block_create.block_tensor_create(worldlenth)
    for i in  range(worldlenth):
        for j in range(worldlenth):
            for k in range(worldlenth):
                if i==0 or j==0 or k==0 or i==worldlenth-1 or j==worldlenth-1 or k==worldlenth-1:
                    air_wall[i][j][k]=1

    for i in div_lst:
        # print(i)
        if i.id==1 and i.weather_crush==True:
            air_wall[i.pos[0]][i.pos[1]][i.pos[2]] = 1

        elif i.id==2 and i.weather_crush==True:
            for dx in range(i.occupy_space[0]):
                for dy in range(i.occupy_space[1]):
                    for dz in range(i.occupy_space[2]):
                        air_wall[i.stp[0] + dx][i.stp[1] + dy][i.stp[2] + dz] = 1

    return air_wall


def wall_detect(air_wall_tensor,x0,y0,z0,x1,y1,speed):
    pos_x = int(x0  / e)
    pos_y = int(y0  / e)
    pos_z = int(z0 / e)

    target_x=int((x0+x1*speed)/e)
    target_y = int((y0+y1*speed) / e)
    target_z = int(z0 / e)

    tarward_x=sign(x1)
    tarward_y=sign(y1)


    if air_wall_tensor[pos_x][pos_y][pos_z]:
        print('you are stucking!',[pos_x,pos_y,pos_z])
        return 2


    if abs(target_x-pos_x)+abs(target_y-pos_y)+abs(target_z-pos_z)<=1:#如果经过微小瞬移后下一个地点就在相邻方块，或者自身所在的方块
        if  not air_wall_tensor[target_x][target_y][target_z]:
            return 0
        else:
            return [target_x,target_y,target_z]


    else:#如果是对角
        if air_wall_tensor[pos_x][pos_y+tarward_y][pos_z] and not air_wall_tensor[pos_x+tarward_x][pos_y][pos_z] :#如果是y相邻方向有空气墙，x方向没有
            return [pos_x, pos_y+tarward_y, pos_z]

        elif not air_wall_tensor[pos_x][pos_y+tarward_y][pos_z] and  air_wall_tensor[pos_x+tarward_x][pos_y][pos_z]:#如果是x相邻方向有空气墙，y方向没有
            return [pos_x+tarward_x,pos_y,pos_z]

        elif air_wall_tensor[target_x][target_y][target_z]:
            #如果是真的对桌角......
            #print(2)
            return 2
        else:
            #没什么情况了,返回0表示可以正常行走。
            return 0


def horizontal_speed_decompositon(shot_block_pos,x0,y0,x1,y1):
    toward=[sign(x1),sign(y1)]
    pos_x=int(x0/e)
    pos_y=int(y0/e)
    if pos_x+toward[0]==shot_block_pos[0]:
        return [0,y1]
    elif pos_y+toward[1]==shot_block_pos[1]:
        return [x1,0]
    else:
        return [0,0]




# def block_preload():
#     blocklst = []
#     blocklst.append([[1, 1, 0], [10, 10, 1], GREEN, WHITE])
#     blocklst.append([[1,0,0],[10,1,1],RED,WHITE])
#     blocklst.append([[0, 1, 0], [1, 10, 1],BLUE, WHITE])
#     blocklst.append([[0, 0, 0], [1, 1, 1], YELLOW, WHITE])
#     # blocklst.append([[5,5,1],[1,1,3],BROWN,BLACK])
#     blocklst.append([[3,3,1],[5,5,2],SKYBLUE,BLACK])
#     blocklst.append([[4,4,3], [3, 3, 1],SKYBLUE,BLACK])
#
#     divid_lst = painter_algorithm.block_lst_seg(blocklst)
#     return divid_lst
#

#
# def eyeopen():
#
#     global shot_block
#
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#
#         #生成地板参考格子
#         painter_algorithm.block_create.men_draw.floorload(painter_algorithm.block_create.men_draw.floorcreate(11*e, 11*e, 11, 11, 0, 0, 0), GREEN,screen,x0,y0,z0,x1,y1,z1)
#
#         painter_algorithm.multi_block_load(screen,painter_algorithm.painter_sort(divid_lst,x0,y0,z0,x1,y1,z1,e),block_occupy_tensor,x0,y0,z0,x1,y1,z1)
#         shot_block=shot_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e)
#         #print(block_occupy_cal(blocklst))
#
#         shows('xyz:'+str([int(1000*x0)/1000,int(1000*y0)/1000,int(1000*z0)/1000]),(10,30*1+10))
#         shows('eyesight'+str([int(1000*x1)/1000,int(1000*y1)/1000,int(1000*z1)/1000]),(10,30*2+10))
#         shows('xyz'+str([int(x0/e),int(y0/e),int(z0/e)]),(10,30*3+10))
#         shows('block'+str(shot_block),(10,30*4+10))
#         shows('speed'+str(speed),(10,30*6+10))
#         if shot_block!=0:
#              shows('ocp:'+str(block_occupy_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]])+'  wall'+str(air_wall_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]]),(10,30*5+10),)
#         shows('peng'+str(collison_block),(10,30*7+10))

# divid_lst=block_preload()
# block_occupy_tensor=painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
# air_wall_tensor=painter_algorithm.block_create.block_tensor_create(world_lenth)
# air_wall_tensor=wall_preshape(air_wall_tensor, block_occupy_tensor, world_lenth)
# collison_block=0


# gamegoing=True#决定整个进程是否会继续的变量
# while gamegoing:#在游戏进行当中
#
#     mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
#     mousey = pygame.mouse.get_pos()[1]
#     theata = -(mousex - mousex0) / (mousex0 / 180) * PI / 180
#     fai = -(mousey - mousey0) / (mousey0 / 89) * PI / 180
#     x1 = math.cos(fai) * math.cos(theata)
#     if x1==0:
#         x1+=0.0001
#     y1 = math.cos(fai) * math.sin(theata)
#     if y1==0:
#         y1+=0.0001
#
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
#             elif event.key==pygame.K_n:#呼出鼠标
#                 pygame.mouse.set_visible(True)
#             elif event.key==pygame.K_r:#复原场景
#                 divid_lst=block_preload()
#                 block_occupy_tensor=painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                 eyeopen()
#             elif event.key==pygame.K_p:#瞬间传送
#                 x0 = 130
#                 y0 = 130
#                 z0 = 270
#             elif event.key == pygame.K_e:  # 凝聚视线
#                 x1=1;y1=0;z1=0;
#             elif event.key==pygame.K_q:
#                 x1=0;y1=1;z1=0;
#             elif event.key==pygame.K_z:
#                 if speed <= 19:
#                     speed = speed + 1
#             elif event.key==pygame.K_c:
#                 if speed >= 2:
#                     speed = speed - 1
#             elif event.key==pygame.K_ESCAPE:
#                 gamegoing=False
#
#
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
#             elif event.key== pygame.K_n:#呼出鼠标
#                 pygame.mouse.set_visible(False)
#
#         if event.type == pygame.MOUSEBUTTONDOWN:#鼠标click事件
#             if event.button == 1:
#                 #shot_block=shot_detect(block_occupy_tensor,x0,y0,z0,x1,y1,z1,e)
#                 if shot_block!=0:
#                     divid_lst=delete_block( divid_lst ,shot_block[0])
#                     block_occupy_tensor = painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                     air_wall_tensor=wall_preshape(air_wall_tensor, block_occupy_tensor, world_lenth)
#                     eyeopen()
#             elif event.button == 2:
#                 pass#print("middle mouse button")
#             elif event.button == 3:
#                 #shot_block = shot_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e)
#                 if shot_block!=0 and shot_block[1]!=0:
#                     divid_lst=add_block(divid_lst,shot_block[1],PINK,YELLOW)
#                     block_occupy_tensor = painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                     air_wall_tensor = wall_preshape(air_wall_tensor, block_occupy_tensor, world_lenth)
#                     eyeopen()
#             elif event.button == 4:
#                 if speed<=19:
#                     speed=speed+1
#             elif event.button == 5:
#                 if speed>=2:
#                     speed=speed-1
#
#
#         if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:
#
#             if mousex<boundaryx:#防止鼠标跑出边界
#                 pygame.mouse.set_pos(2*mousex0-boundaryx,mousey)
#             elif mousex>2*mousex0-boundaryx:
#                 pygame.mouse.set_pos(boundaryx,mousey)
#             if mousey<boundaryy:
#                 pygame.mouse.set_pos(mousex, boundaryy)
#             elif mousey > 2 * mousey0 -boundaryy:
#                 pygame.mouse.set_pos(mousex0, 2*mousey0-boundaryy)
#             eyeopen()
#
#     '''在运动的过程中'''
#     r=painter_algorithm.block_create.men_draw.line_draw.sqr(x1**2+y1**2)
#     if ahead_kd:
#         collison_block=wall_detect(air_wall_tensor, x0,y0,x1,y1,speed/r)
#
#         if  collison_block==0:
#             x0 += x1 * speed/r;
#             y0 += y1 * speed/r;
#             eyeopen()
#             #print(x0,y0)
#         elif  collison_block!=2:  #得到空气墙方块之后对速度进行向量切分
#
#             vestigial_speed=horizontal_speed_decompositon(collison_block, x0, y0, x1, y1)
#
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#
#     if back_kd:
#         collison_block = wall_detect(air_wall_tensor, x0,y0,-x1,-y1,speed/r)
#         if collison_block==0:
#             x0 -= x1 * speed/r;
#             y0 -= y1 * speed/r
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=horizontal_speed_decompositon(collison_block, x0, y0, -x1, -y1)
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#
#     if left_kd:
#         collison_block = wall_detect(air_wall_tensor, x0, y0, -y1, x1,speed/r)
#         if  collison_block==0:
#             x0 -= y1 * speed/r
#             y0 += x1 * speed/r;
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=horizontal_speed_decompositon(collison_block, x0, y0, -y1, x1)
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#     if right_kd:
#         collison_block = wall_detect(air_wall_tensor,  x0, y0, y1, -x1,speed/r)
#         if collison_block==0:
#             x0 += y1 * speed/r
#             y0 -= speed * x1/r;
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=horizontal_speed_decompositon(collison_block, x0, y0, y1, -x1)
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#     if up_Kd:
#         if air_wall_tensor[int(x0/e)] [int(y0/e)] [int((z0+speed)/e)]==0:
#             z0+=speed
#             eyeopen()
#     if down_Kd:
#         if air_wall_tensor[int(x0/e)] [int(y0/e)] [int((z0-speed)/e)]==0:
#             z0-=speed
#             eyeopen()
#
#     # 绘制十字架
#     pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
#     pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)
#
#     pygame.display.update()#更新显示的画面
#     timer.tick(60)#表示每秒播放60帧
#
# pygame.quit()#及时退出game模块好习惯
