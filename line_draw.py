import pygame#引入game模块
import math
import numpy as np
# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化
#
# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("3 to 2")#设定窗口的标题
# pygame.mouse.set_visible(False)
# font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量
#
#
# '''
# 重要注释
#
#
# 绿色：2个端点均在屏幕内
# 黄色：1个端点在屏幕内，另一个在屏幕外
# 浅蓝色：2个端点均在屏幕外，但都在摄像机的面前
# 红色：1个端点在摄像机的面前，1个在背后。
#
# 黑色：两个端点都在摄像机背后的直线是不会显示的。
#
# '''
#
#
# '''初始的设定'''
PI=3.1415926535897932384626
scl=1000
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
mousex0=500
mousey0=300
# BLACK=(0,0,0)
# WHITE=(255,255,255)
# x0=1001;y0=601;z0=105;
# x1=1;y1=0;z1=0
# speed=10
# widelimit=math.atan(mousex0/scl)#视线广角极限
# uplimit=math.atan(mousey0/scl)#视线仰角极限
#
roomlenth=4000
roomwidth=1200
roomheight=1000
# room=[roomlenth,roomwidth,roomheight]
# ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False#控制按键初始化
#
d=[[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]]
#
#
# vsnx=[[[0,0],[0,0]],[[0,0],[0,0]]]
# vsny=[[[0,0],[0,0]],[[0,0],[0,0]]]

'''函数集'''

def sqr(a):
    return a**0.5

def distance(xa,ya,za,xb,yb,zb):
    return sqr((xb-xa)**2+(yb-ya)**2+(zb-za)**2)

#取反，1，0相互转换
def inverse(a):
    return 1-a

#tnr为日语tonari的简写。意思是旁边
#d为干顶点的编号，j为干节点下遍历的顺序。
#返回支顶点的[1,0,0]形式的额编号
def tnr(d,j):
    abc=[d[0],d[1],d[2]]
    abc[j]=inverse(d[j])
    return abc

#输入x2、y2、z2为客观空间的坐标，x1,y1,z1为视角的方向向量, 输出该点在屏幕上的横坐标
def stchx(x2,y2,z2,x1,y1,z1,x0,y0,z0):
    cos1 = x1 * (x2 - x0) + y1 * (y2 - y0) + z1 * (z2 - z0)
    cos2=(-y1*(x2-x0)+x1*(y2-y0))/(1-z1**2)**0.5
    if cos1==0:
        cos1=cos1+0.000001
    return mousex0-cos2/cos1*scl

#输入x2、y2、z2为客观空间的坐标，x1,y1,z1为视角的方向向量, 输出该点在屏幕上的纵坐标
def stchy(x2,y2,z2,x1,y1,z1,x0,y0,z0):
    cos1=x1*(x2-x0)+y1*(y2-y0)+z1*(z2-z0)
    cos2=(-x1*z1*(x2-x0)-y1*z1*(y2-y0)+(1-z1**2)*(z2-z0))/sqr(1-z1**2)
    if cos1 == 0:
        cos1 = cos1 + 0.000001
    return  mousey0-cos2/cos1*scl

# 判断该点在身前还是身后
def backorfront(x2,y2,z2,x1,y1,z1,x0,y0,z0):
    hcos=x1*(x2-x0)+y1*(y2-y0)+z1*(z2-z0)
    if hcos>0:
        return 1
    else:
        return 0

#求得两组向量的夹角,单位为弧度制
# def angle(xa,ya,za,x2,y2,z2):
#     fenmu1 =xa ** 2 + ya ** 2 + za ** 2
#     fenmu2=x2**2+y2**2+z2**2
#     if fenmu1==0:
#         fenmu1+=0.01
#     if fenmu2==0:
#         fenmu2+=0.01
#     result = (xa * x2 + ya * y2 + za * z2) / (sqr(fenmu1 *fenmu2))
#
#     if result > 1:
#         result = 1
#     elif result < -1:
#         result = -1
#
#     return math.acos(result)

def angle(xa,ya,za,xb,yb,zb):
    a = np.array([xa, ya, za])
    b = np.array([xb, yb, zb])
    cos_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    if cos_angle> 1:
        cos_angle = 1
    elif cos_angle < -1:
        cos_angle = -1
    angle = np.arccos(cos_angle)
    return angle


#点向式交屏幕框,要求k(斜率)存在,且不为零
#当两个端点都在前方不可见时，为了让电脑正常显示，返回让绘制线条函数能接受的两个screen边缘坐标，
#输入为xa,ya为屏幕上的坐标，k为屏幕上的斜率(x/y)，竖直为0,水平为无穷
def camera(xa,ya,k):
    solve=[[0,0],[0,0]]
    if k!=0:
        cnt=2
        if cnt:
            #先将屏幕上边长与初始直线相交，得到横坐标temp,若temp在0至2mousex内,存之
            temp = k * (0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0:
                solve[2 - cnt] = [temp, 0]
                cnt = cnt - 1

        if cnt:
            # 再将屏幕下边长与初始直线相交，得到横坐标temp,若temp在0至2mousex内,存之
            temp = k* (2 * mousey0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0:
                solve[2 - cnt] = [temp, 2 * mousey0]
                cnt = cnt - 1
        if cnt:
            # 先将屏幕左与初始直线相交，得到纵坐标temp,若temp在0至2mousey内,存之
            temp = 1/k * (0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0:
                solve[2 - cnt] = [0, temp]
                cnt = cnt - 1
        if cnt:
            # 将屏幕右边长与初始直线相交，得到纵坐标temp,若temp在0至2mousey内,存之
            temp = 1/k * (2 * mousex0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0:
                solve[2 - cnt] = [2 * mousex0, temp]

    else:
        #当线条完全竖直的情况下
        solve=[[xa,0],[xa,2*mousey0]]
    return solve


#h为水平的基向量？s为竖直的基向量？h/s或者s/h为斜率。
#当其中一个可见时，另一个端点都在前方不可见时，为了让电脑正常显示，返回让绘制线条函数能接受的一个screen边缘坐标，
#输入为xa,ya为屏幕上的坐标，

def pole(xa,ya,h,s):#点向式交线框
    solve=[0,0]
    if h!=0 and s!=0:
        cnt=1
        if cnt:
            # 先将屏幕上边长与初始直线相交，得到横坐标temp,若temp在0至2mousex内,存之
            temp = h/s * (0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0  and (temp-xa)*h+(0-ya)*s>0:
                solve = [temp, 0]
                cnt = cnt - 1
        if cnt:
            # 先将屏幕下边长与初始直线相交，得到横坐标temp,若temp在0至2mousex内,存之
            temp = h/s* (2 * mousey0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0 and (temp-xa)*h+(2*mousey0-ya)*s>0:
                solve = [temp, 2 * mousey0]
                cnt = cnt - 1
        if cnt:
            # 先将屏幕左边长与初始直线相交，得到横坐标temp,若temp在0至2mousey0内,存之
            temp = s/h* (0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0 and (0-xa)*h+(temp-ya)*s>0:
                solve = [0, temp]
                cnt = cnt - 1
        if cnt:
            # 先将屏幕右边长与初始直线相交，得到横坐标temp,若temp在0至2mousey0内,存之
            temp = s/h * (2 * mousex0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0 and (2*mousex0-xa)*h+(temp-ya)*s>0:
                solve = [2 * mousex0, temp]

    elif h==0:
        if s>0:
            solve=[xa,2*mousey0]
        else:
            solve=[xa,0]
    else :
        if h>0:
            solve=[2*mousex0,ya]
        else:
            solve=[0,ya]
    return solve

#显示调试语句
# def show(draw_string):
#     text = font.render(draw_string, True, WHITE)  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     text_rect = text.get_rect()  # 根据已有的文字的大小来制定合适大小的文本框text_rect
#     text_rect.bottomleft = screen.get_rect().bottomleft
#     text_rect.y = 80  # 设定文本框的纵坐标
#     pygame.draw.rect(screen, BLACK, (text_rect.x, text_rect.y, 430,27 ))  # 在屏幕上绘制黑色的矩形
#     screen.blit(text, text_rect)  # 将文本框放在屏幕当中，文字也就放好了

#遇到红色类型的线条时，把摄像机身后的点移动到【视线法平面】上
#[a1,b1,c1]为身后点的坐标，[a2,b2,c2]为身前点的坐标，[x1,y1,z1]为视线,[x0,y0,z0]为摄像机坐标
#返回值为   【视线法平面】上的a坐标
def linecut(a1,b1,c1,a2,b2,c2,x1,y1,z1,x0,y0,z0):
    if a1!=a2:
        fenzi=x0*x1+y0*y1+z0*z1+a2*(y1*(b1-b2)+z1*(c1-c2))/(a1-a2)-b2*y1-c2*z1
        fenmu=x1+y1*(b1-b2)/(a1-a2)+z1*(c1-c2)/(a1-a2)
        if fenmu==0:
            fenmu+=0.01
        return fenzi/fenmu
    else:
        return a1

#对linecut函数的重复调用
#[xa,ya,za]为身前的点，[xb,yb,zb]为身后的点
def cutback(xa,ya,za,xb,yb,zb,x0,y0,z0,x1,y1,z1):
    solve=[0,0,0]
    solve[0]=linecut(xa,ya,za,xb,yb,zb,x1,y1,z1,x0,y0,z0)
    solve[1]=linecut(ya,xa,za,yb,xb,zb,y1,x1,z1,y0,x0,z0)
    solve[2]=linecut(za,ya,xa,zb,yb,xb,z1,y1,x1,z0,y0,x0)
    return solve



#封印，别删
'''创建点的集合'''
# for i1 in range(2):
#     for i2 in range(2):
#         for i3 in range(2):
#                 d[i1][i2][i3][0]=i1*roomlenth
#                 d[i1][i2][i3][1]=i2*roomwidth
#                 d[i1][i2][i3][2]=i3*roomheight

# def eyeopen(theata,fai):
#
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#
#         # show(str(int(x1 * 1000) / 1000) + ' ' + str(int(1000 * y1) / 1000) + ' ' + str(int(1000*z1)/1000) +'#'+
#         #      str(int(x0 * 1000) / 1000) + ' ' + str(int(1000 * y0) / 1000) + ' ' + str(int(1000 * z0) / 1000)
#         #      )
#
#         #八个位置对应八个顶点
#         seeable = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
#         bof = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
#
#         # 先检测该点是否在视野里可见，备用
#         for i1 in range(2):
#             for i2 in range(2):
#                 for i3 in range(2):
#                     vsnx[i1][i2][i3] = stchx(d[i1][i2][i3][0], d[i1][i2][i3][1], d[i1][i2][i3][2], x1, y1, z1)
#                     vsny[i1][i2][i3] = stchy(d[i1][i2][i3][0], d[i1][i2][i3][1], d[i1][i2][i3][2], x1, y1, z1)
#                     bof[i1][i2][i3] = backorfront(d[i1][i2][i3][0], d[i1][i2][i3][1], d[i1][i2][i3][2], x1, y1, z1)
#                     if vsnx[i1][i2][i3] > 0 and vsnx[i1][i2][i3] < 2 * mousex0 and vsny[i1][i2][i3] > 0 and vsny[i1][i2][i3] < 2 * mousey0 and bof[i1][i2][i3]==1:
#                         seeable[i1][i2][i3] = 1
#
#         #要想不重复不遗漏的渲染整个长方体
#         #先挑出有代表性的4个干顶点，其余为支顶点。任意一对干顶点互不相邻，支顶点具有与干顶点同样性质。
#         #遍历干顶点，每一个干顶点加载3边支顶点。
#         for i in [[0, 0, 0], [0, 1, 1], [1, 1, 0], [1, 0, 1]]:
#
#             f = [0, 0, 0, 0]
#             fob = [0, 0, 0, 0]
#             #最后一个位置给干顶点，前三个给支线顶点。
#             f[3] = seeable[i[0]][i[1]][i[2]]
#             fob[3] = bof[i[0]][i[1]][i[2]]
#
#
#             for j in range(3):
#                 #abc为长方体具体的二叉树形状的编号。
#                 abc = tnr([i[0], i[1], i[2]], j)
#                 f[j] = seeable[abc[0]][abc[1]][abc[2]]
#                 fob[j] = bof[abc[0]][abc[1]][abc[2]]
#
#             for j in range(3):
#                 abc = tnr([i[0], i[1], i[2]], j)
#
#                 if f[3] & f[j]  and fob[3] & fob[j] :  # 两者都在可见的范围内，画绿色线条
#                     pygame.draw.line(screen, (0, 255, 0), (vsnx[abc[0]][abc[1]][abc[2]], vsny[abc[0]][abc[1]][abc[2]]),
#                                      (vsnx[i[0]][i[1]][i[2]], vsny[i[0]][i[1]][i[2]]), 2)
#
#                 elif not(fob[3]|fob[j]==0):  # 至少其中一个在我们的"前方"，不管在不在视线内
#
#                     if not(f[3]|f[j]==0):#至少一个可见，画黄色线条
#
#                     #管它另一个不可见的在哪里，都按照一个在后面，一个可见的操作来。
#                         xa = d[abc[0]][abc[1]][abc[2]][0]
#                         ya = d[abc[0]][abc[1]][abc[2]][1]
#                         za = d[abc[0]][abc[1]][abc[2]][2]
#                         xb = d[i[0]][i[1]][i[2]][0]
#                         yb = d[i[0]][i[1]][i[2]][1]
#                         zb = d[i[0]][i[1]][i[2]][2]
#
#                         if f[j] == 0:  # 强行让b类坐标代表不可见的点
#                             xa,xb=xb,xa
#                             ya,yb=yb,ya
#                             za,zb=zb,za
#
#                         jsx = stchx(xa, ya, za, x1, y1, z1)
#                         jsy = stchy(xa, ya, za, x1, y1, z1)
#
#                         # 为了防止直线算到后面的视锥，所以就干脆把原有线段在我们后面的部分全部截掉
#                         if (xa-xb)*x1+(ya-yb)*y1+(za-zb)*z1!=0 and fob[j]*fob[3]==0:
#                             [xb,yb,zb]= cutback(xa, ya, za, xb, yb, zb)
#
#                             jup = math.cos(angle(xb - x0, yb - y0, zb - z0, -x1 * z1, -z1 * y1, x1 ** 2 + y1 ** 2))
#                             jear = math.cos(angle(xb - x0, yb - y0, zb - z0, -y1, x1, 0))
#
#                         else:
#                             j2x=stchx(xb,yb,zb,x1,y1,z1)
#                             j2y=stchy(xb,yb,zb,x1,y1,z1)
#                             jup = -(j2y-jsy)
#                             jear = -(j2x-jsx)
#
#                         # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上
#
#                         solve = pole(jsx, jsy, -jear,-jup)#只需插1个点，因此换个函数。
#                         pygame.draw.line(screen, (255, 255, 0), (jsx,jsy),(solve[0], solve[1]), 2)
#
#
#                     elif f[j]|f[3]==0 and fob[j]&fob[3]:#两个都在我们的”前面“,但均不可见，画蓝色线条
#
#                         d1x=vsnx[i[0]][i[1]][i[2]]; d1y=vsny[i[0]][i[1]][i[2]]
#                         d2x=vsnx[abc[0]][abc[1]][abc[2]];d2y=vsny[abc[0]][abc[1]][abc[2]]
#                         zone=[[1,1],[1,1]]
#
#                         # 对面前的屏幕进行九宫格划分，以可见屏幕为正中间。
#                         #zone[第几个点][的第几个坐标]=的约束情况
#
#                         if d1x<0:
#                             zone[0][0]=0
#                         elif d1x>2*mousex0:
#                             zone[0][0]=2
#                         if d1y<0:
#                             zone[0][1]=0
#                         elif d1y>2*mousey0:
#                             zone[0][1]=2
#
#                         if d2x<0:
#                             zone[1][0]=0
#                         elif d2x>2*mousex0:
#                             zone[1][0]=2
#                         if d2y<0:
#                             zone[1][1]=0
#                         elif d2y>2*mousey0:
#                             zone[1][1]=2
#                         if d2y==d1y:
#                             pygame.draw.line(screen, (0, 0, 255),(0,d1y),(2*mousex0,d2y), 2)
#                         else:
#                             k = (d2x - d1x)/ (d2y - d1y)
#                             if not (zone[0][0] == zone[1][0] or zone[0][1] == zone[1][1]):  # 排除法，排除掉肯定不会与视框相交的部分'''
#                                 solve = camera(d1x,d1y,k)
#                                 pygame.draw.line(screen, (0, 255, 255), (solve[0][0], solve[0][1]),
#                                                  (solve[1][0], solve[1][1]), 2)
#
#                             else:
#
#                                 if zone[0][0]==1 and 1==zone[1][0] and zone[0][1]+zone[1][1]==2:#在大十字架的上下两个
#                                     pygame.draw.line(screen, (0, 255, 255), (k*(0-d1y)+d1x, 0), (k*(2*mousey0-d1y)+d1x, 2*mousey0), 2)
#                                 elif zone[0][1]==1 and 1==zone[1][1] and zone[0][0]+zone[1][0]==2:#在大十字架的左右两边
#                                     pygame.draw.line(screen, (0, 255, 255), (0,1/k * (0 - d1x)+d1y),( 2 * mousex0,1/k * (2 * mousex0 - d1x)+d1y), 2)
#
#                                 else:
#                                     pass
#
#                     else:#两个都不可见，但至少有一个在前面，画红色线条
#
#                         xa = d[abc[0]][abc[1]][abc[2]][0]
#                         ya = d[abc[0]][abc[1]][abc[2]][1]
#                         za = d[abc[0]][abc[1]][abc[2]][2]
#                         xb = d[i[0]][i[1]][i[2]][0]
#                         yb = d[i[0]][i[1]][i[2]][1]
#                         zb = d[i[0]][i[1]][i[2]][2]
#
#                         if fob[j]==0:#强行让b类坐标代表在我们后方的点
#                             temp=xa;xa=xb;xb=temp;
#                             temp=ya;ya=yb;yb=temp;
#                             temp=za;za=zb;zb=temp;
#
#                         #为了防止直线算到后面的视锥，所以就干脆把原有线段在我们后面的部分全部截掉
#                         cut=cutback(xa,ya,za,xb,yb,zb)
#                         xb=cut[0];yb=cut[1];zb=cut[2]
#
#                         # 但由于会严重超出视界范围，所以这里只保留极坐标下的角度信息。
#                         jup=math.cos(angle(xb-x0,yb-y0,zb-z0,-x1*z1,-z1*y1,x1**2+y1**2))
#                         jear=math.cos(angle(xb-x0,yb-y0,zb-z0,-y1,x1,0))
#
#                         # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上
#                         jsx=stchx(xa,ya,za,x1,y1,z1)
#                         jsy=stchy(xa,ya,za,x1,y1,z1)
#
#                         zone = [[1, 1], [1, 1]]
#
#                         # zone[第几个点][的第几个坐标]=的约束情况
#                         if jear > 0:
#                             zone[0][0] = 0#说明无穷远点在左方
#                         elif jear <0:
#                             zone[0][0] = 2#说明无穷远点在右方
#                         if jup > 0:
#                             zone[0][1] = 0#说明无穷远点在上方
#                         elif jup <0:
#                             zone[0][1] = 2#说明无穷远点在下方
#
#                         if jsx < 0:
#                             zone[1][0] = 0#说明前点在左边
#                         elif jsx > 2 * mousex0:
#                             zone[1][0] = 2#说明前点在右边
#                         if jsy < 0:
#                             zone[1][1] = 0#说明前点在上面
#                         elif jsy > 2 * mousey0:
#                             zone[1][1] = 2#说明前点在下边
#
#                         if not(zone[0][0]==zone[1][0] or zone[0][1]==zone[1][1]):#排除法，排除掉肯定不会与视框相交的部分'''
#
#                                 solve=camera(jsx,jsy,jear/jup)
#                                 pygame.draw.line(screen, (255,0,0), (solve[0][0],solve[0][1]),(solve[1][0], solve[1][1]), 2)
#
#                 else:
#                     #都在身后的直线显示不出来。
#                      pass

gamegoing=True#决定整个进程是否会继续的变量
#要想测试就把gamegoing=False改成gamegoing=true
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
#         if event.type==pygame.QUIT:#鼠标点击X按钮退出
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
#             elif event.key==pygame.K_ESCAPE:
#                 gamegoing=False
#         if event.type==pygame.KEYUP:
#             if event.key==pygame.K_w:
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
#         if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:
#             eyeopen(theata,fai)
#
#     if ahead_kd:
#         x0 += x1 * speed;
#         y0 += y1 * speed;
#         eyeopen(theata, fai)
#     if back_kd:
#         x0 -= x1 * speed;
#         y0 -= y1 * speed
#         eyeopen(theata, fai)
#     if left_kd:
#         y0 += x1 * speed;
#         x0 -= y1 * speed
#         eyeopen(theata, fai)
#     if right_kd:
#         y0 -= speed * x1;
#         x0 += y1 * speed
#         eyeopen(theata, fai)
#     if up_Kd:
#         z0+=speed
#         eyeopen(theata,fai)
#     if down_Kd:
#         z0-=speed
#         eyeopen(theata,fai)
#
#     # 绘制十字架
#     pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
#     pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)
#
#     pygame.display.update()#更新显示的画面
#     timer.tick(60)#表示每秒播放60帧
#
# pygame.quit()#及时退出game模块好习惯