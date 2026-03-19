
import pygame
import sys
#
# (width, height) = (800, 600)
# pygame.init()
# screen = pygame.display.set_mode((width, height))
# screen.fill((255,255,255))
#
#
# image = pygame.image.load("C:\\Users\\Franklinxiao\\pythonProject1\\书法鉴赏作业\\反色合文.jpg").convert()
# # image1 = pygame.image.load("1.jpg").convert()
# d3=pygame.surfarray.array3d(image)
# f=250#数字大会显示更前面的图片
# sc=300#数字越大视角越高
# color=(255, 255, 255)
# sarray=pygame.surfarray.array3d(pygame.Surface((width,height)))
#
# tsize=image.get_size()#图片宽高
# # tsize1=image1.get_size()#图片宽高
# print(tsize)
scl=1000
# people_pos=[-100,0,0]
# sight=[1,0,0]
# img_3D_cornor_series=[[50,50,100],[-50,50,300],[-50,-50,300],[50,-50,100]]
# #real [[100,-100,50],[200,100,50],[]]
#
mousex0=500
mousey0=300




def sqr(a):
    return  a**0.5

#输入x2、y2、z2为客观空间的坐标，x1,y1,z1为视角的方向向量, 输出该点在屏幕上的横坐标
def stchx(x2,y2,z2,x1,y1,z1,x0,y0,z0):
    cos1 = (x1 * (x2 - x0) + y1 * (y2 - y0) + z1 * (z2 - z0))#*(1.17-0.8*z1)
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

def transform(img_x, img_y, screen_conor_pos_series, picture_size):
    #screen_center_pos=cal_lines_intersection(screen_conor_pos_series)
    p1=screen_conor_pos_series[0]
    p2=screen_conor_pos_series[1]
    p3=screen_conor_pos_series[2]
    p4=screen_conor_pos_series[3]

    #screen_center_pos=[(p1[0]+p2[0]+p3[0]+p4[0])/4,(p1[1]+p2[1]+p3[1]+p4[1])/4]
    #k=tsize[1]/tsize[0]
    bili1=(img_x-0)/picture_size[0]
    bili2=(img_y-0)/picture_size[1]
    ax1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    ax2 = [p4[0] - p1[0], p4[1] - p1[1], p4[2] - p1[2]]

    return p1[0] + bili1 * ax1[0] + bili2 * ax2[0], p1[1] + bili1 * ax1[1] + bili2 * ax2[1], p1[2] + bili1 * ax1[
        2] + bili2 * ax2[2]

def img_load(image,img_3D_cornor_series,sight,people_pos,screen):
    #
    tsize=image.get_size()


    x_boundary=screen.get_width()
    y_boundary=screen.get_height()
    # p1=img_3D_cornor_series[0]
    # p2=img_3D_cornor_series[1]
    # p3=img_3D_cornor_series[2]
    # p4=img_3D_cornor_series[3]
    #
    # p1sx=stchx(p1[2],p1[0],p1[1],sight[0],sight[1],sight[2],people_pos[0],people_pos[1],people_pos[2])
    # p1sy=stchy(p1[2],p1[0],p1[1],sight[0],sight[1],sight[2],people_pos[0],people_pos[1],people_pos[2])
    #
    # p2sx = stchx(p2[2], p2[0], p2[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    # p2sy = stchy(p2[2], p2[0], p2[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    #
    # p3sx = stchx(p3[2], p3[0], p3[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    # p3sy = stchy(p3[2], p3[0], p3[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    #
    # p4sx = stchx(p4[2], p4[0], p4[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    # p4sy = stchy(p4[2], p4[0], p4[1], sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    #
    #
    #
    # stepx=tsize[0]/max(abs(p2sx-p1sx),abs(p3sx-p2sx),abs(p4sx-p3sx),abs(p1sx-p4sx))
    # stepy =tsize[1]/max(abs(p2sy-p1sy),abs(p3sy-p2sy),abs(p4sy-p3sy),abs(p1sy-p4sy))

    stepx=4
    stepy=4

    # print(stepx, stepy)
    #
    # setx, sety = transform(0, 0, img_3D_cornor_series, tsize)
    # setx, sety, setz = two2three(setx, sety, img_3D_cornor_series)
    # tempx = stchx(setz, setx, sety, sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    # tempy = stchy(setz, setx, sety, sight[0], sight[1], sight[2], people_pos[0], people_pos[1], people_pos[2])
    i = 0;
    cnt=0
    while i <tsize[0]:
        j = 0;
        while j <tsize[1]:
            fp=int(i),int(j)
            setx,sety,setz=transform(i,j,img_3D_cornor_series,tsize)

            drawx=stchx(setx,sety,setz,sight[0],sight[1],sight[2],people_pos[0],people_pos[1],people_pos[2])
            drawy=stchy(setx,sety,setz,sight[0],sight[1],sight[2],people_pos[0],people_pos[1],people_pos[2])

            if drawx>0 and drawx<x_boundary and drawy>0 and drawy< y_boundary :
                pygame.Surface.set_at(screen, (int(drawx), int(drawy)), image.get_at(fp))

            # pygame.Surface.set_at(screen, (int(drawx), int(drawy)), (255,0,0))

            j+=stepy
            cnt+=1

            # if cnt%500==0:
            #      print("painting...",setx,sety,setz,drawx,drawy)

        i+=stepx

