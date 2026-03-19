import pygame#引入game模块
pygame.init()

screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
pygame.display.set_caption("搞搞颜色")#设定窗口的标题
timer=pygame.time.Clock()

#绘制参数
R=200;
G=128;
B=128;

r=0
g=0
b=0

font = pygame.font.SysFont("Times", 24)#设定文字的字体和大小，并赋予到font框架里

#控制参数
switch_pos=0
startx=30
starty=30
dx = 2;
dy = 2;
w_kd=False
s_kd=False

def fill_pre_select():
    pygame.draw.polygon(screen, (255, 0, 0), [(700, 400), (900, 400), (900, 450), (700, 450)])

    if switch_pos==0:
        for i in range(256):
            for j in range(256):
                pygame.draw.polygon(screen, (R, i, j),
                                    [(startx + i * dx, starty + j * dy), (startx + (i + 1) * dx, starty + j * dy),
                                     (startx + (i + 1) * dx, starty + (j + 1) * dy),
                                     (startx + i * dx, starty + (j + 1) * dy)])



        shows('R:'+str(R),(700,400))

    elif switch_pos==1:
        for i in range(256):
            for j in range(256):
                pygame.draw.polygon(screen, (i,G , j),
                                    [(startx + i * dx, starty + j * dy), (startx + (i + 1) * dx, starty + j * dy),
                                     (startx + (i + 1) * dx, starty + (j + 1) * dy),
                                     (startx + i * dx, starty + (j + 1) * dy)])
        shows('G:' + str(G), (700, 400))

    elif switch_pos==2:
        for i in range(256):
            for j in range(256):
                pygame.draw.polygon(screen, ( i, j,B),
                                    [(startx + i * dx, starty + j * dy), (startx + (i + 1) * dx, starty + j * dy),
                                     (startx + (i + 1) * dx, starty + (j + 1) * dy),
                                     (startx + i * dx, starty + (j + 1) * dy)])
        shows('B:' + str(B), (700, 400))

def fill_after_select(r,g,b):
    pygame.draw.polygon(screen, (r,g,b),
                        [(700,100),(800,100),(800,200),(700,200)])

def shows(draw_string,pos):#显示操作提示语句
    game_font = pygame.font.SysFont("SimHei", 30)

    text = game_font.render(draw_string ,False, (255, 255, 0))

    #text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置



fill_pre_select()
shows('按A D切换主色,按W S改变主色值,鼠标点击选色',(10,550))

gamegoing=True
while gamegoing:#在游戏进行当中

    #screen.fill((0, 0, 0))  # 重新让整个屏幕变黑，防止运动的图像留下残影

    for event in pygame.event.get():#遍历所有捕捉到的事件
        if event.type==pygame.QUIT:#按X按钮退出
            gamegoing=False
        if event.type == pygame.KEYDOWN:

            if event.key==pygame.K_w:
                if switch_pos==0:
                    R=(R+1)%256
                elif switch_pos==1:
                    G = (G + 1) % 256
                elif switch_pos==2:
                    B = (B + 1) % 256
                w_kd = True
            elif event.key==pygame.K_s:
                if switch_pos==0:
                    R=(R+256-1)%256
                elif switch_pos==1:
                    G = (G + 256-1) % 256
                elif switch_pos==2:
                    B = (B + 256-1) % 256
                s_kd=True
            elif event.key==pygame.K_a:
                switch_pos=(switch_pos+3-1)%3
            elif event.key==pygame.K_d:
                switch_pos = (switch_pos+1) % 3
            elif event.key==pygame.K_ESCAPE:
                gamegoing=False
            fill_pre_select()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # 表示松开了w键
                w_kd = False
            elif event.key == pygame.K_s:
                s_kd = False

        if event.type==pygame.MOUSEBUTTONDOWN:#点击取色
            mousepos=pygame.mouse.get_pos()
            if  mousepos[0]>=startx  and mousepos[1]>=starty and mousepos[0]<=startx+255*dx and mousepos[1]<=starty+255*dy  :
                if switch_pos==0:
                    r=R
                    g=int((mousepos[0]-startx)/dx)
                    b = int((mousepos[1] - starty) / dy)

                if switch_pos==1:
                    g=G
                    r = int((mousepos[0] - startx) / dx)
                    b = int((mousepos[1] - starty) / dy)

                if switch_pos==2:
                    b=B
                    r = int((mousepos[0] - startx) / dx)
                    g = int((mousepos[1] - starty) / dy)

            fill_after_select(r,g,b)

            pygame.draw.polygon(screen,(0,0,255),[(700,300),(950,300),(950,350),(700,350)])
            shows(str([r,g,b]),(700,300))

            #print(mousepos)

    if w_kd:
        if switch_pos == 0:
            R = (R + 5) % 256
        elif switch_pos == 1:
            G = (G + 5) % 256
        elif switch_pos == 2:
            B = (B + 5) % 256
        fill_pre_select()
    if s_kd:
        if switch_pos == 0:
            R = (R + 256 - 5) % 256
        elif switch_pos == 1:
            G = (G + 256 - 5) % 256
        elif switch_pos == 2:
            B = (B + 256 - 5) % 256
        fill_pre_select()

    pygame.display.update()  # 更新显示的画面
    timer.tick(50)  # 表示每秒播放50帧
pygame.quit()  # 及时退出game模块好习惯