import time
import pygame
import ctypes
import data

#b = input("启用AutoPlay？ 留空关闭，输入1启用")
#c = input("谱面流速? 200 - 5000")
#d = input("选择谱面 1/2/3/4")
b = False
c = 2200
pumian1 = data.wasuru
#设置是否全屏
isFullScreen = True
#全屏下禁用windows缩放影响
if isFullScreen:
    ctypes.windll.user32.SetProcessDPIAware()
pygame.init()
#谱面流速
speed = int(c)/1
sound = pygame.mixer.Sound("resources/maps/wasuru/忘れてやらない-instrumental- - 結束バンド.mp3")
font_path = "resources/otf/Furore.otf"
beatSound = pygame.mixer.Sound("resources/audios/normal-hitnormal.wav")
backGroundPic = pygame.image.load("resources/maps/wasuru/BG.png")
hit300o = pygame.image.load("resources/images/hit300.png")
hit300 = pygame.transform.scale(hit300o,(hit300o.get_width()*0.5,hit300o.get_height()*0.5))


#fm = pygame.transform.rotate(fm1, 45)
beatSound.set_volume(0.1)
a = 0

FPS = 400


#自动播放谱面
autoPlay = bool(b)
#非全屏模式下的窗口长宽
winModeWidth= 800
winModeHeight= 800
#音符宽度
noteWidth = 170
#音符高度
noteHeight = 80
#左边缘宽度
edgeWidth = 120
#下边缘高度
edghHeight = 100
#音符间距
gapWidth = 0
#谱面固有延迟,aotoPlay不在正确的位置调这个
level_delay = 45
#设备输入延迟,键盘打击和音乐对不上调这个
device_delay = 45
judg_delay = level_delay+device_delay
#判定容差
judg_tl = 80
#MISS容差
judg_tlmiss = 20

screen_info = pygame.display.Info()
#遮罩不透明度
mask_alpha1 = 190
mask_alpha2 = 150

#自定义事件

#aotoPlay下的按键特效消失事件
RESET_I_EVENT1 = pygame.USEREVENT + 1
RESET_I_EVENT2 = pygame.USEREVENT + 2
RESET_I_EVENT3 = pygame.USEREVENT + 3
RESET_I_EVENT4 = pygame.USEREVENT + 4
#设置全局变量屏幕参数方便取用
if(isFullScreen):     
     screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
     #pygame.HWSURFACE
     scHeight = screen_info.current_h
     scWidth = screen_info.current_w
else:
    screen = pygame.display.set_mode((winModeWidth,winModeHeight))
    scHeight = winModeHeight
    scWidth = winModeWidth
pygame.display.set_caption("忘れてやらない-instrumental- - 結束バンド")

#获取屏幕参数

#scHeight = screen_info.current_h
#scWidth = screen_info.current_w
sl = pygame.image.load("resources/images/mania-stage-left.png")
sr = pygame.image.load("resources/images/mania-stage-right.png")
ori_beatLight = pygame.image.load("resources/images/mania-stage-light.png")
sideLeft_img = pygame.transform.scale(sl,(sl.get_width(),scHeight))
sideRight_img = pygame.transform.scale(sr,(sr.get_width(),scHeight))
#beatLight_img = pygame.transform.scale(ori_beatLight,(noteWidth+gapWidth,ori_beatLight.get_height()))
beatLight_img = pygame.transform.scale(ori_beatLight,(noteWidth+gapWidth,(scHeight-edghHeight)*(5/6)))
 

BLACK = (0, 0, 0)
isPlayMusic = False
class ComboCounter(pygame.sprite.Sprite):
    text = ""
    count = 0
    font = pygame.font.Font(font_path, 99)
    position = None
    def __init__(self, text, position):
        super().__init__()
        self.position = position
        self.text = text        
        self.image = self.font.render(text, True, (225,225,0))  
        self.rect = self.image.get_rect(center=position) 
    def update(self):
        
        if(self.count == 0):
            self.text = " "
            self.image = self.font.render(self.text, True, (225,225,0))        
        else:
            self.text = str(self.count)
            self.image = self.font.render(self.text, True, (225,225,0))
        self.rect = self.image.get_rect(center=self.position)
# class BeatLight(pygame.sprite.Sprite):
#     isDisPlay = False
#     def __init__(self, image, speed,position):
#         super().__init__()
#         self.original_image = image
#         self.original_image_width = self.original_image.get_width()
#         self.original_image_height = self.original_image.get_height()
#         self.vis_rect = pygame.Rect(0, self.original_image_height, 0, 0)        
#         self.image = self.original_image.subsurface(self.vis_rect) 
#         self.rect = self.original_image.get_rect()      
#         self.speed = speed
#         self.visible_height = 0
#         # 设置精灵的位置，使矩形下边缘的中点为指定坐标
#         self.position = position
#         self.rect.midbottom = position

#     def update(self):
#      if self.isDisPlay:
#         if self.visible_height < self.original_image_height:
#             self.visible_height += self.speed*dt
#         else:
#             self.visible_height = self.original_image_height

#      else:
#         self.visible_height = 0
                

        
#      #self.rect.midbottom = self.position
#      if self.visible_height < self.original_image_height:
#       self.vis_rect = pygame.Rect(0,self.original_image_height-self.visible_height,self.original_image_width,self.visible_height)
#       self.image = self.original_image.subsurface(self.vis_rect)
#      else:
#         self.image = self.original_image
#      self.rect = self.image.get_rect()
#      self.rect.midbottom = self.position

#按下按键时的特效,有一个从下往上的动画
class BeatLight(pygame.sprite.Sprite):
    isDisPlay = False

    def __init__(self, image, speed, position):
        super().__init__()
        self.original_image = image
        self.original_image_width = self.original_image.get_width()
        self.original_image_height = self.original_image.get_height()
        self.image_segments = []  # 存储子图像列表
        self.create_image_segments()
        self.rect = self.original_image.get_rect()
        self.speed = speed
        self.visible_height = 0
        self.position = position
        self.rect.midbottom = position

    def create_image_segments(self):
        for h in range(self.original_image_height):
            rect = pygame.Rect(0, self.original_image_height - h, self.original_image_width, h)
            self.image_segments.append(self.original_image.subsurface(rect))

    def update(self):
        if self.isDisPlay:
            if self.visible_height < self.original_image_height:
                self.visible_height += self.speed * dt
            else:
                self.visible_height = self.original_image_height
        else:
            self.visible_height = 0

        segment_index = int(self.visible_height)  # 根据可见高度选择子图像
        if segment_index < len(self.image_segments):
            self.image = self.image_segments[segment_index]
        else:
            self.image = self.original_image

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.position


class ScoreFX(pygame.sprite.Sprite):
    def __init__(self, image, position, scoreFxList):
        super().__init__()
        if scoreFxList:
            s = scoreFxList[0]
            scoreFxList.pop(0)
            s.kill()
        self.position = position
        self.og_image = image        
        self.image = self.og_image
        self.rect = self.image.get_rect(center=position)
        self.scale_factor = 1.0
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        scoreFxList.append(self)

    def update(self):
        self.scalSelf()

    def scalSelf(self):
        self.scale_factor += 1.9*dt 
        new_width = int(self.original_width * self.scale_factor)
        new_height = int(self.original_height * self.scale_factor)
        self.image = pygame.transform.scale(self.og_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.position)
        
        # 删除自身条件
        if new_width > self.original_width * 1.2:
            self.kill()



    
    
        
    
class Note(pygame.sprite.Sprite):
    af = 255
    ismove = True
    fading = False
    timing = 0
    playBeatSound = True
    isMiss = True
    dd = True
    fadeSpeed = 255000000000/1
    line = []
    def __init__(self,order,timing):
        super().__init__()
        self.order = order
        self.timing = timing
        self.image = pygame.Surface((noteWidth, noteHeight))
        if(order==1 or order ==4):
            self.image.fill((72,209,204))
        else:
            self.image.fill((224,255,255))
        self.rect = self.image.get_rect()
        
        if(order==1):
            self.rect.x=edgeWidth
        if(order==2):
            self.rect.x=edgeWidth+noteWidth+gapWidth
        if(order==3):
            self.rect.x=edgeWidth+noteWidth+gapWidth+noteWidth+gapWidth
        if(order==4):
            self.rect.x=edgeWidth+noteWidth+gapWidth+noteWidth+gapWidth+noteWidth+gapWidth
    def update(self):
        
        if(self.ismove):
            #这种写法比下面的时间准确度更高,性能没考究不知道如何
            self.rect.y =  scHeight-edghHeight-noteHeight-(speed/1000)*(self.timing+level_delay-pmTime)
            #self.rect.y += speed*dt      
        if(self.fading):
            
            if(self.af<=0):
                self.kill()
            self.image.set_alpha(self.af)
            self.af-=255          
        if(autoPlay):
            if(self.timing+level_delay<pmTime):
                #self.fadeSpeed = 200000000000/1
                
                if(self.dd):
                    self.deter(False)
                    comboCounter.count+=1
                    beatSound.play()
                    #显示""300"
                    scoreFX = ScoreFX(hit300,(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight*(6/10)),scoreFxList)
                    scoreFxList.append(scoreFX)
                    upfx_group2.add(scoreFX)
                    #显示按键条
                    if(self.order == 1):
                        beatLight1.isDisPlay = True
                        pygame.time.set_timer(RESET_I_EVENT1, 100)
                    if(self.order == 2):
                        beatLight2.isDisPlay = True
                        pygame.time.set_timer(RESET_I_EVENT2, 100)
                    if(self.order == 3):
                        beatLight3.isDisPlay = True
                        pygame.time.set_timer(RESET_I_EVENT3, 100)
                    if self.order == 4:
                        beatLight4.isDisPlay = True
                        pygame.time.set_timer(RESET_I_EVENT4, 100)

                    self.playBeatSound=False
        else:
            if(self.timing+judg_delay+judg_tl<pmTime and self.isMiss):
                if(self.dd):
                    self.line.pop(0)
                    comboCounter.count = 0
                #self.fadeSpeed = 2000/1
                
                self.deter(True)
                self.ismove = True
                self.playBeatSound = False
                #print(self.line)
                


    def deter(self,miss):
        if(self.playBeatSound and (not miss)):
                    beatSound.play()
                    self.playBeatSound=False
        self.dd = False
        self.isMiss = miss
        self.ismove = False
        self.fading = True

my_group = pygame.sprite.Group()
downfx_group = pygame.sprite.Group()
upfx_group = pygame.sprite.Group()
upfx_group2 = pygame.sprite.Group()
clock = pygame.time.Clock()
beatLight1 = BeatLight(beatLight_img,11000,(edgeWidth+noteWidth/2,scHeight-edghHeight))
beatLight2 = BeatLight(beatLight_img,11000,(edgeWidth+noteWidth+gapWidth+noteWidth/2,scHeight-edghHeight))
beatLight3 = BeatLight(beatLight_img,11000,(edgeWidth+noteWidth+gapWidth+noteWidth+gapWidth+noteWidth/2,scHeight-edghHeight))
beatLight4 = BeatLight(beatLight_img,11000,(edgeWidth+noteWidth+gapWidth+noteWidth+gapWidth+noteWidth+gapWidth+noteWidth/2,scHeight-edghHeight))
downfx_group.add(beatLight1,beatLight2,beatLight3,beatLight4)
running = True
#print(pumian1[a][0])

#prev_time = pygame.time.get_ticks()
line1 = []
line2 = []
line3 = []
line4 = []
scoreFxList = []
#加载谱面
for note in pumian1:
    n = Note(note[1],note[0])
    n.rect.y =  scHeight-edghHeight-noteHeight-(speed/1000)*(note[0]+judg_delay)
    if(note[1]==1):
        line1.append((n,note[0]))
        n.line = line1
    if(note[1]==2):
        line2.append((n,note[0]))
        n.line = line2
    if(note[1]==3):
        line3.append((n,note[0]))
        n.line = line3
    if(note[1]==4):
        line4.append((n,note[0]))
        n.line = line4
    my_group.add(n)
comboCounter = ComboCounter(" ",(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight/4))
upfx_group.add(comboCounter)
pmStartTime = 0
loadTime = 0    
def draw_line():
    pygame.draw.line(screen, (255,0,0), (0, scHeight - 1-edghHeight), (scWidth - 1, scHeight - 1-edghHeight), 5)
    pygame.draw.line(screen, (255,64,0), (0, scHeight - 1-edghHeight), (scWidth - 1, scHeight - 1-edghHeight), 2)
    #pygame.draw.line(screen, (255,64,0), (0, scHeight - 1-edghHeight), (scWidth - 1, scHeight - 1-edghHeight), 2)
def drawPic(fm,x,y):
    fm_rc = fm.get_rect()
    fm_rc.x = x
    fm_rc.y = y
    screen.blit(fm,fm_rc)
#加载初始画面,可以放些别的东西
def initSc():              
        screen.fill((255,255,255))
        my_group.draw(screen)
        pygame.display.flip()        
        return pygame.time.get_ticks()
class Mytools:
    #图像快速转变为背景图像,保证覆盖全荧幕
    @staticmethod 
    def  image2BG(image,screenWidth,screenHeight):
    
     image_width, image_height = image.get_size()

     # 计算缩放比例
     scale_width = screenWidth / image_width
     scale_height = screenHeight / image_height
     scale = max(scale_width, scale_height)

      #缩放
     scaled_width = int(image_width * scale)
     scaled_height = int(image_height * scale)
     scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

      #居中
     x = (screenWidth - scaled_width) // 2
     y = (screenHeight - scaled_height) // 2
     return (scaled_image,x,y)
backGround = Mytools.image2BG(backGroundPic,scWidth,scHeight)
mask1 = Mytools.image2BG(pygame.Surface((100,100)),scWidth,scHeight)
mask1[0].fill(BLACK)
mask1[0].set_alpha(mask_alpha1)
mask2 = pygame.Surface(((4*noteWidth+3*gapWidth),scHeight+10))
mask2.fill(BLACK)
mask2.set_alpha(mask_alpha2)
loadTime = initSc()
    



while running:
    pygame.event.get_keyboard_grab()
    #事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                print("游戏关闭")
                running = False
        if event.type == pygame.KEYDOWN:         
            if event.key == pygame.K_j:
                #print("J键按下")
                #print(line3[0][1])
                #print(pmTime)
                if(line3 and (line3[0][1]+judg_tl+judg_delay)>pmTime and (line3[0][1]-judg_tlmiss)<pmTime):
                   line3[0][0].deter(False)
                   comboCounter.count+=1
                   line3.pop(0)
                   scoreFX = ScoreFX(hit300,(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight*(6/10)),scoreFxList)
                   scoreFxList.append(scoreFX)
                   upfx_group2.add(scoreFX)
            if event.key == pygame.K_k:
                #print("K按下")
                if(line4 and (line4[0][1]+judg_tl+judg_delay)>pmTime and (line4[0][1]-judg_tlmiss)<pmTime):
                   line4[0][0].deter(False)
                   comboCounter.count+=1
                   line4.pop(0)
                   scoreFX = ScoreFX(hit300,(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight*(6/10)),scoreFxList)
                   scoreFxList.append(scoreFX)
                   upfx_group2.add(scoreFX)
            if event.key == pygame.K_d:
               # print("D按下")
                if(line1 and (line1[0][1]+judg_tl+judg_delay)>pmTime and (line1[0][1]-judg_tlmiss)<pmTime):
                   line1[0][0].deter(False)
                   comboCounter.count+=1
                   line1.pop(0)
                   scoreFX = ScoreFX(hit300,(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight*(6/10)),scoreFxList)
                   scoreFxList.append(scoreFX)
                   upfx_group2.add(scoreFX)
            if event.key == pygame.K_f:
               # print("F按下")
                if(line2 and (line2[0][1]+judg_tl+judg_delay)>pmTime and (line2[0][1]-judg_tl)<pmTime):
                   line2[0][0].deter(False)
                   comboCounter.count+=1
                   line2.pop(0)
                   scoreFX = ScoreFX(hit300,(edgeWidth+2*noteWidth+gapWidth+(1/2)*gapWidth,scHeight*(6/10)),scoreFxList)
                   scoreFxList.append(scoreFX)
                   upfx_group2.add(scoreFX)
            if event.key == pygame.K_q:
                running = False
        if event.type == RESET_I_EVENT1:
            beatLight1.isDisPlay = False
            pygame.time.set_timer(RESET_I_EVENT1,0)
        if event.type == RESET_I_EVENT2:
            beatLight2.isDisPlay = False
            pygame.time.set_timer(RESET_I_EVENT2,0)

        if event.type == RESET_I_EVENT3:
            beatLight3.isDisPlay = False
            pygame.time.set_timer(RESET_I_EVENT3,0)
        if event.type == RESET_I_EVENT4:
            beatLight4.isDisPlay = False
            pygame.time.set_timer(RESET_I_EVENT4,0)
    if(not autoPlay):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
           beatLight1.isDisPlay = True
        else:
           beatLight1.isDisPlay = False
        if keys[pygame.K_f]:
           beatLight2.isDisPlay = True
        else:
           beatLight2.isDisPlay = False
        if keys[pygame.K_j]:
           beatLight3.isDisPlay = True
        else:
           beatLight3.isDisPlay = False
        if keys[pygame.K_k]:
           beatLight4.isDisPlay = True
        else:
           beatLight4.isDisPlay = False
    #print("pmstarttime:"+ str(pmStartTime))        
    pmTime = pygame.time.get_ticks()-pmStartTime
    #current_time = pygame.time.get_ticks()
    #prev_time = current_time
    # 三秒后再进行其他的逻辑     
    if(pygame.time.get_ticks()-loadTime>3000):
        if(not isPlayMusic):
            sound.play()
            isPlayMusic = True
    # 绘制背景 
        screen.fill((0, 0, 0))
        drawPic(backGround[0],backGround[1],backGround[2])
        drawPic(mask1[0],mask1[1],mask1[2])        
        drawPic(mask2,edgeWidth,-10)
        drawPic(sideLeft_img,edgeWidth-sideLeft_img.get_width(),0)
        drawPic(sideRight_img,edgeWidth+4*noteWidth+3*gapWidth,0)
        upfx_group.update()
        my_group.update()
        upfx_group2.update()
        downfx_group.update()
    # 绘制精灵   
        downfx_group.draw(screen)
        my_group.draw(screen)
        upfx_group.draw(screen)
        upfx_group2.draw(screen)
    #画线
        draw_line()
    # 更新窗口
        pygame.display.update()
    else:
        pmStartTime = pygame.time.get_ticks()
    # 控制游戏帧率
    dt = clock.tick(FPS)/ 1000.0
    

pygame.quit()
#input()
