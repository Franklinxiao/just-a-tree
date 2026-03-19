# import copy
# from typing import List
#import pygame#引入game模块
import math
import block_create
import copy
from operator import attrgetter

#
# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化
#
# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("破壁")#设定窗口的标题
# pygame.mouse.set_visible(False)
#font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量
#
# '''2023年重大更新，引入空间方块占用张量'''
#
# block_input_tensor=block_create.block_tensor_create(10)
#

#
# '''显示设定'''
#e=100#打算做成体素化的游戏，这个就当成单位长度
PI=3.1415926535897932384626
e=100
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
# scl=1000#中轴线的长度
# # ccd=900#人物与摄像机的距离
# basehigh=250
# x1=1;y1=0;z1=0
# x0=1*e;y0=1*e;z0=1.7*e;
# theata=0;fai=0;
# '''颜色设定'''

# BLACK=(0,0,0)
# RED=(255,0,0)
# GREEN=(0,255,0)
# BLUE=(0,0,255)
# YELLOW=(255,255,0)
# PINK=(255,0,255)
# SKYBLUE=(0,255,255)
# WHITE=(255,255,255)
# BROWN=(120,80,0)
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
#
'''类集合'''
class Block:
    id=1
    pos=[0,0,0]
    men_color=(0,0,0)
    line_color=(0,0,0)
    weather_crush=False
    distance=0
    hardness=0

    def __init__(self,pos,wallcolor,linecolor,weather_crush,hardness):
        self.pos=pos
        self.men_color=wallcolor
        self.line_color=linecolor
        self.weather_crush=weather_crush
        self.hardness=hardness

'''函数集'''
def sign(a):
    if a>0:
        b=1;
    elif a==0:
        b=0;
    else:
        b=-1
    return b
#更具具体描述，填充方块占用空间
#blocklst格式是([[15,15,0],[1,1,3],BROWN,BLACK,e])([放置位置，放置大小,方块颜色，线条颜色，单位长])
def block_occupy_cal(div_blocklst,lenth):

    #初始化
    block_input_tensor=block_create.block_tensor_create(lenth)

    for i in range(lenth):
        for j in range(lenth):
            for k in range(lenth):
                if i == 0 or j == 0 or k == 0 or i == lenth - 1 or j == lenth - 1 or k == lenth - 1:
                    block_input_tensor[i][j][k] = 1

    #遍历
    for i in div_blocklst:
        #print(i)
        if i.id==1:
            block_input_tensor[i.pos[0]][i.pos[1]][i.pos[2]] = 1
        elif i.id==2:
            for dx in range(i.occupy_space[0]):
                for dy in range(i.occupy_space[1]):
                    for dz in range(i.occupy_space[2]):
                        block_input_tensor[i.stp[0] + dx][i.stp[1] + dy][i.stp[2] + dz] = 1

    #block_input_tensor = [block_input_tensorx, block_input_tensory, block_input_tensorz]
    return block_input_tensor

def block_intransparent_cal(div_blocklst,lenth):
    # 初始化
    block_input_tensor = block_create.block_tensor_create(lenth)

    # 遍历
    for i in div_blocklst:
        # print(i)
        if i.id==1:
            block_input_tensor[i.pos[0]][i.pos[1]][i.pos[2]] = 1

    # block_input_tensor = [block_input_tensorx, block_input_tensory, block_input_tensorz]
    return block_input_tensor


def cube_relepos_judge(pos1,occu1,pos2,occu2,p1name,p2name,x0,y0,z0):

    x0_in_cube1_range=  abs(pos1[0] - x0) <= 0.5 * occu1[0]
    y0_in_cube1_range = abs(pos1[1] - y0) <= 0.5 * occu1[1]
    z0_in_cube1_range = abs(pos1[2] - z0) <= 0.5 * occu1[2]



    if  x0_in_cube1_range or y0_in_cube1_range or z0_in_cube1_range:

        loss_demensions=0
        in_cube_range=[x0_in_cube1_range,y0_in_cube1_range,z0_in_cube1_range]
        for i in in_cube_range:
            if i :
                loss_demensions+=1

        d0 = (pos2[0] - pos1[0])
        d1 = (pos2[1] - pos1[1])
        d2 = (pos2[2] - pos1[2])

        x_eyeforward = sign(pos1[0] - x0)
        y_eyeforward = sign(pos1[1] - y0)
        z_eyeforward = sign(pos1[2] - z0)

        x_overlap = abs(d0) < 0.5 * (occu1[0] + occu2[0])
        y_overlap = abs(d1) < 0.5 * (occu1[1] + occu2[1])
        z_overlap = abs(d2) < 0.5 * (occu1[2] + occu2[2])

        eyeforward = [x_eyeforward, y_eyeforward, z_eyeforward]
        d = [d0, d1, d2]
        overlap = [x_overlap, y_overlap, z_overlap]

        if loss_demensions==1:

            loss_index=0
            for i in range(len(in_cube_range)):
                if in_cube_range[i] :
                    loss_index=i

            a_index=(loss_index+1)%3
            b_index=(loss_index+2)%3

            if sign(eyeforward[a_index] *d[a_index])>=0 and sign( eyeforward[b_index] *d[b_index])>=0:
                return 1
            else:
                if eyeforward[a_index] ==d[a_index] and  eyeforward[b_index] !=d[b_index] and overlap[b_index]   :
                    return 1
                elif  eyeforward[a_index] !=d[a_index] and  eyeforward[b_index] ==d[b_index] and overlap[a_index] :
                    return 1
                else:
                    return -1


        elif loss_demensions==2:

            remain_index = 0
            for i in range(len(in_cube_range)):
                if not in_cube_range[i]:
                    remain_index = i
            if eyeforward[remain_index]==d[remain_index]:
                return 1
            else:
                if overlap[(remain_index+1)%3] or overlap[(remain_index+2)%3]:
                    return -1
                else:
                    return 1

        else:
            print('you are stucking!')

    else:
        x_eyeforward=sign(pos1[0]-x0)
        y_eyeforward=sign(pos1[1]-y0)
        z_eyeforward=sign(pos1[2]-z0)

        d0=  (pos2[0] - pos1[0])
        d1 = (pos2[1] - pos1[1])
        d2 = (pos2[2] - pos1[2])

        x_overlap = abs(d0)  < 0.5 * (occu1[0] + occu2[0])
        y_overlap = abs(d1)  < 0.5 * (occu1[1] + occu2[1])
        z_overlap = abs(d2)  < 0.5 * (occu1[2] + occu2[2])

        eyeforward=[x_eyeforward,y_eyeforward,z_eyeforward]
        d=[d0,d1,d2]
        overlap=[x_overlap,y_overlap,z_overlap]

        result=0
        overlap_cnt=0

        # if sign(eyeforward[0]*d[0])>=0 and sign(eyeforward[1]*d[1])>=0 and sign(eyeforward[2]*d[2])>=0 :
        #     return 1
        # if sign(eyeforward[0]*d[0])<0 and sign(eyeforward[1]*d[1])<0 and sign(eyeforward[2]*d[2])<0 :
        #     return -1
        #
        #
        print('******')
        print(eyeforward,p1name,p2name,d,overlap)

        for i in range(3):
            if not overlap[i]:
                if sign(eyeforward[i]*sign(d[i]))>=0:
                    result+=1
                else:
                    result-=1
            else:
                overlap_cnt+=1

        if result==3-overlap_cnt:
            return 1
        elif result==overlap_cnt-3:
            return -1
        else:
            return 0


def block_lst_seg(blocklst):
    divid_lst = []


    for i in blocklst:

        if i.id==11:

            startx = i.stp[0]
            starty = i.stp[1]
            startz = i.stp[2]

            fillx = i.occupy_space[0]
            filly = i.occupy_space[1]
            fillz = i.occupy_space[2]

            for dx in range(fillx):
                for dy in range(filly):
                    for dz in range(fillz):
                        divid_lst.append(Block([startx + dx, starty + dy, startz + dz],i.men_color,i.line_color,i.weather_crush,i.hardness))
        elif i.id==1:
            divid_lst.append(i)

        elif i.id==2:
            divid_lst.append(i)

        elif i.id==3:
            divid_lst.append(i)

    return divid_lst


#适用于两个多边形相交时，没有任何顶点在多边形内的情况，求出交点。
def seek_for_one_intersection_point(d1,d2):

    len1=len(d1)
    len2=len(d2)

    for a_index in range(len1):
        i=d1[a_index]
        j=d1[(a_index+1)%len1]

        if j[0]!=i[0]:#第一个直线不是竖直的，因此斜率存在
            k1=(j[1]-i[1])/(j[0]-i[0])

            for b_index in range(len2):#遍历第二个多边形的所有线段
                o=d2[b_index]
                k=d2[(b_index+1)%len2]

                if o[0]!=k[0]:#第二个直线不是竖直的，因此斜率存在
                    k2=(k[1]-o[1])/(k[0]-o[0])

                    if k1!=k2:#两个线段不平行
                        xcal=(k1*i[0]-k2*o[0]+o[1]-i[1])/(k1-k2)#先求出虚拟的交点
                        if xcal>min([o[0],k[0]]) and xcal<max([o[0],k[0]])  and    xcal>min([i[0],j[0]]) and xcal<max([i[0],j[0]])               :#如果交点均在两条线段的范围内
                            ycal=(xcal-i[0])*k1+i[1]
                            if ycal>min([o[1],k[1]]) and ycal<max([o[1],k[1]]) and ycal>min([i[1],j[1]]) and ycal<max([i[1],j[1]]):
                                return [[xcal,ycal],i]
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:

                    ycal=(o[0]-i[0])*k1+i[1]
                    if ycal > min([o[1], k[1]]) and ycal < max([o[1], k[1]]) and ycal>min([i[1],j[1]]) and ycal<max([i[1],j[1]]): # 如果交点均在两条线段范围内
                        xcal = o[0]
                        if xcal > min([o[0], k[0]]) and xcal < max([o[0], k[0]]) and xcal > min(
                                [i[0], j[0]]) and xcal < max([i[0], j[0]]):
                            return [[xcal, ycal],i]
                        else:
                            pass
                    else:
                        pass



        else:#第一段线段是竖直的，特殊情况特殊处理

            for b_index in range(len2):  # 遍历第二个多边形的所有线段
                o = d2[b_index]
                k = d2[(b_index + 1) % len2]

                if o[0] != k[0]:  # 第二个直线不是竖直的，因此斜率存在
                    k2 = (k[1] - o[1]) / (k[0] - o[0])

                    ycal = k2*(i[0]-o[0])+o[1]  # 先求出虚拟的交点
                    xcal = i[0]
                    if ycal > min([i[1],j[1]]) and ycal < max([i[1], j[1]]) and xcal > min([o[0],k[0]]) and xcal < max([o[0], k[0]]) :  # 如果交点均在两条线段范围内
                        if xcal > min([o[0], k[0]]) and xcal < max([o[0], k[0]]):
                            return [[xcal, ycal], i]
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

    return 0


#当在二维屏幕中得到了交点，需要将这个交点在空间中的位置求出来。
#midp是函数seek_for_one_intersection_point的非0输出中的二维交点坐标
#d1,d2为midp内i对应的三维坐标。
#d11,d22为midp内i对应的三维坐标。

def high_dimensional_inversion(d1,d11,d2,d22,midp):

    ans=[0,0,0]
    if d1[0]!=d2[0]:
        k=(midp[0]-d1[0])/(d2[0]-d1[0])

    else:
        k=(midp[1]-d1[1])/(d2[1]-d1[1])

    ans[0] = d11[0] + (d22[0] - d11[0]) * k
    ans[1] = d11[1] + (d22[1] - d11[1]) * k
    ans[2] = d11[2] + (d22[2] - d11[2]) * k

    return ans

def men_quick_sort(array, start, end, initial_lst):
    if start >= end:
        return

    mid_data, left, right = array[start], start, end

    # print('*******')
    # for i in array:
    #     print(i)


    while left < right:
        # while array[right] >= mid_data and left < right:
        #print('wft?',left,right)

        while ovlap_judge(array[right][3], array[right][0], array[right][4],mid_data[3], mid_data[0],mid_data[4])<=0 and left<right:
            right -= 1
            #print('<-',str(right))

        array[left] = array[right]
        initial_lst[left]=initial_lst[right]


        while ovlap_judge(array[left][3], array[left ][0], array[left][4], mid_data[3], mid_data[0],mid_data[4])>=0 and left < right:
            left += 1
            #print('->',str(left))

        array[right] = array[left]
        initial_lst[right]=initial_lst[left]

    array[left] = mid_data
    men_quick_sort(array, start, left - 1,initial_lst)
    men_quick_sort(array, left + 1, end,initial_lst)

#在所有方块加载之前根据与摄像机的距离进行排序,距离远的先渲染,近的最后渲染,
#本来就在视线后面的直接踢出列表，不渲染。
def painter_sort(divid_lst,screen,x0,y0,z0,x1,y1,z1,e):
    x0=int(x0)
    y0 = int(y0)
    z0 = int(z0)

    #load_block_lst=[i for i in divid_lst]

    load_block_lst=copy.deepcopy(divid_lst)

    #以下循环剔除掉在摄像机后面的方块列表
    for i in divid_lst:
        #divid_lst格式是[[startx + dx, starty + dy, startz + dz], (X,X,X), (X,X,X),id]
        #有时会是[[startx,starty,startz],[lenth,width,height],men_lst , crush'b , id ]
        if i.id==1:

            if  block_create.men_draw.line_draw.angle(
                    (i.pos[0] + 0.5) * e - x0, (i.pos[1] + 0.5) * e - y0, (i.pos[2] + 0.5) * e - z0,
                x1,y1,z1
            )>2*PI/3:

                for j in load_block_lst:
                    if j.id==1:
                        if j.pos==i.pos:
                            load_block_lst.remove(j)
                            break

        #面组筛选和排序:
        elif i.id==2 :

            startx=i.stp[0];starty=i.stp[1];startz=i.stp[2]
            angle=[]
            for dx in range( i.occupy_space[0]):
                for dy in range(i.occupy_space[1]):
                    for dz in range(i.occupy_space[2]):
                        angle.append(
                            # block_create.men_draw.line_draw.angle(
                            #     (startx+dx + 0.5) * e - x0, (starty+dy + 0.5) * e - y0, (startz+dz+ 0.5) * e - z0,
                            #     x1, y1, z1
                            # )
                            ((startx + dx + 0.5) * e - x0)*x1+((starty+dy + 0.5) * e - y0)*y1+((startz+dz+ 0.5) * e - z0)*z1
                        )
            #距离视角最近的都没有的话
            if min(angle)<0 :
                for j in load_block_lst :
                    if j.id==2:
                        if j.pos==i.pos:
                            load_block_lst.remove(j)
                            break
            else:
                #对面组的面的渲染顺序进行排序。
                # compose_lst为 大小为n的面组，其中
                # compose_lst[n][0]为点的位置列表k,
                # k=[
                #           [@,@,@],[@,@,@],.....,[@,@,@]
                #     ]
                # compose_lst[n][1]为compose[n]面的颜色,
                # compose_lst[n][2]为compose[n]的线条的颜色


                compose_lst = copy.deepcopy(i.mens_list)

                compose_lst_lenth=len(compose_lst)
                
                for n in compose_lst:# n=[k,mencolor,linecolor]
                        point3lst= n[0]     
                        lenth=len(point3lst)
                        
                        point2lst=[]
                        for j in range(lenth):
                            point2lst.append(
                                [
                                    block_create.men_draw.line_draw.stchx(point3lst[j][0],point3lst[j][1],point3lst[j][2],x1,y1,z1,x0,y0,z0),
                                    block_create.men_draw.line_draw.stchy(point3lst[j][0], point3lst[j][1],
                                                                          point3lst[j][2], x1, y1, z1, x0, y0, z0)
                                ]
                            )

                        # 产生由线条产生的待填充多边形的顶点
                        # for j in range(lenth):
                        #     p2pd = block_create.men_draw.p2pshow(point3lst[j], point3lst[(j + 1) % lenth], n[2], screen, x1, y1, z1, x0, y0, z0)
                        #     if not p2pd == [[0, 0], [0, 0]]:
                        #         for k in point2lst:
                        #             for l in p2pd:
                        #                 if l == k:
                        #                     point2lst.remove(k)
                        #         point2lst.extend(p2pd)
                        # 这里ploygonlist为 点阵的二维坐标,
                        n.append(point2lst)
                        
                        #面的法向量
                        mennor = block_create.men_draw.vecpro([point3lst[1][0] - point3lst[0][0], point3lst[1][1] - point3lst[0][1], point3lst[1][2] - point3lst[0][2]],
                                        [point3lst[2][0] - point3lst[1][0], point3lst[2][1] - point3lst[1][1], point3lst[2][2] - point3lst[1][2]],
                                        )


                        midv=[0,0,0]
                        for ave in range(len(point3lst)):
                            midv[0]+=point3lst[ave][0]
                            midv[1]+=point3lst[ave][1]
                            midv[2]+=point3lst[ave][2]

                        midv[0]=midv[0]/lenth-x0
                        midv[1] = midv[1] / lenth - y0
                        midv[2] = midv[2] / lenth - z0


                       #reverse = 0
                        releangle = midv[0]*mennor[0]+midv[1]*mennor[1]+midv[2]+mennor[2]
                        if releangle <0:
                            for j in range(3):
                                mennor[j] = -mennor[j]
                            #reverse = 1;
                        
                        
                        n.append( mennor)#添加了点法式的平面方程

                #至此 n 的格式变为：[k,mencolor,linecolor,point2lst, mennor(面法向量)  ]

                # 选择排序框架
                for ib in range(compose_lst_lenth-1):
                    for jb in range(compose_lst_lenth-ib-1):

                        ovlap = ovlap_judge(compose_lst[ib][3], compose_lst[ib][0],compose_lst[ib][4] ,compose_lst[jb+ib+1][3], compose_lst[jb+ib+1][0],compose_lst[jb+ib+1][4])

                        if ovlap== -1 :#如果列表前面的面反而排在列表后面的面的前边，是要进行调换的
                            i.mens_list[ib], i.mens_list[ib + jb + 1] = i.mens_list[ib + jb + 1], i.mens_list[ib]
                            compose_lst[ib],compose_lst[ib+jb+1]=compose_lst[ib+jb+1],compose_lst[ib]

                # # 调用快速排序
                # men_quick_sort(compose_lst, 0, len(compose_lst) - 1,i.mens_list)

        elif i.id==3:

            if (i.center_pos[0] * e - x0)*x1+(i.center_pos[1] * e - y0)*y1+(i.center_pos[2] * e - z0)*z1<0:
                for j in load_block_lst:
                    if j.id==3 :
                        if j.center_pos==i.center_pos:
                            load_block_lst.remove(j)
                            break
            else:

                compose_lst = copy.deepcopy(i.cube_list)
                len_cube=len(compose_lst)

                reledis=0

                print('######')

                for row in range(len_cube):
                    for column in range(len_cube):
                        if row!=column:
                            reledis+=cube_relepos_judge(
                                compose_lst[row][0][0],compose_lst[row][0][1],compose_lst[column][0][0],compose_lst[column][0][1],
                            compose_lst[row][3],compose_lst[column][3],x0,y0,z0)
                        print(cube_relepos_judge(
                                compose_lst[row][0][0],compose_lst[row][0][1],compose_lst[column][0][0],compose_lst[column][0][1],
                            compose_lst[row][3],compose_lst[column][3],x0,y0,z0))
                            # print(compose_lst[row][3],compose_lst[column][3],cube_relepos_judge(
                            #     compose_lst[row][0][0],compose_lst[row][0][1],compose_lst[column][0][0],compose_lst[column][0][1],
                            # x0,y0,z0))

                    compose_lst[row].append(reledis)

                    if len(i.cube_list[row])<=4:
                        i.cube_list[row].append(reledis)
                    else:
                        i.cube_list[row].pop(-1)
                        i.cube_list[row].append(reledis)

                    reledis=0


                for ib in range(len_cube-1):
                    for jb in range(len_cube-ib-1):
                        if compose_lst[ib][-1]>compose_lst[jb+ib+1][-1] :#如果列表前面的面反而排在列表后面的面的前边，是要进行调换的
                            i.cube_list[ib], i.cube_list[ib + jb+1 ] = i.cube_list[ib + jb+1 ], i.cube_list[ib]
                            compose_lst[ib],compose_lst[ib+jb+1]=compose_lst[ib+jb+1],compose_lst[ib]


        else:
            #更多方块类型有待拓展
            pass



    for objects in load_block_lst:
        if objects.id==1 or objects.id==2:
            objects.distance=block_create.men_draw.line_draw.distance(
                (objects.pos[0] + 0.5) * e, (objects.pos[1] + 0.5) * e, (objects.pos[2] + 0.5) * e,
                x0,y0,z0
            )
        elif objects.id==3:
            objects.distance = block_create.men_draw.line_draw.distance(
                (objects.center_pos[0] ) * e, (objects.center_pos[1] ) * e, (objects.center_pos[2] ) * e,
                x0, y0, z0
            )

    load_block_lst.sort(key=attrgetter("distance"),reverse=True)


    return load_block_lst

#判断两个多边形列表之间有无重叠，若没有重叠则返回[0，0],若有重叠则返回[1,3Dpos],i为d1内第一个重叠的点的三维坐标。（可能不是d1而是额外生成的）
def pion(d1,d11,d2,d22):

    len1=len(d1); len2=len(d2)
    interflag = 1;
    for i in range(len1):

        #先假设这个点在多边形的内部，那么只要每一次逆时针绕着多边形走，该点都在左边，那么就能通过假设。只要有一次跑到右边去了，那么就说明，点在外边。
        for j in range(len2):
            vmain = [d2[(j + 1) % len2][0] - d2[j][0], d2[(j + 1) % len2][1] - d2[j][1], 0]
            vsub = [d1[i][0] - d2[j][0],
                    d1[i][1] - d2[j][1],
                    0]
            charge_res = block_create.men_draw.vecpro(vmain, vsub)

            if charge_res[2] > 0:
                interflag = 0;
                break;

        if interflag == 1:
            return [1,d11[i]]

    #接下来进行第二道工序检测，将每一个多边形的边的法向量作为潜在轴，所有线条投影到该轴上，只要存在一条轴，使得投影的区间不相交，那么就判定没有重叠，否则轮番了都有重叠，那么就有重叠
    if interflag==0:

        cnt=0
        for i in range(len(d1)):
            vec_axis=[d1[(i+1)%len(d1)][0]-d1[i][0],d1[(i+1)%len(d1)][1]-d1[i][1]]
            vec_axis=[-vec_axis[1],vec_axis[0]]
            #建立法轴
            #第一个面的所有点在法轴上的投影，选最大最小作为区间
            df1=[]
            for i1 in d1:
                df1.append( block_create.men_draw.line_draw.angle(i1[0],i1[1],0,vec_axis[0],vec_axis[1],0)*
                    math.sqrt(i1[0]**2+i1[1]**2))
            df1=[min(df1),max(df1)]
            
            df2=[]
            for i1 in d2:
                df2.append( block_create.men_draw.line_draw.angle(i1[0],i1[1],0,vec_axis[0],vec_axis[1],0)*
                    math.sqrt(i1[0]**2+i1[1]**2))
            df2=[min(df2),max(df2)]

            if df1[1]<=df2[0] or df2[1]<=df1[0]:#区间没有重叠，说明存在某法轴，让多边形区间不重叠，说明两个多边形不重叠
                return [0,0]
            else:
                cnt+=1
                continue

        if cnt==len(d1):#完蛋,有重叠，而且没有点，

            insection_p=seek_for_one_intersection_point(d1,d2)

            if insection_p!=0:
                index=d1.index(insection_p[1])

                if insection_p!=0:
                    return [1,high_dimensional_inversion(d1[index],d11[index],d1[(index+1)%len(d1)],d11[(index+1)%len(d11)],insection_p[1])]



    return [0,0]

def ovlap_judge(d1, d11, men1,d2, d22,men2):#d1=[[@,@],[@,@]....],d2=[[@,@],[@,@],...]
    # 判断三维空间内多边形之间是否有重叠并且判断前后，0表示没有重叠，1表示d1在d2的前面，-1表示d1在d2的后面
    #d11,d22是实际三维的坐标

    # len1=len(d1)
    # len2=len(d2)
    # zlst = [i[2] for i in d2]

    ovlap_flag=pion(d1,d11,d2,d22)
    if ovlap_flag[0]==0:
        #两个面毫无重叠，比较没有意义
        return 0

    else:
        jtg=ovlap_flag[1]

        #从第一个面的第一个重叠的点向第二面的第一个点作向量
        fishing_line=[jtg[0]-d22[0][0], jtg[1]-d22[0][1],jtg[2]-d22[0][2] ]

        # forward=block_create.men_draw.line_draw.angle(fishing_line[0],fishing_line[1],fishing_line[2],men2[0],men2[1],men2[2])
        forward=fishing_line[0]*men2[0]+fishing_line[1]*men2[1]+fishing_line[2]*men2[2]
        if forward>0:
            return 1
        elif forward<0:
            return -1
        else:
            return False


#其余的狠狠的渲染
def multi_block_load(screen,load_block_lst,block_input_tensor,x0,y0,z0,x1,y1,z1):
    # load_block_lst格式是[[X,X,X], (X,X,X), (X,X,X),id,distance]
    #或者是[[X,X,X],  [X,X,X],  lst,  crush_or_not,  id,distance]
    for i in load_block_lst:
        if i.id==1:#说明被渲染对象为普通方块
            block_create.blockinput(i.pos, [1, 1, 1], i.men_color, i.line_color, block_input_tensor, screen, x0, y0, z0, x1, y1, z1)
        elif i.id==2:#说明渲染对象为不透明面组：
            for men in i.mens_list:
                block_create.men_draw.mencreate(men[0],men[1],men[2],screen,x0,y0,z0,x1,y1,z1)
        elif i.id==3:
            for cube in i.cube_list:

                block_create.creature_cube_load(block_create.men_draw.blockcreate(
                    cube[0][1][0],cube[0][1][1],cube[0][1][2],
                    # [cube[0][0][0]-0.5*cube[0][1][0],cube[0][0][1]-0.5*cube[0][1][1],cube[0][0][2]-0.5*cube[0][1][2]],
                    block_create.men_draw.postrans(
                        cube[0][0][0],cube[0][0][1],cube[0][0][2],
                        0.5 * cube[0][1][0],0.5*cube[0][1][1],-0.5*cube[0][1][2],
                        -i.face_x,-i.face_y,-i.face_z
                    )
                    ,i.face_x, i.face_y, i.face_z)

                     ,cube[1],cube[2],screen,x0,y0,z0,x1,y1,z1)

#
# def shows(screen,font,draw_string,pos):#显示操作提示语句
#     text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
#
# def eyeopen():
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#
#         #生成地板参考格子
#         block_create.men_draw.floorload(block_create.men_draw.floorcreate(11*e, 11*e, 11, 11, 0, 0, 0), GREEN,screen,x0,y0,z0,x1,y1,z1)
#
#         blocklst=[]
#         blocklst.append([[5,5,0],[1,1,3],BROWN,BLACK])
#         blocklst.append([[3,3,3],[5,5,2],GREEN,BLACK])
#         blocklst.append([[4,4 , 5], [3, 3, 1],GREEN,BLACK])
#
#         divid_lst=block_lst_seg(blocklst)
#         multi_block_load(painter_sort(divid_lst,x0,y0,z0,x1,y1,z1,e),block_occupy_cal(blocklst),x0,y0,z0,x1,y1,z1)
#
#         #print(block_occupy_cal(blocklst))
#
#         shows(str([x0,y0,z0]),(10,30*(+1)+10))
#         shows(str([x1,y1,z1]),(10,30*(+2)+10))
#
# gamegoing=True#决定整个进程是否会继续的变量
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
#             elif event.key==pygame.K_p:#瞬间传送
#                 x0 = 247.866
#                 y0 = -70
#                 z0 = 160
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
#     r=block_create.men_draw.line_draw.sqr(x1**2+y1**2)
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
#     # 绘制十字架
#     pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
#     pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)
#
#     pygame.display.update()#更新显示的画面
#     timer.tick(60)#表示每秒播放60帧
#
# pygame.quit()#及时退出game模块好习惯
