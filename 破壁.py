import pygame#引入game模块
import math

pygame.init()#game模块的初始化
pygame.mixer.init()#game播放声音部分的初始化

screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
pygame.display.set_caption("破壁")#设定窗口的标题
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
timer=pygame.time.Clock()#创建time变量



'''显示设定'''
PI=3.1415926535897932384626
mousex0=0.5*screen.get_width()
mousey0=0.5*screen.get_height()
scl=1000
ccd=900#人物与摄像机的距离
basehigh=250
x1=1;y1=0;z1=0
xc=1001;yc=601;zc=0
xc1=1;yc1=0;zc1=0
x0=xc-x1*ccd;y0=yc-y1*ccd;z0=zc-z1*ccd+basehigh;
BLACK=(0,0,0)
WHITE=(255,255,255)


'''运动设定'''
rusht=0
jumpt=0
fall=False
fallt=0
speed=10
ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
g=20

'''鼠标控制设定'''
widelimit=math.atan(mousex0/scl)#视线广角极限
uplimit=math.atan(mousey0/scl)#视线仰角极限
boundaryx=50
boundaryy=50

'''空间设定'''
room=[4000,1200,800]
d=[[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]]



'''函数集'''
#普通数学函数
def vecpro(a,b):#v1=[@,@,@] ; v2=[@,@,@],返回这两个向量的法向量
    solve=[0,0,0]
    solve[0]=a[1]*b[2]-a[2]*b[1]
    solve[1]=a[2]*b[0]-a[0]*b[2]
    solve[2]=a[0]*b[1]-a[1]*b[0]
    return solve
    pass
def sqr(a):
    return a**0.5
def inverse(a):
    return 2+~a
def angle(xa,ya,za,x2,y2,z2):
    fenmu1=xa**2+ya**2+za**2
    fenmu2=x2**2+y2**2+z2**2
    if fenmu1<=0 :
        fenmu1=0.001
    if fenmu2<=0:
        fenmu2=0.001
    result=(xa*x2+ya*y2+za*z2)/sqr(fenmu1)/sqr(fenmu2)
    if result>1:
        result=1
    if result<-1:
        result=-1
    return math.acos(result)

#3D实现绘制函数
def tnr(d,j):
    abc=[d[0],d[1],d[2]]
    abc[j]=inverse(d[j])
    return abc
def stchx(x2,y2,z2,x1,y1,z1):
    cos1 = x1 * (x2 - x0) + y1 * (y2 - y0) + z1 * (z2 - z0)
    cos2=(-y1*(x2-x0)+x1*(y2-y0))/(1-z1**2)**0.5
    return mousex0-cos2/cos1*scl
def stchy(x2,y2,z2,x1,y1,z1):
    cos1=x1*(x2-x0)+y1*(y2-y0)+z1*(z2-z0)
    cos2=(-x1*z1*(x2-x0)-y1*z1*(y2-y0)+(1-z1**2)*(z2-z0))/sqr(1-z1**2)
    return  mousey0-cos2/cos1*scl
def backorfront(x2,y2,z2,x1,y1,z1):
    hcos=x1*(x2-x0)+y1*(y2-y0)+z1*(z2-z0)
    if hcos>0:
        return 1
    else:
        return 0
def camera(xa,ya,k):#点向式交线框,要求k存在,且不为零
    solve=[[0,0],[0,0]]
    if k!=0:
        cnt=2
        if cnt:
            temp = k * (0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0:
                solve[2 - cnt] = [temp, 0]
                cnt = cnt - 1
        if cnt:
            temp = k* (2 * mousey0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0:
                solve[2 - cnt] = [temp, 2 * mousey0]
                cnt = cnt - 1
        if cnt:
            temp = 1/k * (0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0:
                solve[2 - cnt] = [0, temp]
                cnt = cnt - 1
        if cnt:
            temp = 1/k * (2 * mousex0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0:
                solve[2 - cnt] = [2 * mousex0, temp];
    else:
        solve=[[xa,0],[xa,2*mousey0]]
    return solve
def pole(xa,ya,h,s):#点向式交线框
    solve=[0,0]
    if h!=0 and s!=0:
        cnt=1
        if cnt:
            temp = h/s * (0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0  and (temp-xa)*h+(0-ya)*s>0:
                solve = [temp, 0]
                cnt = cnt - 1
        if cnt:
            temp = h/s* (2 * mousey0 - ya) + xa
            if temp >= 0 and temp <= 2 * mousex0 and (temp-xa)*h+(2*mousey0-ya)*s>0:
                solve = [temp, 2 * mousey0]
                cnt = cnt - 1
        if cnt:
            temp = s/h* (0 - xa) + ya
            if temp >= 0 and temp <= 2 * mousey0 and (0-xa)*h+(temp-ya)*s>0:
                solve = [0, temp]
                cnt = cnt - 1
        if cnt:
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
def show(draw_string):#显示调试语句

    text = font.render(draw_string, True, WHITE)  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    text_rect = text.get_rect()  # 根据已有的文字的大小来制定合适大小的文本框text_rect
    text_rect.bottomleft = screen.get_rect().bottomleft
    text_rect.y = 80  # 设定文本框的纵坐标
    pygame.draw.rect(screen, BLACK, (text_rect.x, text_rect.y, 430,27 ))  # 在屏幕上绘制黑色的矩形
    screen.blit(text, text_rect)  # 将文本框放在屏幕当中，文字也就放好了
def shows(draw_string,pos):#显示操作提示语句
    text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
def linecut(a1,b1,c1,a2,b2,c2,x1,y1,z1,x0,y0,z0):
    if a1!=a2:
        fenzi=x0*x1+y0*y1+z0*z1+a2*(y1*(b1-b2)+z1*(c1-c2))/(a1-a2)-b2*y1-c2*z1
        fenmu=x1+y1*(b1-b2)/(a1-a2)+z1*(c1-c2)/(a1-a2)
        if fenmu==0:
            fenmu+=0.01
        return fenzi/fenmu
    else:
        return a1
def cutback(xa,ya,za,xb,yb,zb):
    solve=[0,0,0]
    solve[0]=linecut(xa,ya,za,xb,yb,zb,x1,y1,z1,x0,y0,z0)
    solve[1]=linecut(ya,xa,za,yb,xb,zb,y1,x1,z1,y0,x0,z0)
    solve[2]=linecut(za,ya,xa,zb,yb,xb,z1,y1,x1,z0,y0,x0)
    return solve

def p2pshow(d1,d2,color):#语法：两个点应该为[x,y,z]三个空间坐标
    export=[]#这是拓展接口，输出在屏幕上显示的两个点的平面坐标
    d=[d1,d2]
    fob=[0,0]
    f=[0,0]
    vsnx=[0,0]
    vsny=[0,0]
    vsnx[0]=stchx(d1[0],d1[1],d1[2],x1,y1,z1)
    vsny[0]=stchy(d1[0],d1[1],d1[2],x1,y1,z1)
    vsnx[1] = stchx(d2[0], d2[1], d2[2], x1, y1, z1)
    vsny[1]= stchy(d2[0], d2[1], d2[2], x1, y1, z1)
    fob[0] = backorfront(d1[0], d1[1], d1[2], x1, y1, z1)
    fob[1]=backorfront(d2[0], d2[1], d2[2], x1, y1, z1)
    for i in range(2):
        if  vsnx[i]> 0 and vsnx[i] < 2 * mousex0 and vsny[i] > 0 and vsny[i] < 2 * mousey0 and fob[i] == 1:
            f[i]=1
        else:
            f[i]=0

    if f[0] * f[1] == 1 and fob[0] * fob[1] == 1:  # 两者都在可见的范围内，画绿色线条
        pygame.draw.line(screen, color, (vsnx[0], vsny[0]),(vsnx[1], vsny[1]), 2)
        export.append([vsnx[0],vsny[0]])
        export.append([vsnx[1], vsny[1]])


    elif not (fob[0] + fob[1] == 0):  # 至少其中一个在我们的"前方"，不管在不在视线内

        if not (f[0] + f[1] == 0):  # 至少一个可见

            # 管它另一个不可见的在哪里，都按照一个在后面，一个可见的操作来。
            xa = d[0][0]
            ya = d[0][1]
            za = d[0][2]
            xb = d[1][0]
            yb = d[1][1]
            zb = d[1][2]

            if f[0] == 0:  # 强行让b类坐标代表不可见的点
                temp = xa;
                xa = xb;
                xb = temp;
                temp = ya;
                ya = yb;
                yb = temp;
                temp = za;
                za = zb;
                zb = temp;

            jsx = stchx(xa, ya, za, x1, y1, z1)
            jsy = stchy(xa, ya, za, x1, y1, z1)

            # 为了防止直线算到后面的视锥，所以就干脆把原有线段在我们后面的部分全部截掉
            if (xa - xb) * x1 + (ya - yb) * y1 + (za - zb) * z1 != 0 and fob[0] * fob[1] == 0:
                cut = cutback(xa, ya, za, xb, yb, zb)
                xb = cut[0];
                yb = cut[1];
                zb = cut[2]
                jup = math.cos(angle(xb - x0, yb - y0, zb - z0, -x1 * z1, -z1 * y1, x1 ** 2 + y1 ** 2))
                jear = math.cos(angle(xb - x0, yb - y0, zb - z0, -y1, x1, 0))

            else:
                j2x = stchx(xb, yb, zb, x1, y1, z1)
                j2y = stchy(xb, yb, zb, x1, y1, z1)
                jup = -(j2y - jsy)
                jear = -(j2x - jsx)

            # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上

            solve = pole(jsx, jsy, -jear, -jup)  # 只需插1个点，因此换个函数。
            pygame.draw.line(screen, color, (jsx, jsy), (solve[0], solve[1]), 2)
            export.append([jsx,jsy])
            export.append([solve[0], solve[1]])

        elif f[0] + f[1] == 0 and fob[0] * fob[1] == 1:  # 两个都在我们的”前面“,但均不可见，画蓝色线条

            d1x = vsnx[0]
            d1y = vsny[0]
            d2x = vsnx[1]
            d2y = vsny[1]
            zone = [[1, 1], [1, 1]]

            # zone[第几个点][的第几个坐标]=的约束情况
            if d1x < 0:
                zone[0][0] = 0
            elif d1x > 2 * mousex0:
                zone[0][0] = 2
            if d1y < 0:
                zone[0][1] = 0
            elif d1y > 2 * mousey0:
                zone[0][1] = 2

            if d2x < 0:
                zone[1][0] = 0
            elif d2x > 2 * mousex0:
                zone[1][0] = 2
            if d2y < 0:
                zone[1][1] = 0
            elif d2y > 2 * mousey0:
                zone[1][1] = 2
            if d2y == d1y:
                pygame.draw.line(screen, color, (0, d1y), (2 * mousex0, d2y), 2)
            else:

                k = (d2x - d1x) / (d2y - d1y)

                if not (zone[0][0] == zone[1][0] or zone[0][1] == zone[1][1]):  # 排除法，排除掉肯定不会与视框相交的部分'''
                    solve = camera(d1x, d1y, k)
                    pygame.draw.line(screen, color, (solve[0][0], solve[0][1]),
                                     (solve[1][0], solve[1][1]), 2)
                    export.append([solve[0][0], solve[0][1]])
                    export.append([solve[1][0], solve[1][1]])

                else:

                    if zone[0][0] == 1 and 1 == zone[1][0] and zone[0][1] + zone[1][1] == 2:  # 在大十字架的上下两个
                        pygame.draw.line(screen, color, (k * (0 - d1y) + d1x, 0),
                                         (k * (2 * mousey0 - d1y) + d1x, 2 * mousey0), 2)
                        export.append([k * (0 - d1y) + d1x, 0])
                        export.append([k * (2 * mousey0 - d1y) + d1x, 2 * mousey0])
                    elif zone[0][1] == 1 and 1 == zone[1][1] and zone[0][0] + zone[1][0] == 2:  # 在大十字架的左右两边
                        pygame.draw.line(screen, color, (0, 1 / k * (0 - d1x) + d1y),
                                         (2 * mousex0, 1 / k * (2 * mousex0 - d1x) + d1y), 2)
                        export.append([0, 1 / k * (0 - d1x) + d1y])
                        export.append([2 * mousex0, 1 / k * (2 * mousex0 - d1x) + d1y])

                    else:
                        pass

        else:  # 两个都不可见，但至少有一个在前面，画红色线条

            xa = d[0][0]
            ya = d[0][1]
            za = d[0][2]
            xb = d[1][0]
            yb = d[1][1]
            zb = d[1][2]

            if fob[0] == 0:  # 强行让b类坐标代表在我们后方的点
                temp = xa;
                xa = xb;
                xb = temp;
                temp = ya;
                ya = yb;
                yb = temp;
                temp = za;
                za = zb;
                zb = temp;

            # 为了防止直线算到后面的视锥，所以就干脆把原有线段在我们后面的部分全部截掉
            cut = cutback(xa, ya, za, xb, yb, zb)
            xb = cut[0];
            yb = cut[1];
            zb = cut[2]

            # 但由于会严重超出视界范围，所以这里只保留极坐标下的角度信息。
            jup = math.cos(angle(xb - x0, yb - y0, zb - z0, -x1 * z1, -z1 * y1, x1 ** 2 + y1 ** 2))
            jear = math.cos(angle(xb - x0, yb - y0, zb - z0, -y1, x1, 0))

            # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上
            jsx = stchx(xa, ya, za, x1, y1, z1)
            jsy = stchy(xa, ya, za, x1, y1, z1)

            zone = [[1, 1], [1, 1]]

            # zone[第几个点][的第几个坐标]=的约束情况
            if jear > 0:
                zone[0][0] = 0  # 说明无穷远点在左方
            elif jear < 0:
                zone[0][0] = 2  # 说明无穷远点在右方
            if jup > 0:
                zone[0][1] = 0  # 说明无穷远点在上方
            elif jup < 0:
                zone[0][1] = 2  # 说明无穷远点在下方

            if jsx < 0:
                zone[1][0] = 0  # 说明前点在左边
            elif jsx > 2 * mousex0:
                zone[1][0] = 2  # 说明前点在右边
            if jsy < 0:
                zone[1][1] = 0  # 说明前点在上面
            elif jsy > 2 * mousey0:
                zone[1][1] = 2  # 说明前点在下边

            # if abs(zone[0][0]-zone[0][1])==2 or abs(zone[0][0]-zone[0][1])==0:#假如无穷远点在四角（好像也有0.01%的概率不是）

            if not (zone[0][0] == zone[1][0] or zone[0][1] == zone[1][1]):  # 排除法，排除掉肯定不会与视框相交的部分'''

                solve = camera(jsx, jsy, jear / jup)
                pygame.draw.line(screen, color, (solve[0][0], solve[0][1]), (solve[1][0], solve[1][1]), 2)
                export.append([solve[0][0], solve[0][1]])
                export.append([solve[1][0], solve[1][1]])
    else:
        pass
    return export
def block_create_asist(d,k):
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
#在不同坐标系下的坐标变换
def postrans(startx,starty,startz,dx,dy,dz,x1,y1,z1):#dx,dy,dz代表你主观想要调整的相对坐标参数，实际会结合x1,y1,z1计算。
    dr=[0,0,0]
    dr[0]=startx+dx*x1+dy*(-y1)/sqr(1-z1**2)+dz*(-x1*z1)/sqr(1-z1**2)
    dr[1]=starty+dx*y1+dy*(+x1)/sqr(1-z1**2)+dz*(-y1*z1)/sqr(1-z1**2)
    dr[2]=startz+dx*z1+dz*sqr(x1**2+y1**2)
    return dr

#生成以及加载到界面的函数
def blockcreate(roomlenth,roomwidth,roomheight,startpos,x1,y1,z1):
    for i1 in range(2):
        for i2 in range(2):
            for i3 in range(2):
                d[i1][i2][i3][0]=i1*roomlenth*x1+i2*roomwidth*(-y1)+i3*roomheight*(-x1*z1)+startpos[0]
                d[i1][i2][i3][1]=i1*roomlenth*y1+i2*roomwidth*x1+i3*roomheight*(-y1*z1)+startpos[1]
                d[i1][i2][i3][2]=i1*roomlenth*z1+i3*roomheight*(x1**2+y1**2)+startpos[2]
    return d
def blockload(d,wallcolor,linecolor):
    global  x1;
    global y1;
    global z1;
    global x0;
    global y0;
    global z0;
    norvec=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rayvec=[[0,0,0],[0,0,0],[0,0,0]]
    midpoint=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    centerpoint=[0.5 * (d[1][0][0][0] + d[0][0][0][0]), 0.5 * (d[0][1][0][1]+d[0][0][0][1]), 0.5 * (d[0][0][0][2] + d[0][0][1][2])]
    midv=[centerpoint[0]-x0,centerpoint[1]-y0,centerpoint[2]-z0]

    #rayvec=[上，前，左，下，后，右]

    for k in range(3):#面向东方：
        rayvec[0][k]=d[1][0][0][k]-d[0][0][0][k]
    for k in range(3):#面向北方：
        rayvec[1][k]=d[0][1][0][k]-d[0][0][0][k]
    for k in range(3):#面向天空（岛）：
        rayvec[2][k]=d[0][0][1][k]-d[0][0][0][k]

    #norvec=[上，前，左，下，后，右]
    for k in range(3):
        norvec[k]=vecpro(rayvec[k],rayvec[(k+1)%3])
    for k in range(3):
        norvec[k+3]=[-norvec[k][0],-norvec[k][1],-norvec[k][2]]

    #midpoint=[上，前，左，下，后，右]
    midpoint[0]=[0.25*(d[1][0][1][0]+d[0][0][1][0]+d[0][1][1][0]+d[1][1][1][0]),0.25*(d[1][0][1][1]+d[0][0][1][1]+d[0][1][1][1]+d[1][1][1][1]),0.25*(d[1][0][1][2]+d[0][0][1][2]+d[0][1][1][2]+d[1][1][1][2])]
    midpoint[1] = [0.25*(d[1][0][0][0]+d[1][0][1][0]+d[1][1][0][0]+d[1][1][1][0]), 0.25*(d[1][0][0][1]+d[1][0][1][1]+d[1][1][0][1]+d[1][1][1][1]), 0.25*(d[1][0][0][2]+d[1][0][1][2]+d[1][1][0][2]+d[1][1][1][2])]
    midpoint[2] = [0.25 * (d[0][1][0][0] + d[0][1][1][0]+d[1][1][0][0]+d[1][1][1][0]), 0.25 * (d[0][1][0][1] + d[0][1][1][1]+d[1][1][0][1]+d[1][1][1][1]),0.25 * (d[0][1][0][2] + d[0][1][1][2]+d[1][1][0][2]+d[1][1][1][2])]
    midpoint[3] = [0.25*(d[1][0][0][0]+d[0][0][0][0]+d[0][1][0][0]+d[1][1][0][0]),0.25*(d[1][0][0][1]+d[0][0][0][1]+d[0][1][0][1]+d[1][1][0][1]),0.25*(d[1][0][0][2]+d[0][0][0][2]+d[0][1][0][2]+d[1][1][0][2])]
    midpoint[4] = [0.25*(d[0][0][0][0]+d[0][0][1][0]+d[0][1][0][0]+d[0][1][1][0]), 0.25*(d[0][0][0][1]+d[0][0][1][1]+d[0][1][0][1]+d[0][1][1][1]), 0.25*(d[0][0][0][2]+d[0][0][1][2]+d[0][1][0][2]+d[0][1][1][2])]
    midpoint[5] = [0.25 * (d[0][0][0][0] + d[0][0][1][0]+d[1][0][0][0]+d[1][0][1][0]), 0.25 * (d[0][0][0][1] + d[0][0][1][1]+d[1][0][0][1]+d[1][0][1][1]),0.25 * (d[0][0][0][2] + d[0][0][1][2]+d[1][0][0][2]+d[1][0][1][2])]

    for i in range(6):
        if angle(norvec[i][0],norvec[i][1],norvec[i][2],midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0)>PI/2 :#and angle(midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0,x1,y1,z1)<PI/2 :#and angle(midpoint[i][0]-x0,midpoint[i][1]-y0,midpoint[i][2]-z0,x1,y1,z1)<PI/2:
            mencreate(block_create_asist(d,i),wallcolor,linecolor)
        #shows(str(midpoint[i])+str(norvec[i]),(10,i*30+10))

    '''for i in [[0, 0, 0], [0, 1, 1], [1, 1, 0], [1, 0, 1]]:
        for j in range(3):
            abc = tnr([i[0], i[1], i[2]], j)
            p2pshow([d[i[0]][i[1]][i[2]][0], d[i[0]][i[1]][i[2]][1], d[i[0]][i[1]][i[2]][2]],
                    [d[abc[0]][abc[1]][abc[2]][0], d[abc[0]][abc[1]][abc[2]][1], d[abc[0]][abc[1]][abc[2]][2]], linecolor)'''
def floorcreate(lenth,width,lensum,widsum,startx,starty,startz):
    #先小小浪费一下空间;

    d=[[[0,0,0] for i in range(widsum+1)]for i in range(lensum+1)]
    for i in range(lensum+1):
        d[i][0][0]=i*lenth/lensum+startx
        d[i][0][1]=starty
        d[i][0][2]=startz
        d[i][widsum][0] = i * lenth / lensum + startx
        d[i][widsum][1]=width+starty
        d[i][widsum][2] = startz

    for i in range(widsum+1):
        d[0][i][0] = startx
        d[0][i][1] = i*width/widsum+starty
        d[0][i][2]=startz
        d[lensum][i][0] = startx+lenth
        d[lensum][i][1] = i*width/widsum+starty
        d[lensum][i][2]=startz

    return d
def floorload(d,color):
    lensum=len(d)
    widsum=len(d[0])
    for i in range(lensum):
        p2pshow([d[i][0][0],d[i][0][1],d[i][0][2]],[d[i][widsum-1][0],d[i][widsum-1][1],d[i][widsum-1][2]],color)
    for i in range(widsum):
        p2pshow([d[0][i][0], d[0][i][1], d[0][i][2]], [d[lensum-1][i][0], d[lensum-1][i][1], d[lensum-1][i][2]], color)
def characrete(startx,starty,startz,x1,y1,z1):

    jiow=20;jiospacing=20;jioh=70
    bodyl=70;bodyw=40;bodyh=110
    arml=20;armw=20;armh=70;
    headl=80;headw=80;headh=80


    blockload(blockcreate(jiow,jiow,jioh,
                          postrans(startx,starty,startz,-0.5*jiow,-0.5*jiospacing-jiow,0,x1,y1,z1)
                          ,x1,y1,z1),(0,0,0),(0,0,200))#第右腿

    blockload(blockcreate(jiow,jiow,jioh,
                          postrans(startx, starty, startz, -0.5 * jiow, 0.5 * jiospacing , 0, x1, y1, z1),
                          x1,y1,z1),(0,0,0),(0,0,200))#第左腿
    startz+=jioh
    blockload(blockcreate(bodyw,bodyl,bodyh,
                          postrans(startx, starty, startz, -0.5 * bodyw, -0.5 * bodyl, 0, x1, y1, z1),
                          x1,y1,z1),(0,0,0),(0,255,255))#身体
    startz+=bodyh-armh
    blockload(blockcreate(arml,armw,armh,
                          postrans(startx, starty, startz, -0.5 * armw, 0.5 * bodyl, 0, x1, y1, z1),
                          x1,y1,z1),(0,0,0),(255,200,200))#左胳膊

    blockload(blockcreate(arml, armw, armh,
                          postrans(startx, starty, startz, -0.5 * armw, -0.5 * bodyl-arml, 0, x1, y1, z1),
                          x1, y1, z1),(0,0,0), (255, 200, 200))  # 右胳膊

    startz+=armh
    blockload(blockcreate(headl,headw,headh,
                          postrans(startx, starty, startz, -0.5 * headw, -0.5 * headl, 0, x1, y1, z1),
                          x1,y1,z1),(0,0,0),(100,100,255))#头
def mencreate(pos,wallcolor,linecolor):#前提是四个点的坐标按顺序连接应该是无交叉的矩形，pos=[@,@,@,@],其中@=[*,*,*]
    ploygonlist=[]
    mennor=vecpro([pos[1][0]-pos[0][0],pos[1][1]-pos[0][1],pos[1][2]-pos[0][2]],
                  [pos[2][0] - pos[1][0], pos[2][1] - pos[1][1], pos[2][2] - pos[1][2]],
                   )
    n=len(pos)
    for i in range(n):#产生由线条产生的待填充多边形的顶点
        p2pd=p2pshow(pos[i],pos[(i+1)%n],wallcolor)
        if not p2pd==[[0,0],[0,0]]:
            for j in ploygonlist:
                for k in p2pd:
                    if j==k:
                        ploygonlist.remove(k)
            ploygonlist.extend(p2pd)

    # 判断屏幕四角上的点该不该列入多边形绘制的端点列表中
    norvec = [[0, 0, 0] for v in range(n)]
    for j in range(n):#计算各个顶点对应的法向量
        norvec[j] = vecpro(
            [pos[j][0]-x0,pos[j][1]-y0,pos[j][2]-z0],
            [pos[(j + 1) % n][0]-x0,pos[(j + 1) % n][1]-y0,pos[(j + 1) % n][2]-z0])

    midv=[(pos[0][0]+pos[1][0]+pos[2][0]+pos[3][0])/n-x0,(pos[0][1]+pos[1][1]+pos[2][1]+pos[3][1])/n-y0,(pos[0][2]+pos[1][2]+pos[2][2]+pos[3][2])/n-z0]
    reverse=0
    releangle = angle(midv[0], midv[1], midv[2], mennor[0], mennor[1], mennor[2])
    if releangle > PI / 2:
        for j in range(3):
            mennor[j] = -mennor[j]
        reverse=1;

    cor4=[]
    for i in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
        [newx1,newy1,newz1] = postrans(0,0,0,scl,i[0]*mousex0,i[1]*mousey0,x1,y1,z1)
        r=sqr(newx1**2+newy1**2+newz1**2)
        newx1=newx1/r
        newy1 = newy1 / r
        newz1 = newz1 / r

        if angle(newx1,newy1,newz1, mennor[0], mennor[1], mennor[2]) < PI / 2:
            forwardflag=1;
        else:
            forwardflag=0;

        flag=[0,0,0,0]

        for j in  range(n):
            prean=newx1*norvec[j][0]+newy1*norvec[j][1]+newz1*norvec[j][2]
            if prean>0:
                flag[j]=1
            else:
                flag[j]=0

        if flag[0]==flag[1] and flag[1]==flag[2] and flag[2]==flag[3] and flag[0]+flag[1]+flag[2]+flag[3]==0 and forwardflag==1 and reverse==1:
            cor4.append([mousex0 * (-i[0] + 1), mousey0 * (-i[1] + 1)])
        elif flag[0] == flag[1] and flag[1] == flag[2] and flag[2] == flag[3] and flag[0] + flag[1] + flag[2] + flag[3] == 4 and forwardflag ==1 and reverse ==0:
            cor4.append([mousex0 * (-i[0] + 1), mousey0 * (-i[1] + 1)])
        #shows(str([x0,y0,z0]),(10,30*(+1)+10))

    cor5=[cor4[j] for j in range(len(cor4))]#备份加去重
    for i in range(len(cor4)):
        for j in range(len(ploygonlist)):
            if cor4[i]==ploygonlist[j]:
                cor5.remove(cor4[i])

    ploygonlist.extend(cor5)

    lenth = len(ploygonlist)

    if lenth>=3:
        lst = [[] for i in range(lenth)]  # 对最终的列表内的元素进行排序，才能生成闭合无交叉的多边形
        loc = [0 for i in range(lenth)]  # 拟定新列表中的次序
        allangle = [0 for i in range(lenth)]
        # loc[0]=0;loc[1]=1;loc[2]=2
        s1 = 0
        p = 1
        s2 = 2
        maxangle = angle(ploygonlist[s1][0] - ploygonlist[p][0], ploygonlist[s1][1] - ploygonlist[p][1], 0,
                         ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1], 0)
        allangle[s1] = maxangle;
        for i in range(lenth - 3):

            langle = angle(ploygonlist[i + 3][0] - ploygonlist[p][0], ploygonlist[i + 3][1] - ploygonlist[p][1], 0,
                           ploygonlist[s1][0] - ploygonlist[p][0], ploygonlist[s1][1] - ploygonlist[p][1], 0)
            rangle = angle(ploygonlist[i + 3][0] - ploygonlist[p][0], ploygonlist[i + 3][1] - ploygonlist[p][1], 0,
                           ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1], 0)

            if langle > maxangle and (langle + rangle + maxangle < 2 * PI or langle == PI)and(langle>rangle):
                s2 = i + 3
                maxangle = langle
                for j in range(i + 3):
                    if j != p and j != s2:
                        allangle[j] += rangle

            elif rangle > maxangle and (langle + rangle + maxangle < 2 * PI or rangle == PI)and(langle<rangle):
                allangle[i + 3] = rangle
                s1 = i + 3
                maxangle = rangle

            elif langle + rangle + maxangle == 2 * PI and rangle != PI and langle != PI:
                p = i + 3
                # 重新计算所有的角度
                for j in range(i + 3):
                    if j != p and j != s2:
                        allangle[j] = angle(ploygonlist[j][0] - ploygonlist[p][0], ploygonlist[j][1] - ploygonlist[p][1], 0,
                                            ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1],
                                            0)
            else:  # 排序的角以rangle为准
                allangle[i + 3] = rangle

        anglerank = [allangle[i] for i in range(len(allangle))]
        anglerank.sort()

        for i in range(lenth):
            if i == s1:
                loc[i] = lenth - 1
            elif i == p:
                loc[i] = 0
            elif i == s2:
                loc[i] = 1
            else:
                loc[i] = anglerank.index(allangle[i])

        for i in range(lenth):
            lst[loc[i]] = ploygonlist[i]

        for i in range(len(lst)):#防止报错的东西
            if lst[i]==0:
                lst[i]=[0,0]
            else:
                for j in range(len(lst[i])):
                    lst[i][j]=int(lst[i][j])

        if len(lst)>=3:
            #shows(str(lst),(10,10))
            pygame.draw.polygon(screen,wallcolor,lst,0)

            for k in range(len(pos)):
                p2pshow(pos[k],pos[(k+1)%len(pos)],linecolor)

#运动函数
def characwalk(w,s,a,d,v):
    global xc
    global yc
    global xc1
    global yc1
    ws = 0;
    ad = 0
    if w:
        ws = 1
    elif s:
        ws = -1
    if a:
        ad = -1
    elif d:
        ad = 1

    if abs(ws) + abs(ad) != 0:
        xc += (ws * x1 + ad * y1) * v/ sqr(abs(ws) + abs(ad)) / sqr(x1 ** 2 + y1 ** 2)
        yc += (ws * y1 - ad * x1) * v / sqr(abs(ws) + abs(ad)) / sqr(x1 ** 2 + y1 ** 2)
        xc1 = (ws * x1 + ad * y1) / sqr(abs(ws) + abs(ad)) / sqr(x1 ** 2 + y1 ** 2)
        yc1 = (ws * y1 - ad * x1) / sqr(abs(ws) + abs(ad)) / sqr(x1 ** 2 + y1 ** 2)
    eyeopen()
def characmove(x1,y1,z1,v):
    global xc
    global yc
    global zc
    global xc1
    global yc1
    xc+=x1*v
    yc+=y1*v
    zc+=z1*v
    eyeopen()

'''统筹显示'''
def eyeopen():
    if not(pygame.mouse.get_visible()):
        screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影

        floorload(floorcreate(8000, 8000, 30, 30, 0, 0, 0), (255, 255, 255))
        blockload(blockcreate(room[0], room[1], room[2], [1000, 1000, 0], 1, 0, 0),(0,0,0), (0, 255, 0))
        #mencreate([[0.5 * room[0], 0, 0], [0.5 * room[0], 0, room[2]], [0.5 * room[0], room[1], room[2]],[0.5 * room[0], room[1], 0]], (0, 0, 0), (0, 0, 255))

        characrete(xc,yc,zc,xc1,yc1,zc1)
        show('press “WSAD” to move,space to up, x to down,esc to exit')


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
                if jumpt==0:
                    jumpt=30

            elif event.key==pygame.K_n:
                pygame.mouse.set_visible(True)
            elif event.key==pygame.K_ESCAPE:
                gamegoing=False
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:#表示按下了w键
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
        if event.type==pygame.MOUSEMOTION or event.type==pygame.KEYDOWN or event.type==pygame.KEYUP:
            mousex = pygame.mouse.get_pos()[0]  # 鼠标控制视角nn
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
            fai = -(mousey - mousey0) / ((mousey0-boundaryy) / 50) * PI / 180
            x1 = math.cos(fai) * math.cos(theata)
            y1 = math.cos(fai) * math.sin(theata)
            z1 = math.sin(fai)
            x0=xc-x1*ccd;y0=yc-y1*ccd;z0=zc-z1*ccd+basehigh;
            eyeopen()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                rusht=45

    #人物移动
    if rusht==0:
        characwalk(ahead_kd,back_kd,left_kd,right_kd,speed)


    if rusht:
        characmove(xc1,yc1,0,speed * 2)
        eyeopen()
        rusht-=1
    if jumpt:
        characmove(0,0,1,speed)
        eyeopen()
        jumpt-=1


     # 状态分析：
    if zc > 0 and jumpt==0:
        fall = True
        fallt=0
    if fall:
        fallt += 1
        characmove(0, 0, -1, 0.5*fallt**2*g)
        if zc - speed * 2 < 0:
            zc = 0
            fall = False



    x0=xc-x1*ccd;y0=yc-y1*ccd;z0=zc-z1*ccd+basehigh;

    eyeopen()


    # 绘制十字架
    pygame.draw.line(screen, WHITE, (mousex0 - 10, mousey0), (mousex0 + 10, mousey0), 2)
    pygame.draw.line(screen, WHITE, (mousex0, mousey0 - 10), (mousex0, mousey0 + 10), 2)

    pygame.display.update()#更新显示的画面
    timer.tick(60)#表示每秒播放60帧

pygame.quit()#及时退出game模块好习惯