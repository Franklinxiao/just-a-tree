import pygame#引入game模块
pygame.init()

screen=pygame.display.set_mode((1000,600))#开拓长为1000，宽为600的窗口
pygame.display.set_caption("搞搞颜色")#设定窗口的标题
timer=pygame.time.Clock()
serchx = 10
serchy = 10
point_id=[0,0]
choose_point=[0,0]
choose_flag=False
w_kd=False
s_kd=False

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
                            return [xcal,ycal]
                        else:
                            pass
                    else:
                        pass
                else:

                    ycal=(o[0]-i[0])*k1+i[1]
                    if ycal > min([o[1], k[1]]) and ycal < max([o[1], k[1]]) and ycal>min([i[1],j[1]]) and ycal<max([i[1],j[1]]): # 如果交点均在两条线段范围内
                        xcal = o[0]
                        return [xcal, ycal]


        else:#第一段线段是竖直的，特殊情况特殊处理

            for b_index in range(len2):  # 遍历第二个多边形的所有线段
                o = d2[b_index]
                k = d2[(b_index + 1) % len2]

                if o[0] != k[0]:  # 第二个直线不是竖直的，因此斜率存在
                    k2 = (k[1] - o[1]) / (k[0] - o[0])


                    ycal = k2*(i[0]-o[0])+o[1]  # 先求出虚拟的交点
                    xcal = i[0]
                    if ycal > min([i[1],j[1]]) and ycal < max([i[1], j[1]]) and xcal > min([o[0],k[0]]) and xcal < max([o[0], k[0]]) :  # 如果交点均在两条线段范围内

                        return [xcal, ycal]
                    else:
                        pass

                else:
                    pass

    return 0

def draw_input_line(d,color):

    for i in range(len(d)):
        pygame.draw.line(screen,color,(d[i][0],d[i][1]),(d[(i+1)%len(d)][0],d[(i+1)%len(d)][1]),1)

def draw_big_point(d,color):
    if d!=0:
        pygame.draw.polygon(screen, color, [(d[0]-5,d[1]-5),(d[0]+5,d[1]-5),(d[0]+5,d[1]+5),(d[0]-5,d[1]+5)], 0)

def shows(draw_string,pos):#显示操作提示语句
    game_font = pygame.font.SysFont("SimHei", 30)

    text = game_font.render(draw_string ,False, (255, 255, 0))

    #text = font.render(draw_string, True, (255,255,0))  # 丰富框架font里除了字体、大小的其他信息：具体文本，和颜色。
    screen.blit( text,pos)  # 语法：其中text,为文本，后面为位置


def eyeopen():
    screen.fill((0,0,0))
    draw_input_line(d1, (255, 0, 0))
    draw_input_line(d2, (0, 255, 0))
    if choose_flag:
        draw_big_point(choose_point,(0,0,255))
    ans = seek_for_one_intersection_point(d1, d2)
    draw_big_point(ans, (255, 255, 0))


d1=[[200,200],[300,200],[300,500],[200,500]]

d2=[[150,300],[650,300],[650,550],[150,550]]

eyeopen()

#shows('按A D切换主色,按W S改变主色值,鼠标点击选色',(10,550))

gamegoing=True
while gamegoing:#在游戏进行当中

    #screen.fill((0, 0, 0))  # 重新让整个屏幕变黑，防止运动的图像留下残影

    for event in pygame.event.get():#遍历所有捕捉到的事件
        if event.type==pygame.QUIT:#按X按钮退出
            gamegoing=False
        if event.type == pygame.KEYDOWN:

            if event.key==pygame.K_w:
                w_kd = True
                pass
            elif event.key==pygame.K_s:
                s_kd=True
                pass
            elif event.key==pygame.K_a:
                pass
            elif event.key==pygame.K_d:
                pass
            elif event.key==pygame.K_ESCAPE:
                gamegoing=False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # 表示松开了w键
                w_kd = False
            elif event.key == pygame.K_s:
                s_kd = False

        if event.type==pygame.MOUSEBUTTONDOWN:#点击选中点

            mousepos = pygame.mouse.get_pos()
            mousex0 = mousepos[0];
            mousey0 = mousepos[1]
            if  not choose_flag:
                point_id=0
                for i in d1:
                    if i[0]>=mousex0-serchx and i[0]<=mousex0+serchx  and  i[1]>=mousey0-serchy  and i[1]<=mousey0+serchy:
                        point_id=[1,d1.index(i)]
                        choose_point=i
                        choose_flag=True
                        break
                
                for i in d2:
                    if i[0]>=mousex0-serchx and i[0]<=mousex0+serchx  and  i[1]>=mousey0-serchy  and i[1]<=mousey0+serchy:
                        point_id=[2,d2.index(i)]
                        choose_point=i
                        choose_flag=True
                        break

            else:
                if point_id[0]==1:
                    d1[point_id[1]]=[mousex0,mousey0]
                elif point_id[0]==2:
                    d2[point_id[1]] = [mousex0, mousey0]

                point_id=[0,0]
                choose_point=[0,0]
                choose_flag=False

            eyeopen()
    if w_kd:
        pass
    if s_kd:
        pass

    pygame.display.update()  # 更新显示的画面
    timer.tick(50)  # 表示每秒播放50帧
pygame.quit()  # 及时退出game模块好习惯