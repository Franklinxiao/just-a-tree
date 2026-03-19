# import copy
# from typing import List
import pygame#引入game模块
import math
import shot_detect
import half_block
import copy
import csv
import time

pygame.init()#game模块的初始化nnnn
pygame.mixer.init()#game播放声音部分的初始化

screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
pygame.display.set_caption("破壁")#设定窗口的标题
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
timer=pygame.time.Clock()#创建time变量

'''2023年重大更新，引入空间方块占用张量'''

block_input_tensor=shot_detect.painter_algorithm.block_create.block_tensor_create(10)
shot_block=[]


'''显示设定'''
e=100#打算做成体素化的游戏，这个就当成单位长度
PI=3.1415926535897932384626
mousex0=0.5*screen.get_width()
mousey0=0.5*screen.get_height()
boundaryx=25
boundaryy=25
scl=1000#中轴线的长度
# ccd=900#人物与摄像机的距离
# basehigh=250
x1=0.707;y1=0.707;z1=0
x0=1*e;y0=1*e;z0=4.5*e;
theata=0;fai=0;
world_lenth=20
'''颜色设定'''

BLACK=(0,0,0)

RED=(255,0,0)
ORINGE=(231,105,40)
YELLOW=(255,255,0)
GREEN=(0,255,0)
Diamond_Blue=(0, 255, 255)
BLUE=(0,0,255)

PURPLE=(135,53,193)
PINK=(232,139,247)
WHITE_PINK=(221,164,226)
WHITE=(255,255,255)
BROWN=(120,80,0)
GRAY=(128,128,128)
SKYBlue=(92,207,249)

'''UI界面设定'''
put_block_color=PINK
weather_show_test_information=False


'''文件操作'''
Read_file=True
# Read_file=True
'''运动设定'''
entity_theata=0
rusht=0
jumpt=0
fall=False
fallt=0
speed=11
ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
g=20
widelimit=math.atan(mousex0/scl)#视线广角极限
uplimit=math.atan(mousey0/scl)#视线仰角极限
couplimit=math.atan(mousey0/(scl**2+mousex0**2)**0.5)#屏幕四角的仰角极限
cowidelimit=math.atan(mousex0/(scl**2+mousey0**2)**0.5)#屏幕四角的广角极限



'''文件间传递的函数集'''
class creature:
    id = 3
    center_pos = [0, 0, 0]
    occupy_space = [0, 0, 0]

    face_x=1
    face_y=0
    face_z=0

    r=2#速度衰减系数

    weather_crush = True

    weather_move=0#0 for stop,1 for goahead, 2 for left,3 for back,4 for right
    cube_list = []

    distance=0
    status = 'wondering'

    def __init__(self, center_pos, oc_space):
        self.center_pos = center_pos
        self.occupy_space = oc_space

    def cube_forword_re_pos(self, lst):

        for i in lst:
            # initial_pos=i[0][0]
            # initial_occu=i[0][1]

            i[0][0]=shot_detect.painter_algorithm.block_create.men_draw.postrans(
                self.center_pos[0]*e,
                self.center_pos[1] * e,
                self.center_pos[2] * e,

                (i[0][0][0]-  50) / 100 * e,
                (i[0][0][1] - 50) / 100 * e,
                (i[0][0][2] - 50) / 100 * e,
                self.face_x,
                self.face_y,
                self.face_z

            )

            for pos in range(len(i[0][1])):
                i[0][1][pos]=i[0][1][pos]/100*e


        self.cube_list=lst


    def cube_lst_replace(self,lst):

        for i in lst:
            # initial_pos=i[0][0]
            # initial_occu=i[0][1]

            for pos in range(len(i[0][0])):
                i[0][0][pos]=(self.center_pos[pos]+(i[0][0][pos]-50)/100)*e

            for pos in range(len(i[0][1])):
                i[0][1][pos]=i[0][1][pos]/100*e


        self.cube_list=lst

class Zombie(creature):

    speed=0
    atk=10
    HP = 100
    M=50
    drop_item='meet'

    interlst=half_block.hito_model_help_build(
    jiow=20,jiol=20,jioh=100,jiod=60,
    bodyl=80,bodyw=40,bodyh=110,
    arml=20,armw=120,armh=20,
    headl=80,headw=80,headh=80
    )


    status = 'wondering'
    def __init__(self, center_pos, oc_space,speed):
        super().__init__(center_pos, oc_space)

        self.center_pos = center_pos
        self.occupy_space = oc_space
        self.speed=speed

    def motion_upgrade(self):
        if self.weather_move:
            if self.weather_move==1:
                self.go_ahead()
            elif self.weather_move==2:
                pass
                # self.go_left()
            elif self.weather_move==3:
                pass
                # self.go_back()
            elif self.weather_move==4:
                pass
                # self.go_right()
            else:
                pass

    def go_ahead(self):

        collison_block = shot_detect.wall_detect(air_wall_tensor, self.center_pos[0]*e, self.center_pos[1]*e,
                                                 self.center_pos[2]*e, self.face_x, self.face_y, self.speed*e )

        if collison_block == 0:
            self.center_pos[0]+=self.speed*self.face_x
            self.center_pos[1]+=self.speed*self.face_y

        elif collison_block != 2:
            vestigial_speed = shot_detect.horizontal_speed_decompositon(collison_block, self.center_pos[0]*e, self.center_pos[1]*e, self.face_x, self.face_y)
            self.center_pos[0] += vestigial_speed[0] * self.speed
            self.center_pos[1] += vestigial_speed[1] * self.speed

        self.cube_lst_replace(copy.deepcopy(self.interlst))

        eyeopen()
    #
    # def go_left(self):
    #     collison_block = shot_detect.wall_detect(air_wall_tensor, self.center_pos[0] * e, self.center_pos[1] * e,
    #                                              self.center_pos[2] * e,  -self.face_y,self.face_x ,self.speed * e)
    #
    #     if collison_block == 0:
    #         self.center_pos[0] -= self.speed * self.face_y
    #         self.center_pos[1] += self.speed * self.face_x
    #
    #     elif collison_block != 2:
    #         vestigial_speed = shot_detect.horizontal_speed_decompositon(collison_block, self.center_pos[0] * e,
    #                                                                     self.center_pos[1] * e, -self.face_y,
    #                                                                     self.face_x)
    #         self.center_pos[0] += vestigial_speed[0] * self.speed
    #         self.center_pos[1] += vestigial_speed[1] * self.speed
    #
    #     self.cube_lst_replace(copy.deepcopy(self.interlst))
    #
    #     eyeopen()
    #
    # def go_back(self):
    #     collison_block = shot_detect.wall_detect(air_wall_tensor, self.center_pos[0] * e, self.center_pos[1] * e,
    #                                              self.center_pos[2] * e, -self.face_x, -self.face_y, self.speed * e)
    #
    #     if collison_block == 0:
    #         self.center_pos[0] -= self.speed * self.face_x
    #         self.center_pos[1] -= self.speed * self.face_y
    #
    #     elif collison_block != 2:
    #         vestigial_speed = shot_detect.horizontal_speed_decompositon(collison_block, self.center_pos[0] * e,
    #                                                                     self.center_pos[1] * e, -self.face_x,
    #                                                                     -self.face_y)
    #         self.center_pos[0] += vestigial_speed[0] * self.speed
    #         self.center_pos[1] += vestigial_speed[1] * self.speed
    #
    #     self.cube_lst_replace(copy.deepcopy(self.interlst))
    #
    #     eyeopen()
    #
    # def go_right(self):
    #     collison_block = shot_detect.wall_detect(air_wall_tensor, self.center_pos[0] * e, self.center_pos[1] * e,
    #                                              self.center_pos[2] * e, self.face_y, -self.face_x, self.speed * e)
    #
    #     if collison_block == 0:
    #         self.center_pos[0] += self.speed * self.face_y
    #         self.center_pos[1] -= self.speed * self.face_x
    #
    #     elif collison_block != 2:
    #         vestigial_speed = shot_detect.horizontal_speed_decompositon(collison_block, self.center_pos[0] * e,
    #                                                                     self.center_pos[1] * e, self.face_y,
    #                                                                     -self.face_x)
    #         self.center_pos[0] += vestigial_speed[0] * self.speed
    #         self.center_pos[1] += vestigial_speed[1] * self.speed
    #
    #     self.cube_lst_replace(copy.deepcopy(self.interlst))
    #
    #     eyeopen()


def entity_shot_detect(creature_list,x0,y0,z0,x1,y1,z1,e,distance_gate):

    creature_lst=copy.deepcopy(creature_list)

    for i in creature_lst:

        #先排除在视线范围之外的实体
        if i.id==3:

            # if  shot_detect.painter_algorithm.block_create.men_draw.line_draw.angle(
            #         i.center_pos[0]  * e - x0, i.center_pos[1]  * e - y0, i.center_pos[2]  * e - z0,
            #     x1,y1,z1
            # )>2*PI/3:
            if ((i.center_pos[0]  * e - x0)*x1+(i.center_pos[1]  * e - y0)*y1+(i.center_pos[2]  * e - z0)*z1)<0:
                for j in creature_list:
                    if j.center_pos==i.center_pos:
                        creature_lst.remove(i)
                        break

            # 再排除手够不到的实体
            if shot_detect.painter_algorithm.block_create.men_draw.line_draw.distance(
                i.center_pos[0]*e,i.center_pos[1]*e,i.center_pos[2]*e,
                x0,y0,z0
            )>distance_gate:
                for j in creature_lst:
                    if j.center_pos==i.center_pos:
                        creature_lst.remove(j)
                        break
            
            
            
    #实体碰撞想理论上是一个空间长方体

    for i in creature_lst:

        #先换算比例，避免大量的乘法
        i.center_pos[0]=i.center_pos[0]*e
        i.center_pos[1] = i.center_pos[1] * e
        i.center_pos[2] = i.center_pos[2] * e

        i.occupy_space[0]=i.occupy_space[0]*e
        i.occupy_space[1] = i.occupy_space[1] * e
        i.occupy_space[2] = i.occupy_space[2] * e



        three_demention_pos=[[],[],[],[],[],[],[],[]]


        three_demention_pos[0]= shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                                     i.center_pos[2] ,
                                                                                     -0.5 * i.occupy_space[0] ,
                                                                                     -0.5 * i.occupy_space[1] ,
                                                                                     -0.5 * i.occupy_space[2] ,
                                                                                     i.face_x, i.face_y, i.face_z)

        three_demention_pos[1]=shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                                     i.center_pos[2] ,
                                                                                     0.5 * i.occupy_space[0] ,
                                                                                     -0.5 * i.occupy_space[1] ,
                                                                                     -0.5 * i.occupy_space[2] ,
                                                                                     i.face_x, i.face_y, i.face_z)

        three_demention_pos[2] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                              i.center_pos[2] ,
                                                                              0.5 * i.occupy_space[0] ,
                                                                              0.5 * i.occupy_space[1] ,
                                                                              -0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        three_demention_pos[3] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                              i.center_pos[2] ,
                                                                              -0.5 * i.occupy_space[0] ,
                                                                              0.5 * i.occupy_space[1] ,
                                                                              -0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        three_demention_pos[4] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1],
                                                                              i.center_pos[2] ,
                                                                              -0.5 * i.occupy_space[0] ,
                                                                              -0.5 * i.occupy_space[1] ,
                                                                              0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        three_demention_pos[5] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                              i.center_pos[2] ,
                                                                              0.5 * i.occupy_space[0] ,
                                                                              -0.5 * i.occupy_space[1] ,
                                                                              0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        three_demention_pos[6] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                              i.center_pos[2] ,
                                                                              0.5 * i.occupy_space[0] ,
                                                                              0.5 * i.occupy_space[1] ,
                                                                              0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        three_demention_pos[7] = shot_detect.painter_algorithm.block_create.men_draw.postrans(i.center_pos[0] , i.center_pos[1] ,
                                                                              i.center_pos[2] ,
                                                                              -0.5 * i.occupy_space[0] ,
                                                                              0.5 * i.occupy_space[1] ,
                                                                              0.5 * i.occupy_space[2] ,
                                                                              i.face_x, i.face_y, i.face_z)

        two_demention_pos=[]
        for j in range(len(three_demention_pos)):
            two_demention_pos.append(
                [
                    shot_detect.painter_algorithm.block_create.men_draw.line_draw.stchx(
                        three_demention_pos[j][0],three_demention_pos[j][1],three_demention_pos[j][2],x1,y1,z1,x0,y0,z0
                    )
                    ,
                    shot_detect.painter_algorithm.block_create.men_draw.line_draw.stchy(
                        three_demention_pos[j][0], three_demention_pos[j][1], three_demention_pos[j][2], x1, y1, z1, x0, y0, z0
                    )
                ]
            )

        #print(two_demention_pos)
        #接下来的想法是筛选出最外面的几个点，之后判断光标在不在最外边的点构成的多边形内就行了

        bad_point_index=[]

        for j in two_demention_pos:
            #判断并且选出最外面的点
            #一般来说长方体所看见的面结合起来均为凸的多边形，所以一般只要用类似最小相位延迟滤波器的证明过程就行？

            initial_forward_x=shot_detect.sign(two_demention_pos[(two_demention_pos.index(j)+1)%len(two_demention_pos)][0]-j[0])
            initial_forward_y=shot_detect.sign(two_demention_pos[(two_demention_pos.index(j)+1)%len(two_demention_pos)][1]-j[1])


            for k in two_demention_pos:
                if j!=k:
                    vecx=shot_detect.sign(k[0]-j[0])
                    vecy=shot_detect.sign(k[1]-j[1])

                    if vecx!= initial_forward_x and vecy!=initial_forward_y:
                        bad_point_index.append(j)
                        break
        #排除在里面的点
        for j in bad_point_index:
            two_demention_pos.remove(j)


        initial_forward_x = shot_detect.sign(two_demention_pos[0][0]-mousex0)
        initial_forward_y = shot_detect.sign(two_demention_pos[0][1]-mousey0)
        for j in two_demention_pos:
            vecx = shot_detect.sign(j[0] - mousex0)
            vecy = shot_detect.sign(j[1] - mousey0)

            if vecx != initial_forward_x and vecy != initial_forward_y:
                bad_point_index.append(j)
                return True

    return False


'''临场调试函数集'''
def shows(draw_string,pos):#显示操作提示语句
    text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置

def C_shows(draw_string,pos,screen):#显示操作提示语句
    game_font = pygame.font.SysFont("SimHei", 30)
    text = game_font.render(draw_string ,False, (255, 255, 0))
    #text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置

def block_preload():

    if  not Read_file:
        blocklst = []
        #生成草
        blocklst.append(half_block.Men_series([4,13,1],[1,1,1],[4,13,1],half_block.GRASS([4,13,1],[1,1,1],e),True,1))
        blocklst.append(half_block.Men_series([16, 13, 1], [1, 1, 2], [16,13,1],half_block.GRASS([16, 13, 1], [1, 1, 2], e), True, 1))
        blocklst.append(half_block.Men_series([13, 13, 1], [1, 1, 1],[13,13,1] ,half_block.GRASS([13, 13, 1], [1, 1, 1], e), True, 1))
        #生成钻石矿
        # blocklst.append(half_block.Block_series([3,3,  1],[5, 5, 1],SKYBLUE,BLACK,True,1))
        # blocklst.append(half_block.Block_series([4, 4, 2], [3, 3, 1], SKYBLUE, BLACK, True, 1))
        # blocklst.append(shot_detect.painter_algorithm.Block([5, 5, 3] , SKYBLUE, BLACK, True,1))
        divid_lst = shot_detect.painter_algorithm.block_lst_seg(blocklst)
    else:
        blocklst=[]
        with open('block_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过标题行，从第一行开始
            for read in reader:
                data = read

                pos=[]
                for i in range(3):
                    pos.append(int(data[i]))
                mencolor=(int(data[3]),int(data[4]),int(data[5]))
                linecolor=(int(data[6]),int(data[7]),int(data[8]))
                block_hardness=int(data[9])
                block_id=int(data[10])

                # blocklst = shot_detect.add_block(blocklst, pos, mencolor, linecolor, block_id, block_hardness)
                blocklst.append(shot_detect.painter_algorithm.Block(pos, mencolor, linecolor, True, block_hardness))

            divid_lst = shot_detect.painter_algorithm.block_lst_seg(blocklst)
    return divid_lst

def creature_preload():
    creature_lst=[]

    zb1 = Zombie([13.5, 5.5, 1.5], [1, 1, 2], 0.1)
    zb1.cube_lst_replace(copy.deepcopy(zb1.interlst))
    creature_lst.append(zb1)
    return creature_lst


def eyeopen():

    global shot_block
    if not(pygame.mouse.get_visible()):
        screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
        #生成地板参考格子
        #shot_detect.painter_algorithm.block_create.men_draw.mencreate([[0,0,1*e],[world_lenth*e,0,1*e],[world_lenth*e,world_lenth*e,1*e],[0,world_lenth*e,1*e]],GREEN,BLACK,screen,x0,y0,z0,x1,y1,z1)
        shot_detect.painter_algorithm.block_create.men_draw.floorload(shot_detect.painter_algorithm.block_create.men_draw.floorcreate(world_lenth*e, world_lenth*e, world_lenth, world_lenth, 0, 0, 1*e), GREEN,screen,x0,y0,z0,x1,y1,z1)

        #直接Load所有的方块和实体
        divid_lst = initial_block_lst + creature_lst
        shot_detect.painter_algorithm.multi_block_load(screen,shot_detect.painter_algorithm.painter_sort(divid_lst,screen,x0,y0,z0,x1,y1,z1,e),block_intransparent_tenser,x0,y0,z0,x1,y1,z1)

        #检测一下鼠标指到了哪个方块``
        shot_block=shot_detect.shot_to_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e,world_lenth)

        if weather_show_test_information:
            shows('xyz:'+str([int(1000*x0)/1000,int(1000*y0)/1000,int(1000*z0)/1000]),(10,30*1+10))
            shows('eyesight'+str([int(1000*x1)/1000,int(1000*y1)/1000,int(1000*z1)/1000]),(10,30*2+10))
            shows('xyz'+str([int(x0/e),int(y0/e),int(z0/e)]),(10,30*3+10))
            shows('block'+str(shot_block),(10,30*4+10))
            shows('speed'+str(speed),(10,30*6+10))
            if shot_block!=0:
                 shows('ocp:'+str(block_occupy_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]])+'  wall'+str(air_wall_tensor[shot_block[0][0]][shot_block[0][1]][shot_block[0][2]]),(10,30*5+10),)
            shows('peng'+str(collison_block),(10,30*7+10))

            C_shows('WSAD前后左右移动', (750, 10), screen)
            C_shows('空格上升，X下降', (750, 40), screen)
            C_shows('左键挖矿右键放矿', (750, 70), screen)
            C_shows('R键重置', (750, 100), screen)


initial_block_lst=block_preload()
creature_lst=creature_preload()
# creature_lst=[]
divid_lst=initial_block_lst+creature_lst

block_occupy_tensor=shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)

#更新理由：透明也不一定就意味着不会被鼠标交互
block_intransparent_tenser=shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)

#更新理由：不透明不一定就意味这不占体碰撞箱
air_wall_tensor=shot_detect.wall_preshape( divid_lst, world_lenth)


collison_block=0


gamegoing=True#决定整个进程是否会继续的变量
while gamegoing:#在游戏进行当中

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
            elif event.key==pygame.K_n:#呼出鼠标
                pygame.mouse.set_visible(True)
            elif event.key==pygame.K_r:#复原场景
                initial_block_lst=block_preload()
                creature_lst=creature_preload()
                divid_lst=initial_block_lst+creature_lst
                block_occupy_tensor=shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
                #air_wall_tensor = shot_detect.painter_algorithm.block_create.block_tensor_create(world_lenth)
                block_intransparent_tenser=shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
                air_wall_tensor = shot_detect.wall_preshape( divid_lst, world_lenth)

            elif event.key==pygame.K_p:#瞬间传送
                x0 = 246
                y0 = 235
                z0 = 527
            elif event.key == pygame.K_e:  # 全体实体向右转

                entity_theata-=PI/6
                for entity in creature_lst:
                    entity.face_x=math.cos(entity_theata)
                    entity.face_y=math.sin(entity_theata)
                    entity.cube_forword_re_pos(copy.deepcopy(entity.interlst))

            elif event.key==pygame.K_q:

                entity_theata += PI / 6
                for entity in creature_lst:
                    entity.face_x = math.cos(entity_theata)
                    entity.face_y = math.sin(entity_theata)
                    entity.cube_forword_re_pos(copy.deepcopy(entity.interlst))


            elif event.key==pygame.K_z:#提高摄像机的运动速度
                if speed <= 19:
                    speed = speed + 1
            elif event.key==pygame.K_c:#降低摄像机的运动速度
                if speed >= 2:
                    speed = speed - 1
            elif event.key==pygame.K_i:#
                for entity in creature_lst:
                    entity.weather_move=1

            elif event.key==pygame.K_i:#实体前
                for entity in creature_lst:
                    entity.weather_move=1
            elif event.key == pygame.K_k:#实体后
                for entity in creature_lst:
                    entity.weather_move=3
            elif event.key == pygame.K_j:#实体左
                for entity in creature_lst:
                    print(entity.center_pos)
                    print(entity.occupy_space)
                    print(entity.face_x,entity.face_y,entity.face_z)
            elif event.key == pygame.K_l:#实体右
                for entity in creature_lst:
                    print('########')
                    for element in entity.cube_list:
                        print(element)
            elif event.key==pygame.K_h:#实体停
                for entity in creature_lst:
                    entity.weather_move=0
            elif event.key==pygame.K_u:#实体停
                print(divid_lst)
            elif event.key==pygame.K_1:
                put_block_color=RED
            elif event.key==pygame.K_2:
                put_block_color=ORINGE
            elif event.key==pygame.K_3:
                put_block_color=YELLOW
            elif event.key==pygame.K_4:
                put_block_color=GREEN
            elif event.key==pygame.K_5:
                put_block_color=Diamond_Blue
            elif event.key==pygame.K_6:
                put_block_color=BLUE
            elif event.key==pygame.K_7:
                put_block_color=PURPLE
            elif event.key==pygame.K_8:
                put_block_color=PINK
            elif event.key==pygame.K_9:
                put_block_color=WHITE
            elif event.key==pygame.K_0:
                put_block_color=BLACK
            elif event.key==pygame.K_F3:
                weather_show_test_information=not weather_show_test_information
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
            elif event.key== pygame.K_n:#呼出鼠标
                pygame.mouse.set_visible(False)

        if event.type == pygame.MOUSEBUTTONDOWN:#鼠标click事件
            if event.button == 1:
                #shot_block=shot_detect(block_occupy_tensor,x0,y0,z0,x1,y1,z1,e)

                if entity_shot_detect(creature_lst,x0,y0,z0,x1,y1,z1,e,6*e):
                    print('you successully attack!')

                elif shot_block!=0:

                    for i in range(len(initial_block_lst)):
                        if initial_block_lst[i].id!=3 and initial_block_lst[i].pos == shot_block[0]:
                            if initial_block_lst[i].hardness>0:
                                initial_block_lst.pop(i)
                                divid_lst = initial_block_lst + creature_lst
                                block_occupy_tensor = shot_detect.painter_algorithm.block_occupy_cal(divid_lst,
                                                                                                     world_lenth)
                                block_intransparent_tenser = shot_detect.painter_algorithm.block_intransparent_cal(
                                    divid_lst, world_lenth)
                                air_wall_tensor = shot_detect.wall_preshape(divid_lst, world_lenth)

                                break

            elif event.button == 2:
                print(creature_lst)
                pass#print("middle mouse button")
            elif event.button == 3:
                #shot_block = shot_detect(block_occupy_tensor, x0, y0, z0, x1, y1, z1, e)
                if shot_block!=0 and shot_block[1]!=0:
                    initial_block_lst=shot_detect.add_block(divid_lst,shot_block[1],put_block_color,YELLOW,1,1)
                    divid_lst=initial_block_lst+creature_lst
                    block_occupy_tensor = shot_detect.painter_algorithm.block_occupy_cal(divid_lst,world_lenth)
                    block_intransparent_tenser = shot_detect.painter_algorithm.block_intransparent_cal(divid_lst,world_lenth)
                    air_wall_tensor = shot_detect.wall_preshape( divid_lst, world_lenth)

            elif event.button == 4:
                if speed<=19:
                    speed=speed+1
            elif event.button == 5:
                if speed>=2:
                    speed=speed-1


        if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:

            if not (pygame.mouse.get_visible()):
                mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角
                mousey = pygame.mouse.get_pos()[1]
                if mousex<boundaryx:#防止鼠标跑出边界
                    pygame.mouse.set_pos(2*mousex0-boundaryx,mousey)
                elif mousex>2*mousex0-boundaryx:
                    pygame.mouse.set_pos(boundaryx,mousey)
                if mousey<boundaryy:
                    pygame.mouse.set_pos(mousex, boundaryy)
                elif mousey > 2 * mousey0 -boundaryy:
                    pygame.mouse.set_pos(mousex,2*mousey0-boundaryy)

                mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角nn
                mousey = pygame.mouse.get_pos()[1]
                theata = -(mousex - mousex0) / ((mousex0-boundaryx) / 360) * PI / 180
                fai = -(mousey - mousey0) / ((mousey0-boundaryy) / 80) * PI / 180
                x1 = math.cos(fai) * math.cos(theata)
                y1 = math.cos(fai) * math.sin(theata)
                z1 = math.sin(fai)
                if x1==0:
                    x1+=0.01
                if y1==0:
                    y1+=0.01



    '''在运动的过程中'''
    r=shot_detect.painter_algorithm.block_create.men_draw.line_draw.sqr(x1**2+y1**2)
    if ahead_kd:
        collison_block=shot_detect.wall_detect(air_wall_tensor, x0,y0,z0,x1,y1,speed/r)

        if  collison_block==0:
            x0 += x1 * speed/r;
            y0 += y1 * speed/r;

            #print(x0,y0)
        elif  collison_block!=2:  #得到空气墙方块之后对速度进行向量切分

            vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, x1, y1)

            x0 += vestigial_speed[0] * speed / r;
            y0 += vestigial_speed[1]* speed / r;

    if back_kd:
        collison_block = shot_detect.wall_detect(air_wall_tensor, x0,y0,z0,-x1,-y1,speed/r)
        if collison_block==0:
            x0 -= x1 * speed/r;
            y0 -= y1 * speed/r

        elif collison_block!=2:
            vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, -x1, -y1)
            x0 += vestigial_speed[0] * speed / r;
            y0 += vestigial_speed[1]* speed / r;

    if left_kd:
        collison_block = shot_detect.wall_detect(air_wall_tensor, x0, y0,z0, -y1, x1,speed/r)
        if  collison_block==0:
            x0 -= y1 * speed/r
            y0 += x1 * speed/r;

        elif collison_block!=2:
            vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, -y1, x1)
            x0 += vestigial_speed[0] * speed / r;
            y0 += vestigial_speed[1]* speed / r;

    if right_kd:
        collison_block = shot_detect.wall_detect(air_wall_tensor,  x0, y0,z0, y1, -x1,speed/r)
        if collison_block==0:
            x0 += y1 * speed/r
            y0 -= speed * x1/r;

        elif collison_block!=2:
            vestigial_speed=shot_detect.horizontal_speed_decompositon(collison_block, x0, y0, y1, -x1)
            x0 += vestigial_speed[0] * speed / r;
            y0 += vestigial_speed[1]* speed / r;

    if up_Kd:
        if air_wall_tensor[int(x0/e)] [int(y0/e)] [int((z0+speed)/e)]==0:
            z0+=speed

    if down_Kd:
        if air_wall_tensor[int(x0/e)] [int(y0/e)] [int((z0-speed)/e)]==0:
            z0-=speed


    for i in creature_lst:
        i.motion_upgrade()

    t1=time.time()
    eyeopen()
    dt = time.time() - t1
    C_shows('处理用时：' + str(dt), (500, 10), screen)

    # 绘制十字架
    pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
    pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)



    pygame.display.update()#更新显示的画面
    timer.tick(60)#表示每秒播放60帧

pygame.quit()#及时退出game模块好习惯

headers = ['pos0', 'pos1', 'pos2','menc0','menc1','menc2','linec0','linec1','linec2','hardness','id']
value=[]
for i in divid_lst:
    if i.id==1:
        v_tuple=(i.pos[0],i.pos[1],i.pos[2],i.men_color[0],i.men_color[1],i.men_color[2],i.line_color[0],i.line_color[1],i.line_color[2],i.hardness,i.id)
        value.append(v_tuple)
# 使用open函数把数据写入csv文件
with open('block_data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)     # 初始化写入对象
    # writer = csv.writer(f, delimiter=' ')     # 可修改列之间的分隔符为空格，传入参数delimiter
    writer.writerow(headers)   # 读取一行，调用writerow()传入每行数据完成写入操作
    writer.writerows(value)    # 读取多行，多行写入，参数为二维列表

print('方块放置情况已经保存')