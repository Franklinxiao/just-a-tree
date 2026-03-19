# import copy
# from typing import List
import pygame#引入game模块
import math
import block_create
import image_load

pygame.init()#game模块的初始化
pygame.mixer.init()#game播放声音部分的初始化

screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
pygame.display.set_caption("破壁")#设定窗口的标题
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
timer=pygame.time.Clock()#创建time变量
image = pygame.image.load("水印.jpg").convert()

'''2023年重大更新，引入空间方块占用张量'''
block_input_tensor=block_create.block_tensor_create(10)



'''显示设定'''
e=100#打算做成体素化的游戏，这个就当成单位长度
PI=3.1415926535897932384626
mousex0=0.5*screen.get_width()
mousey0=0.5*screen.get_height()
scl=1000#中轴线的长度
ccd=900#人物与摄像机的距离
basehigh=250
x1=1;y1=0;z1=0
x0=1*e;y0=1*e;z0=1.7*e;
theata=0;fai=0;
'''颜色设定'''

BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
WHITE_PINK=(221,164,226)
PINK=(232,139,247)
SKYBLUE=(0,255,255)
WHITE=(255,255,255)
BROWN=(120,80,0)


'''运动设定'''
rusht=0
jumpt=0
fall=False
fallt=0
speed=10
ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
g=20
widelimit=math.atan(mousex0/scl)#视线广角极限
uplimit=math.atan(mousey0/scl)#视线仰角极限
couplimit=math.atan(mousey0/(scl**2+mousex0**2)**0.5)#屏幕四角的仰角极限
cowidelimit=math.atan(mousex0/(scl**2+mousey0**2)**0.5)#屏幕四角的广角极限
'''空间设定'''
room=[4000,1000,600]
d=[[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]]


'''函数集'''

#更具具体描述，填充方块占用空间
#blocklst格式是([[15,15,0],[1,1,3],BROWN,BLACK,e])([放置位置，放置大小,方块颜色，线条颜色，单位长])
def block_occupy_cal(blocklst):

    #初始化
    block_input_tensor=block_create.block_tensor_create(11)

    #遍历
    for i in blocklst:
        startx=i[0][0]
        starty=i[0][1]
        startz=i[0][2]

        fillx=i[1][0]
        filly=i[1][1]
        fillz=i[1][2]


        for dx in range (fillx ):
            for dy in range(filly):
                for dz in range(fillz):
                    block_input_tensor[startx+dx][starty+dy][startz+dz]=1
                    #print(block_input_tensor)

    #block_input_tensor = [block_input_tensorx, block_input_tensory, block_input_tensorz]
    return block_input_tensor

# 先对blocklst内涉及的方块数量进行拆分。
def block_lst_seg(blocklst):
    divid_lst = []
    for i in blocklst:
        startx = i[0][0]
        starty = i[0][1]
        startz = i[0][2]

        fillx = i[1][0]
        filly = i[1][1]
        fillz = i[1][2]

        for dx in range(fillx):
            for dy in range(filly):
                for dz in range(fillz):
                    divid_lst.append([[startx + dx, starty + dy, startz + dz], i[2], i[3]])
    return divid_lst

#在所有方块加载之前根据与摄像机的距离进行排序,距离远的先渲染,近的最后渲染,
#本来就在视线后面的直接提出列表，不渲染。
def painter_sort(divid_lst,x0,y0,z0,x1,y1,z1,e):
    x0=int(x0)
    y0 = int(y0)
    z0 = int(z0)

    load_block_lst=[i for i in divid_lst]

    #以下循环剔除掉在摄像机后面的方块列表
    for i in divid_lst:

        # divid_lst格式是[[startx + dx, starty + dy, startz + dz], (X,X,X), (X,X,X)]
        if  block_create.men_draw.line_draw.angle(
            i[0][0]*e-x0,i[0][1]*e-y0,i[0][1]*e-z0,
            x1,y1,z1
        )>PI/2:
            load_block_lst.remove(i)

    for i in load_block_lst:
        i.append(block_create.men_draw.line_draw.distance(
            i[0][0]*e,i[0][1]*e,i[0][2]*e,
            x0,y0,z0
        ))

    load_block_lst.sort(key=lambda ele: ele[-1],reverse=True)

    return load_block_lst

#其余的狠狠的渲染
def multi_block_load(load_block_lst,block_input_tensor,x0,y0,z0,x1,y1,z1):

    # load_block_lst格式是[[X,X,X], (X,X,X), (X,X,X),distance]
    for i in load_block_lst:
        block_create.blockinput(i[0],[1,1,1],i[1],i[2],block_input_tensor,screen,x0,y0,z0,x1,y1,z1)

def shows(draw_string,pos):#显示操作提示语句
    text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置

def eyeopen():
    if not(pygame.mouse.get_visible()):
        screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影

        #生成地板参考格子
        block_create.men_draw.floorload(block_create.men_draw.floorcreate(11*e, 11*e, 11, 11, 0, 0, 0), GREEN,screen,x0,y0,z0,x1,y1,z1)

        blocklst=[]
        blocklst.append([[3,3,0],[1,1,1],BLACK,WHITE])
        blocklst.append([[5,5,0],[1,1,3],BROWN,BLACK])
        blocklst.append([[3,3,3],[5,5,2],GREEN,BLACK])
        blocklst.append([[4,4 , 5], [3, 3, 1],GREEN,BLACK])

        divid_lst=block_lst_seg(blocklst)
        multi_block_load(painter_sort(divid_lst,x0,y0,z0,x1,y1,z1,e),block_occupy_cal(blocklst),x0,y0,z0,x1,y1,z1)
        #print(block_occupy_cal(blocklst))
        # image_load.img_load(image,[[3*e,3*e,e],[2*e,3*e,e],[2*e,3*e,0],[3*e,3*e,0]],[x1,y1,z1],[x0,y0,z0],screen)
        # image_load.img_load(image, [[3 * e, 2 * e, e], [3 * e, 3 * e, e], [3 * e, 3 * e, 0], [3 * e, 2 * e, 0]],
        #                     [x1, y1, z1], [x0, y0, z0], screen)
        image_load.img_load(image, [[4 * e, 4 * e, e-5], [3 * e+5, 4 * e, e-5], [3 * e, 4 * e, 0], [4 * e, 4 * e, 0]],[x1, y1, z1], [x0, y0, z0], screen)
        # shows(str([x0,y0,z0]),(10,30*(+1)+10))
        # shows(str([x1,y1,z1]),(10,30*(+2)+10))

gamegoing=True#决定整个进程是否会继续的变量

while gamegoing:#在游戏进行当中

    mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
    mousey = pygame.mouse.get_pos()[1]
    theata = -(mousex - mousex0) / (mousex0 / 270) * PI / 180
    fai = -(mousey - mousey0) / (mousey0 / 89) * PI / 180
    x1 = math.cos(fai) * math.cos(theata)
    y1 = math.cos(fai) * math.sin(theata)
    z1 = math.sin(fai)

    for event in pygame.event.get():#遍历所有捕捉到的事件
        if event.type==pygame.QUIT:#按X按钮退出
            gamegoing=False
        if event.type==pygame.KEYDOWN:#按下按键
            if event.key==pygame.K_w:#表示按下了w键
                ahead_kd=True
            elif event.key==pygame.K_s:
                back_kd=True
            elif event.key==pygame.K_a:
                left_kd=True
            elif event.key == pygame.K_d:
                right_kd=True
            elif event.key==pygame.K_SPACE:
                up_Kd=True
            elif event.key==pygame.K_x:
                down_Kd=True
            elif event.key==pygame.K_n:
                pygame.mouse.set_visible(True)
            elif event.key==pygame.K_r:#视角定
                pygame.mouse.set_pos(mousex0,mousey0)
            elif event.key==pygame.K_p:#瞬间传送
                x0 = 247.866
                y0 = -70
                z0 = 160
            elif event.key==pygame.K_ESCAPE:
                gamegoing=False


        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:#表示松开了w键
                ahead_kd=False
            elif event.key==pygame.K_s:
                back_kd=False
            elif event.key==pygame.K_a:
                left_kd=False
            elif event.key == pygame.K_d:
                right_kd=False
            elif event.key==pygame.K_SPACE:
                up_Kd=False
            elif event.key==pygame.K_x:
                down_Kd=False
            elif event.key== pygame.K_n:
                pygame.mouse.set_visible(False)
        if  event.type==pygame.MOUSEBUTTONDOWN:
            if speed==1:
                speed=10
            else:
                speed=1
        if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:
            eyeopen()

    r=block_create.men_draw.line_draw.sqr(x1**2+y1**2)
    if ahead_kd:
        x0 += x1 * speed/r;
        y0 += y1 * speed/r;
        eyeopen()
    if back_kd:
        x0 -= x1 * speed/r;
        y0 -= y1 * speed/r
        eyeopen()
    if left_kd:
        y0 += x1 * speed/r;
        x0 -= y1 * speed/r
        eyeopen()
    if right_kd:
        y0 -= speed * x1/r;
        x0 += y1 * speed/r
        eyeopen()
    if up_Kd:
        z0+=speed
        eyeopen()
    if down_Kd:
        z0-=speed
        eyeopen()

    # 绘制十字架
    pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
    pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)

    pygame.display.update()#更新显示的画面
    timer.tick(24)#表示每秒播放60帧

pygame.quit()#及时退出game模块好习惯
