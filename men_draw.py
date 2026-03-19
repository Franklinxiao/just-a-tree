import pygame#引入game模块
import math
import line_draw

# pygame.init()#game模块的初始化
# pygame.mixer.init()#game播放声音部分的初始化

# screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
# pygame.display.set_caption("破壁")#设定窗口的标题
# pygame.mouse.set_visible(False)
# font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里
# timer=pygame.time.Clock()#创建time变量
#


'''显示设定'''
PI=3.1415926535897932384626
# mousex0=0.5*screen.get_width()
# mousey0=0.5*screen.get_height()
mousex0=500
mousey0=300

scl=1000#中轴线的长度
# ccd=900#人物与摄像机的距离
# basehigh=250
# x1=1;y1=0;z1=0
# x0=-1000;y0=500;z0=300
BLACK=(0,0,0)
WHITE=(255,255,255)
# theata=0;fai=0;

'''运动设定'''
# fallt=0
# speed=10
# ahead_kd=False;back_kd=False;left_kd=False;right_kd=False;up_Kd=False;down_Kd=False
# widelimit=math.atan(mousex0/scl)#视线广角极限
# uplimit=math.atan(mousey0/scl)#视线仰角极限
# couplimit=math.atan(mousey0/(scl**2+mousex0**2)**0.5)#屏幕四角的仰角极限
# cowidelimit=math.atan(mousex0/(scl**2+mousey0**2)**0.5)#屏幕四角的广角极限
'''空间设定'''
room=[4000,1000,600]
d=[[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]]

'''
写在前面：
men_draw相比于line_draw的最大特色在于：
    mencreate函数。
以及从line_draw提取出了p2pshow 单独两点画线的函数
'''

'''函数集'''

# def shows(draw_string,pos):#显示操作提示语句
#     text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
#     screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置
def vecpro(a,b):#v1=[@,@,@] ; v2=[@,@,@],返回这两个向量的法向量
    solve=[0,0,0]
    solve[0]=a[1]*b[2]-a[2]*b[1]
    solve[1]=a[2]*b[0]-a[0]*b[2]
    solve[2]=a[0]*b[1]-a[1]*b[0]
    return solve

def p2pshow(d1,d2,color,screen,x1,y1,z1,x0,y0,z0):#语法：两个点应该为[x,y,z]三个空间坐标
    export=[]#这是拓展接口，输出在屏幕上显示的两个点的平面坐标
    d=[d1,d2]
    fob=[0,0]
    f=[0,0]
    vsnx=[0,0]
    vsny=[0,0]
    vsnx[0]=line_draw.stchx(d1[0],d1[1],d1[2],x1,y1,z1,x0,y0,z0)
    vsny[0]=line_draw.stchy(d1[0],d1[1],d1[2],x1,y1,z1,x0,y0,z0)
    vsnx[1] = line_draw.stchx(d2[0], d2[1], d2[2], x1, y1, z1,x0,y0,z0)
    vsny[1]= line_draw.stchy(d2[0], d2[1], d2[2], x1, y1, z1,x0,y0,z0)
    fob[0] = line_draw.backorfront(d1[0], d1[1], d1[2], x1, y1, z1,x0,y0,z0)
    fob[1]= line_draw.backorfront(d2[0], d2[1], d2[2], x1, y1, z1,x0,y0,z0)
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

            jsx = line_draw.stchx(xa, ya, za, x1, y1, z1,x0,y0,z0)
            jsy = line_draw.stchy(xa, ya, za, x1, y1, z1,x0,y0,z0)

            # 为了防止直线算到后面的视锥，所以就干脆把原有线段在我们后面的部分全部截掉
            if (xa - xb) * x1 + (ya - yb) * y1 + (za - zb) * z1 != 0 and fob[0] * fob[1] == 0:
                cut = line_draw.cutback(xa, ya, za, xb, yb, zb,x0,y0,z0,x1,y1,z1)
                xb = cut[0];
                yb = cut[1];
                zb = cut[2]
                jup = math.cos(line_draw.angle(xb - x0, yb - y0, zb - z0, -x1 * z1, -z1 * y1, x1 ** 2 + y1 ** 2))
                jear = math.cos(line_draw.angle(xb - x0, yb - y0, zb - z0, -y1, x1, 0))

            else:
                j2x = line_draw.stchx(xb, yb, zb, x1, y1, z1,x0,y0,z0)
                j2y = line_draw.stchy(xb, yb, zb, x1, y1, z1,x0,y0,z0)
                jup = -(j2y - jsy)
                jear = -(j2x - jsx)

            # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上

            solve = line_draw.pole(jsx, jsy, -jear, -jup)  # 只需插1个点，因此换个函数。
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

            if d2y == d1y and zone[1][0]+zone[0][0]==2:
                pygame.draw.line(screen, color, (0, d1y), (2 * mousex0, d2y), 2)
                solve=[[0,d1y+3],[2*mousex0,d1y]]
                export.append([solve[0][0], solve[0][1]])
                export.append([solve[1][0], solve[1][1]])
            elif d2y!=d1y:

                k = (d2x - d1x) / (d2y - d1y)

                if not (zone[0][0] == zone[1][0] or zone[0][1] == zone[1][1]):  # 排除法，排除掉肯定不会与视框相交的部分'''
                    solve = line_draw.camera(d1x, d1y, k)
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
            cut = line_draw.cutback(xa, ya, za, xb, yb, zb,x0,y0,z0,x1,y1,z1)
            xb = cut[0];
            yb = cut[1];
            zb = cut[2]

            # 但由于会严重超出视界范围，所以这里只保留极坐标下的角度信息。
            jup = math.cos(line_draw.angle(xb - x0, yb - y0, zb - z0, -x1 * z1, -z1 * y1, x1 ** 2 + y1 ** 2))
            jear = math.cos(line_draw.angle(xb - x0, yb - y0, zb - z0, -y1, x1, 0))

            # 为了方便计算和讨论，不如把前面的点也给”投影“到以“目向量”为法向量的平面上
            jsx = line_draw.stchx(xa, ya, za, x1, y1, z1,x0,y0,z0)
            jsy = line_draw.stchy(xa, ya, za, x1, y1, z1,x0,y0,z0)

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

                solve = line_draw.camera(jsx, jsy, jear / jup)
                pygame.draw.line(screen, color, (solve[0][0], solve[0][1]), (solve[1][0], solve[1][1]), 2)
                export.append([solve[0][0], solve[0][1]])
                export.append([solve[1][0], solve[1][1]])
    else:
        pass
    return export
#在不同坐标系下的坐标变换
def postrans(startx,starty,startz,dx,dy,dz,x1,y1,z1):#dx,dy,dz代表你主观想要调整的相对坐标参数，实际会结合x1,y1,z1计算。
    dr=[0,0,0]
    dr[0]=startx+dx*x1+dy*(-y1)/line_draw.sqr(1-z1**2)+dz*(-x1*z1)/line_draw.sqr(1-z1**2)
    dr[1]=starty+dx*y1+dy*(+x1)/line_draw.sqr(1-z1**2)+dz*(-y1*z1)/line_draw.sqr(1-z1**2)
    dr[2]=startz+dx*z1+dz*line_draw.sqr(x1**2+y1**2)
    return dr

#生成以及加载到界面的函数
#startpos:构建方块的起始位置
def blockcreate(roomlenth,roomwidth,roomheight,startpos,x1,y1,z1):
    for i1 in range(2):
        for i2 in range(2):
            for i3 in range(2):
                d[i1][i2][i3][0]=i1*roomlenth*x1+i2*roomwidth*(-y1)+i3*roomheight*(-x1*z1)+startpos[0]
                d[i1][i2][i3][1]=i1*roomlenth*y1+i2*roomwidth*x1+i3*roomheight*(-y1*z1)+startpos[1]
                d[i1][i2][i3][2]=i1*roomlenth*z1+i3*roomheight*(x1**2+y1**2)+startpos[2]
    return d

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
def floorload(d,color,screen,x0,y0,z0,x1,y1,z1):
    lensum=len(d)
    widsum=len(d[0])
    #wallcreate([[d[0][0][0],d[0][0][1],d[0][0][2]],[d[0][widsum-1][0],d[0][widsum-1][1],d[0][widsum-1][2]],[d[lensum - 1][widsum-1][0], d[lensum - 1][widsum-1][1], d[lensum - 1][widsum-1][2]],[d[lensum-1][0][0],d[lensum-1][0][1],d[lensum-1][0][2]]])
    for i in range(lensum):
        p2pshow([d[i][0][0],d[i][0][1],d[i][0][2]],[d[i][widsum-1][0],d[i][widsum-1][1],d[i][widsum-1][2]],color,screen,x1,y1,z1,x0,y0,z0)
    for i in range(widsum):
        p2pshow([d[0][i][0], d[0][i][1], d[0][i][2]], [d[lensum-1][i][0], d[lensum-1][i][1], d[lensum-1][i][2]], color,screen,x1,y1,z1,x0,y0,z0)

def mencreate(pos,wallcolor,linecolor,screen,x0,y0,z0,x1,y1,z1):#前提是四个点的坐标按顺序连接应该是无交叉的矩形，pos=[@,@,@,@],其中@=[*,*,*]

    n = len(pos)
    cnt=0
    ploygonlist=[[0,0] for i in range(n)]

    '''2023年重大优化，只要4个点（一般来说是4个）,只要均可见，可直接生成面，无需经过复杂的排序'''
    for i in range(len(pos)):
        ploygonlist[i][0]=line_draw.stchx(pos[i][0],pos[i][1],pos[i][2],x1,y1,z1,x0,y0,z0)
        ploygonlist[i][1]=vsny=line_draw.stchy(pos[i][0],pos[i][1],pos[i][2],x1,y1,z1,x0,y0,z0)
        if ploygonlist[i][0]>0 and ploygonlist[i][0]<2*mousex0 and ploygonlist[i][1]>0 and ploygonlist[i][1]<2*mousey0:
            cnt+=1
    if cnt==4 and cnt==n:
        pygame.draw.polygon(screen, wallcolor, ploygonlist, 0)

        for i in range(n):#产生由线条产生的待填充多边形的顶点
            p2pshow(pos[i],pos[(i+1)%n],linecolor,screen,x1,y1,z1,x0,y0,z0)

    else:
        ploygonlist=[]
        #墙面的法向量
        mennor=vecpro([pos[1][0]-pos[0][0],pos[1][1]-pos[0][1],pos[1][2]-pos[0][2]],
                      [pos[2][0] - pos[1][0], pos[2][1] - pos[1][1], pos[2][2] - pos[1][2]],
                       )

        for i in range(n):#产生由线条产生的待填充多边形的顶点
            p2pd=p2pshow(pos[i],pos[(i+1)%n],linecolor,screen,x1,y1,z1,x0,y0,z0)
            if not p2pd==[[0,0],[0,0]]:
                for j in ploygonlist:
                    for k in p2pd:
                        if j==k:
                            ploygonlist.remove(k)
                ploygonlist.extend(p2pd)

        #遍历每个屏幕四角的点对应的新的视角，若在摄像机与四角墙面组成的四棱锥内：
        #就添加该屏幕四角的点的屏幕坐标到ploygonlist=[]。

        # 判断屏幕四角上的点该不该列入多边形绘制的端点列表中
        norvec = [[0, 0, 0] for v in range(n)]
        for j in range(n):#计算各个顶点对应的法向量
            norvec[j] = vecpro(
                [pos[j][0]-x0,pos[j][1]-y0,pos[j][2]-z0],
                [pos[(j + 1) % n][0]-x0,pos[(j + 1) % n][1]-y0,pos[(j + 1) % n][2]-z0])



        #midv=[(pos[0][0]+pos[1][0]+pos[2][0]+pos[3][0])/n-x0,(pos[0][1]+pos[1][1]+pos[2][1]+pos[3][1])/n-y0,(pos[0][2]+pos[1][2]+pos[2][2]+pos[3][2])/n-z0]
        midv = [0, 0, 0]
        for ave in range(len(pos)):
            midv[0] += pos[ave][0]
            midv[1] += pos[ave][1]
            midv[2] += pos[ave][2]

        midv[0] = midv[0] / n - x0
        midv[1] = midv[1] / n - y0
        midv[2] = midv[2] / n - z0


        reverse=0
        releangle = line_draw.angle(midv[0], midv[1], midv[2], mennor[0], mennor[1], mennor[2])
        if releangle > PI / 2:
            for j in range(3):
                mennor[j] = -mennor[j]
            reverse=1;

        cor4=[]
        for i in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
            [newx1,newy1,newz1] = postrans(0,0,0,scl,i[0]*mousex0,i[1]*mousey0,x1,y1,z1)
            r=line_draw.sqr(newx1**2+newy1**2+newz1**2)
            newx1=newx1/r
            newy1 = newy1 / r
            newz1 = newz1 / r

            #if line_draw.angle(newx1,newy1,newz1, mennor[0], mennor[1], mennor[2]) < PI / 2:
            if mennor[0]*newx1+mennor[1]*newy1+mennor[2]*newz1>0:
                forwardflag=1;
            else:
                forwardflag=0;

            #存储新视角与每个四棱锥侧面的法向量的向量积的正负性，并存储之，
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

        #接下来要对ploygonlist内的元素进行排序，使其顺序相连为凸多边形
        # 对最终的列表内的元素进行排序，才能生成闭合无交叉的多边形

        '''dadeyaolaile'''
        lenth = len(ploygonlist)
        if lenth>=3:

            lst = [[] for i in range(lenth)]
            loc = [0 for i in range(lenth)]  # 拟定新列表中的次序
            allangle = [0 for i in range(lenth)]#储存所有的夹角
            # loc[0]=0;loc[1]=1;loc[2]=2
            s1 = 0
            p = 1
            s2 = 2
            maxangle = line_draw.angle(ploygonlist[s1][0] - ploygonlist[p][0], ploygonlist[s1][1] - ploygonlist[p][1], 0,
                             ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1], 0)
            allangle[s1] = maxangle;


            copy=[ [int(i[0]),int(i[1])] for i in ploygonlist]
            #shows(str(copy),(10,40))

            for i in range(lenth - 3):

                langle = line_draw.angle(ploygonlist[i + 3][0] - ploygonlist[p][0], ploygonlist[i + 3][1] - ploygonlist[p][1], 0,
                               ploygonlist[s1][0] - ploygonlist[p][0], ploygonlist[s1][1] - ploygonlist[p][1], 0)
                rangle = line_draw.angle(ploygonlist[i + 3][0] - ploygonlist[p][0], ploygonlist[i + 3][1] - ploygonlist[p][1], 0,
                               ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1], 0)

                if langle > maxangle and (langle + rangle + maxangle < 2 * PI or langle == PI) and  (langle>rangle):
                    s2 = i + 3
                    maxangle = langle
                    for j in range(i + 3):
                        if j != p and j != s2:
                            allangle[j] += rangle

                elif rangle > maxangle and (langle + rangle + maxangle < 2 * PI or rangle == PI) and (rangle >langle):
                    allangle[i + 3] = rangle
                    s1 = i + 3
                    maxangle = rangle

                elif langle + rangle + maxangle == 2 * PI and rangle != PI and langle != PI:
                    p = i + 3
                    # 重新计算所有的角度
                    for j in range(i + 3):
                        if j != p and j != s2:
                            allangle[j] = line_draw.angle(ploygonlist[j][0] - ploygonlist[p][0], ploygonlist[j][1] - ploygonlist[p][1], 0,
                                                ploygonlist[s2][0] - ploygonlist[p][0], ploygonlist[s2][1] - ploygonlist[p][1],
                                                0)
                else:  # 排序的角以rangle为准
                    allangle[i + 3] = rangle

                #copy = [int(1000*i)/1000 for i in allangle]
                #shows(str([copy,'$$',s1,p,s2,maxangle]), (10, 70 + 30 * i))

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


            '''真复杂'''
            for i in range(lenth):
                lst[loc[i]] = ploygonlist[i]


            for i in lst:
                if not i:
                    lst.remove(i)

            for i in range(len(lst)):#防止报错的东西
                if lst[i]==0 or lst[i]==[]:
                    lst[i]=[0,0]
                else:
                    for j in range(len(lst[i])):
                        lst[i][j]=int(lst[i][j])

            if len(lst)>=3:

                pygame.draw.polygon(screen,wallcolor,lst,0)

                for k in range(len(pos)):
                    p2pshow(pos[k],pos[(k+1)%len(pos)],linecolor,screen,x1,y1,z1,x0,y0,z0)

#统筹显示
# def eyeopen():
#     if not(pygame.mouse.get_visible()):
#         screen.fill(BLACK)  # 重新让整个屏幕变黑，防止运动的图像留下残影
#
#         #blockload(blockcreate(room[0],room[1],room[2],[0,0,0],1,0,0),(0,255,0),x0,y0,z0)
#         floorload(floorcreate(8000, 8000, 30, 30, 0, 0, 0), (255, 255, 255),x0,y0,z0,x1,y1,z1)
#         mencreate([[0.5*room[0], 0, 0], [0.5*room[0], 0,room[2] ], [0.5*room[0],room[1],room[2]], [0.5*room[0],room[1],0]],(0,0,0),(0,255,0),x0,y0,z0,x1,y1,z1)
#        mencreate([[0,0,0.5*room[1]],[0.5*room[0],0,0.5*room[1]],[0.5*room[0],room[1],0.5*room[1]],[0,room[1],0.5*room[1]]],(0,0,255),(0,255,0))
        #
        # mencreate([[room[0], 0, 0], [room[0], 0, room[1]], [ room[0], room[1],  room[1]],
        #            [room[0], room[1], 0]], (0, 255, 255), (255, 0, 0))
        # shows(str([int(x0),int(y0),int(z0)]),(10,500))
        # shows(str([int(1000*x1)/1000,int(1000*y1)/1000,int(1000*z1)/1000]),(10,550))


# def testpointshow(pos):
#
#     stx=line_draw.stchx(pos[0],pos[1],pos[2],x1,y1,z1,x0,y0,z0)
#     sty=line_draw.stchy(pos[0],pos[1],pos[2],x1,y1,z1,x0,y0,z0)
#     flag=line_draw.backorfront(pos[0],pos[1],pos[2],x1,y1,z1,x0,y0,z0)
#     if stx>=0 and stx<=2*mousex0 and sty>=0 and sty <=2*mousey0 and flag:
#         pygame.draw.rect(screen, (0, 0, 255), (stx-5, sty-5, 10, 10))
#
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
#                 x0=1891
#                 y0=764
#                 z0=300
#             elif event.key==pygame.K_ESCAPE:
#                 gamegoing=False
#             elif event.key==pygame.K_q:
#                 [newx1, newy1, newz1] = postrans(0, 0, 0, scl, 1 * mousex0, 1 * mousey0, x1, y1, z1)
#                 r = line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#                 x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             elif event.key==pygame.K_e:
#                 [newx1, newy1, newz1] = postrans(0, 0, 0, scl, -1 * mousex0, 1 * mousey0, x1, y1, z1)
#                 r = line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#                 x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             elif event.key==pygame.K_z:
#                 [newx1, newy1, newz1] = postrans(0, 0, 0, scl, 1 * mousex0, -1 * mousey0, x1, y1, z1)
#                 r =line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#                 x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
#             elif event.key==pygame.K_c:
#                 [newx1, newy1, newz1] = postrans(0, 0, 0, scl, -1 * mousex0, -1 * mousey0, x1, y1, z1)
#                 r = line_draw.sqr(newx1 ** 2 + newy1 ** 2 + newz1 ** 2)
#                 x1 = newx1 / r;y1 = newy1 / r;z1 = newz1 / r;
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
#
#
#     r=line_draw.sqr(x1**2+y1**2)
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
#
# pygame.quit()#及时退出game模块好习惯