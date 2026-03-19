# import copy
# from typing import List
# import pygame#引入game模块
# import math
# import shot_detect
#
# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化
#
# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("破壁")#设定窗口的标题
# pygame.mouse.set_visible(False)
# font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量
#
# '''2023年重大更新，引入空间方块占用张量'''
#
# block_input_tensor=shot_detect.painter_algorithm.block_create.block_tensor_create(10)
# shot_block=[]
#
#
# '''显示设定'''
# e=100#打算做成体素化的游戏，这个就当成单位长度
# PI=3.1415926535897932384626
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
# boundaryx=25
# boundaryy=25
# scl=1000#中轴线的长度
# # ccd=900#人物与摄像机的距离
# # basehigh=250
# x1=1;y1=0;z1=0
# x0=1*e;y0=1*e;z0=4.5*e;
# theata=0;fai=0;
# world_lenth=20
# '''颜色设定'''
#
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
WHITE_PINK=(221,164,226)
PINK=(232,139,247)
Diamond_Blue=(0, 255, 255)
WHITE=(255,255,255)
BROWN=(120,80,0)
GRAY=(128,128,128)
DEEP_GREEN=(40,182,29)
#
#
# '''运动设定'''
# rusht=0
# jumpt=0
# fall=False
# fallt=0
# speed=11
# ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
# g=20
# widelimit=math.atan(mousex0/scl)#视线广角极限
# uplimit=math.atan(mousey0/scl)#视线仰角极限
# couplimit=math.atan(mousey0/(scl**2+mousex0**2)**0.5)#屏幕四角的仰角极限
# cowidelimit=math.atan(mousex0/(scl**2+mousey0**2)**0.5)#屏幕四角的广角极限
#


'''文件间传递的函数集'''

def GRASS(startpos,occupy_space,e):

    # 归一化的比例,以100为单位：
    interlst=[
        [ [ [1,1,1] ,[49,49,1]  ,[25,25,98]   ]  ,DEEP_GREEN,(0,0,0)],
        [ [ [99,1,1] ,[51,49,1]  ,[75,25,98]   ]  ,DEEP_GREEN,(0,0,0)],
        [[[99, 99, 1], [51, 51, 1], [75, 75, 98]], DEEP_GREEN, (0, 0, 0)],
        [[[1, 99, 1], [49, 51, 1], [25, 75, 98]], DEEP_GREEN, (0, 0, 0)]
    ]

    for men in interlst:
        for point in men[0]:
            for point_pos in range( len(point)):
                point[point_pos]=int(startpos[point_pos]*e
                                      +point[point_pos]/100*e*occupy_space[point_pos])

    return interlst


#
#
# '''临场调试函数集'''
#
# def shows(draw_string,pos):#显示操作提示语句
#     text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
#
# def C_shows(draw_string,pos,screen):#显示操作提示语句
#     game_font = pygame.font.SysFont("SimHei", 30)
#     text = game_font.render(draw_string ,False, (255, 255, 0))
#     #text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
#
# def occupy_block_test_print(xrange,yrange,zrange):
#     print('#####occupy#######')
#     for x in xrange:
#         for y in yrange:
#             for z in zrange:
#                 print(str([x,y,z])+str(block_occupy_tensor[x][y][z]))
#     print('#####occupy#######')
# def intransparent_test_print(xrange,yrange,zrange):
#     print('#####intransparent#######')
#     for x in xrange:
#         for y in yrange:
#             for z in zrange:
#                 print(str([x,y,z])+str(block_intransparent_tenser[x][y][z]))
#     print('############')
#
# def airwall_test_print(xrange,yrange,zrange):
#     print('#####airwall#######')
#     for x in xrange:
#         for y in yrange:
#             for z in zrange:
#                 print(str([x,y,z])+str(air_wall_tensor[x][y][z]))
#     print('############')
#
# def distance_print(lst):
#     print('############')
#     for i in lst:
#         print(i.distance)
#     print('##########')
#
# def angle_print(lst):
#     print('############')
#     for i in lst:
#         print(
#             shot_detect.painter_algorithm.block_create.men_draw.line_draw.angle(x1,y1,z1,(i.pos[0]+0.5)*e-x0,(i.pos[1]+0.5)*e-y0,(i.pos[2]+0.5)*e-z0)
#             *180/PI
#         )
#     print('##########')
#

'''类集合'''
class Block_series:
    id=11
    startpos=[0,0,0]
    occupy_space=[0,0,0]
    men_color=(0,0,0)
    line_color=(0,0,0)
    weather_crush=False
    distance=0
    hardness=-1

    def __init__(self,startpos,occupy_space,wallcolor,linecolor,weather_crush,hardness):
        self.startpos=startpos
        self.occupy_space=occupy_space
        self.men_color=wallcolor
        self.line_color=linecolor
        self.weather_crush=weather_crush
        self.hardness=hardness


class Men_series:
    id=2
    startpos=[0,0,0]
    occupy_space=[0,0,0]
    pos=[0,0,0]
    mens_list=[]
    weather_crush=0
    distance=0
    hardness=-1

    def __init__(self,startpos,occupy_space, pos ,menlst,weather_crush,hardness):
        self.startpos=startpos
        self.occupy_space=occupy_space
        self.mens_list=menlst
        self.weather_crush=weather_crush
        self.hardness=hardness
        self.pos=pos


def hito_model_help_build(jiow,jiol,jioh,jiod,bodyl,bodyw,bodyh,arml,armw,armh,headl,headw,headh):

    finallst=[]

    '''生成右腿'''
    cube_lst=[]
    cube_lst.append([50,50-0.5*jiod,0.5*jioh])
    cube_lst.append([jiow,jiol,jioh])
    finallst.append([cube_lst, GRAY, BLACK,'right leg'])

    '''生成左腿'''
    cube_lst = []
    cube_lst.append([50, 50 + 0.5 * jiod, 0.5*jioh])
    cube_lst.append([jiow, jiol, jioh])
    finallst.append([cube_lst, GRAY, BLACK,'left leg'])
    
    '''生成身体'''
    cube_lst = []
    cube_lst.append([50, 50 , jioh+bodyh*0.5])
    cube_lst.append([bodyw,bodyl,bodyh-1])
    finallst.append([cube_lst, GRAY, BLACK,'body'])
    
    '''生成右胳膊'''
    cube_lst=[]
    cube_lst.append([50 - 0.5 * bodyw+0.5*armw, 50 - 0.5 * bodyl - 0.5*arml,  jioh+bodyh-armh])
    cube_lst.append([armw,arml,armh])
    finallst.append([cube_lst, GRAY, BLACK,'right arm'])
    #
    '''生成左胳膊'''
    cube_lst = []
    cube_lst.append([50 - 0.5 * bodyw + 0.5 * armw, 50 + 0.5 * bodyl + 0.5 * arml, jioh + bodyh - armh])
    cube_lst.append([armw, arml, armh])
    finallst.append([cube_lst, GRAY, BLACK,'left arm'])

    '''生成脑袋'''
    cube_lst = []
    cube_lst.append([50,50,jioh+bodyh+0.5*headh])
    cube_lst.append([headw,headl,headh])
    finallst.append([cube_lst, GRAY, BLACK,'head'])

    return finallst
''''''
# def block_preload():
#     blocklst = []
#
#     blocklst.append(Men_series([4,13,1],[1,1,1],[4,13,1],GRASS([4,13,1],[1,1,1],e),True,1))
#     blocklst.append(Men_series([16, 13, 1], [1, 1, 2], [16,13,1],GRASS([16, 13, 1], [1, 1, 2], e), True, 1))
#     blocklst.append(Men_series([13, 13, 1], [1, 1, 1],[13,13,1] ,GRASS([13, 13, 1], [1, 1, 1], e), True, 1))
#
#     blocklst.append(Block_series([3,3,  1],[5, 5, 1],SKYBLUE,BLACK,True,1))
#     blocklst.append(Block_series([4, 4, 2], [3, 3, 1], SKYBLUE, BLACK, True, 1))
#     blocklst.append(shot_detect.painter_algorithm.Block([5, 5, 3] , SKYBLUE, BLACK, True,1))
#
#
#     divid_lst = shot_detect.painter_algorithm.block_lst_seg(blocklst)
#
#     return divid_lst

#
# def eyeopen():
#
#     global shot_block
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#         #生成地板参考格子
#         shot_detect.painter_algorithm.block_create.men_draw.mencreate([[0,0,1*e],[world_lenth*e,0,1*e],[world_lenth*e,world_lenth*e,1*e],[0,world_lenth*e,1*e]],GREEN,BLACK,screen,x0,y0,z0,x1,y1,z1)
#         shot_detect.painter_algorithm.block_create.men_draw.floorload(shot_detect.painter_algorithm.block_create.men_draw.floorcreate(world_lenth*e, world_lenth*e, world_lenth, world_lenth, 0, 0, 1*e), YELLOW,screen,x0,y0,z0,x1,y1,z1)
#
#         #直接Load所有的不透明方块
#
#         shot_detect.painter_algorithm.multi_block_load(screen,shot_detect.painter_algorithm.painter_sort(divid_lst,screen,x0,y0,z0,x1,y1,z1,e),block_intransparent_tenser,x0,y0,z0,x1,y1,z1)
#
#         #检测一下鼠标指到了哪个方块``
#         shot_block=shot_detect.shot_to_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e,world_lenth)
#
#
#         shows('xyz:'+str([int(1000*x0)/1000,int(1000*y0)/1000,int(1000*z0)/1000]),(10,30*1+10))
#         shows('eyesight'+str([int(1000*x1)/1000,int(1000*y1)/1000,int(1000*z1)/1000]),(10,30*2+10))
#         shows('xyz'+str([int(x0/e),int(y0/e),int(z0/e)]),(10,30*3+10))
#         shows('block'+str(shot_block),(10,30*4+10))
#         shows('speed'+str(speed),(10,30*6+10))
#         if shot_block!=0:
#              shows('ocp:'+str(block_occupy_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]])+'  wall'+str(air_wall_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]]),(10,30*5+10),)
#         shows('peng'+str(collison_block),(10,30*7+10))
#
#
#
# divid_lst=block_preload()
#
# block_occupy_tensor=shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#
# #更新理由：透明也不一定就意味着不会被鼠标交互
# block_intransparent_tenser=shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
#
#
# #更新理由：不透明不一定就意味这不占体碰撞箱
# air_wall_tensor=shot_detect.wall_preshape( divid_lst, world_lenth)
#
#
#
# collison_block=0
#
#
# gamegoing=True#决定整个进程是否会继续的变量
# while gamegoing:#在游戏进行当中
#
#     # mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
#     # mousey = pygame.mouse.get_pos()[1]
#     # theata = -(mousex - mousex0) / (mousex0 / 180) * PI / 180
#     # fai = -(mousey - mousey0) / (mousey0 / 89) * PI / 180
#     # x1 = math.cos(fai) * math.cos(theata)
#     # if x1==0:
#     #     x1+=0.0001
#     # y1 = math.cos(fai) * math.sin(theata)
#     # if y1==0:
#     #     y1+=0.0001
#     #
#     # z1 = math.sin(fai)
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
#                 block_occupy_tensor=shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                 #air_wall_tensor = shot_detect.painter_algorithm.block_create.block_tensor_create(world_lenth)
#                 block_intransparent_tenser=shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
#                 air_wall_tensor = shot_detect.wall_preshape( divid_lst, world_lenth)
#                 eyeopen()
#             elif event.key==pygame.K_p:#瞬间传送
#                 x0 = 130
#                 y0 = 1702
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
#             elif event.key==pygame.K_j:
#                 occupy_block_test_print([3,4],[3,4],[1,2])
#             elif event.key == pygame.K_k:
#                 angle_print(divid_lst)
#             elif event.key == pygame.K_l:
#                 airwall_test_print([3,4],[3,4],[1,2])
#             elif event.key == pygame.K_m:
#                 print('#####divid_lst#####')
#                 for i in divid_lst:
#                     print(i)
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
#
#                     for i in range(len(divid_lst)):
#                         if divid_lst[i].pos == shot_block[0]:
#                             if divid_lst[i].hardness>0:
#                                 divid_lst.pop(i)
#                                 #divid_lst=shot_detect.delete_block( divid_lst ,shot_block[0])
#                                 block_occupy_tensor = shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                                 block_intransparent_tenser=shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
#                                 air_wall_tensor=shot_detect.wall_preshape( divid_lst, world_lenth)
#                                 eyeopen()
#                                 break
#
#             elif event.button == 2:
#                 pass#print("middle mouse button")
#             elif event.button == 3:
#                 #shot_block = shot_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e)
#                 if shot_block!=0 and shot_block[1]!=0:
#                     divid_lst=shot_detect.add_block(divid_lst,shot_block[1],PINK,YELLOW,1,1)
#                     block_occupy_tensor = shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
#                     block_intransparent_tenser = shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
#                     air_wall_tensor = shot_detect.wall_preshape( divid_lst, world_lenth)
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
#             mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
#             mousey = pygame.mouse.get_pos()[1]
#             if mousex<boundaryx:#防止鼠标跑出边界
#                 pygame.mouse.set_pos(2*mousex0-boundaryx,mousey)
#             elif mousex>2*mousex0-boundaryx:
#                 pygame.mouse.set_pos(boundaryx,mousey)
#             if mousey<boundaryy:
#                 pygame.mouse.set_pos(mousex, boundaryy)
#             elif mousey > 2 * mousey0 -boundaryy:
#                 pygame.mouse.set_pos(mousex,2*mousey0-boundaryy)
#             mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角nn
#             mousey = pygame.mouse.get_pos()[1]
#             theata = -(mousex - mousex0) / ((mousex0-boundaryx) / 360) * PI / 180
#             fai = -(mousey - mousey0) / ((mousey0-boundaryy) / 50) * PI / 180
#             x1 = math.cos(fai) * math.cos(theata)
#             y1 = math.cos(fai) * math.sin(theata)
#             z1 = math.sin(fai)
#
#             eyeopen()
#
#     '''在运动的过程中'''
#     r=shot_detect.painter_algorithm.block_create.men_draw.line_draw.sqr(x1**2+y1**2)
#     if ahead_kd:
#         collison_block=shot_detect.wall_detect(air_wall_tensor, x0,y0,z0,x1,y1,speed/r)
#
#         if  collison_block==0:
#             x0 += x1 * speed/r;
#             y0 += y1 * speed/r;
#             eyeopen()
#             #print(x0,y0)
#         elif  collison_block!=2:  #得到空气墙方块之后对速度进行向量切分
#
#             vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, x1, y1)
#
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#
#     if back_kd:
#         collison_block = shot_detect.wall_detect(air_wall_tensor, x0,y0,z0,-x1,-y1,speed/r)
#         if collison_block==0:
#             x0 -= x1 * speed/r;
#             y0 -= y1 * speed/r
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, -x1, -y1)
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#
#     if left_kd:
#         collison_block = shot_detect.wall_detect(air_wall_tensor, x0, y0,z0, -y1, x1,speed/r)
#         if  collison_block==0:
#             x0 -= y1 * speed/r
#             y0 += x1 * speed/r;
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, -y1, x1)
#             x0 += vestigial_speed[0] * speed / r;
#             y0 += vestigial_speed[1]* speed / r;
#             eyeopen()
#     if right_kd:
#         collison_block = shot_detect.wall_detect(air_wall_tensor,  x0, y0,z0, y1, -x1,speed/r)
#         if collison_block==0:
#             x0 += y1 * speed/r
#             y0 -= speed * x1/r;
#             eyeopen()
#         elif collison_block!=2:
#             vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, y1, -x1)
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
#     C_shows('WSAD前后左右移动',(750,10),screen)
#     C_shows('空格上升，X下降', (750, 40), screen)
#     C_shows('左键挖矿右键放矿', (750, 70), screen)
#     C_shows('R键重置', (750, 100), screen)
#
#     pygame.display.update()#更新显示的画面
#     timer.tick(60)#表示每秒播放60帧
#
# pygame.quit()#及时退出game模块好习惯
