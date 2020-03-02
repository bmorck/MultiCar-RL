#initialize the screen
import pygame, math, sys, time
from pygame.locals import *
import math

pygame.init()
screen = pygame.display.set_mode((1024, 768))
screen.fill([128, 128, 128])
pygame.display.update()
#GAME CLOCK
clock = pygame.time.Clock()
font = pygame.font.Font(None, 75)
win_font = pygame.font.Font(None, 50)
win_condition = None
win_text = font.render('', True, (0, 255, 0))
loss_text = font.render('', True, (255, 0, 0))
#pygame.mixer.music.load('My_Life_Be_Like.mp3')
t0 = time.time()
rect = screen.get_rect()






class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 10

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        x, y = (self.position)
        self.rect = pygame.Rect(self.src_image.get_rect())
        

    
    def update(self, deltat):
        #SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = (self.position)
        rad = self.direction * math.pi / 180
        velocity_x = -self.speed*math.sin(rad)
        velocity_y = -self.speed*math.cos(rad)
        x += velocity_x
        y += velocity_y
        x_c = x
        y_c = y
        self.position = (x, y)

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        pygame.draw.rect(screen, (255, 255, 0), self.rect, width=2)



class SensorSprite(pygame.sprite.Sprite):
    xpos = 0
    ypos = 0
    xnew = 0
    ynew = 0
    obj = None

    def __init__(self, x_pos, y_pos, obj):
        self.xpos = x_pos
        self.ypos = y_pos
        self.xnew = obj.rect.centerx + x_pos
        self.ynew = obj.rect.centery + y_pos
        self.obj = obj
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.draw.line(screen,(255,0,0),(obj.rect.centerx, obj.rect.centery), (self.xnew, obj.rect.centery + y_pos), width=5)
    def update(self):

        rad = -self.obj.direction * math.pi / 180
        s = math.sin(rad);
        c = math.cos(rad);
        x = self.obj.rect.centerx
        y = self.obj.rect.centery

        xnew = c*(self.xpos) - s *(self.ypos) + x
        ynew = s*(self.xpos) + c *(self.ypos) + y

        self.rect = pygame.draw.line(screen,(255, 0, 0),(x, y),(xnew, ynew), width=2)



class PadSprite(pygame.sprite.Sprite):
    normal = None
    #hit = pygame.image.load('images/collision.png')
    def __init__(self, position, image):
        self.normal = pygame.image.load(image)
        super(PadSprite, self).__init__()
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
    def update(self, hit_list):
        if self in hit_list: 
            #self.image = self.hit
            self.position = (50, 50)
        else: self.image = self.normal
pads = [
    PadSprite((50, 50), 'images/pad_vert.png'),
    PadSprite((50, 100), 'images/pad_vert.png'),
    PadSprite((50, 150), 'images/pad_vert.png'),
    PadSprite((50, 200), 'images/pad_vert.png'),
    PadSprite((50, 250), 'images/pad_vert.png'),
    PadSprite((50, 300), 'images/pad_vert.png'),
    PadSprite((50, 350), 'images/pad_vert.png'),
    PadSprite((50, 400), 'images/pad_vert.png'),
    PadSprite((50, 450), 'images/pad_vert.png'),
    PadSprite((50, 500), 'images/pad_vert.png'),
    PadSprite((50, 550), 'images/pad_vert.png'),
    PadSprite((50, 600), 'images/pad_vert.png'),
    PadSprite((50, 650), 'images/pad_vert.png'),
    PadSprite((50, 700), 'images/pad_vert.png'),

    PadSprite((160, 150), 'images/pad_vert.png'),
    PadSprite((160, 200), 'images/pad_vert.png'),
    PadSprite((160, 250), 'images/pad_vert.png'),
    PadSprite((160, 300), 'images/pad_vert.png'),
    PadSprite((160, 350), 'images/pad_vert.png'),
    PadSprite((160, 400), 'images/pad_vert.png'),
    PadSprite((160, 450), 'images/pad_vert.png'),
    PadSprite((160, 500), 'images/pad_vert.png'),
    PadSprite((160, 550), 'images/pad_vert.png'),
    PadSprite((160, 600), 'images/pad_vert.png'),

    PadSprite((75, 32), 'images/pad_horiz.png'),
    PadSprite((125, 32), 'images/pad_horiz.png'),
    PadSprite((175, 32), 'images/pad_horiz.png'),
    PadSprite((225, 32), 'images/pad_horiz.png'),
    PadSprite((275, 32), 'images/pad_horiz.png'),
    PadSprite((325, 32), 'images/pad_horiz.png'),
    PadSprite((375, 32), 'images/pad_horiz.png'),
    PadSprite((425, 32), 'images/pad_horiz.png'),
    PadSprite((475, 32), 'images/pad_horiz.png'),
    PadSprite((525, 32), 'images/pad_horiz.png'),
    PadSprite((575, 32), 'images/pad_horiz.png'),
    PadSprite((625, 32), 'images/pad_horiz.png'),
    PadSprite((675, 32), 'images/pad_horiz.png'),
    PadSprite((725, 32), 'images/pad_horiz.png'),
    PadSprite((775, 32), 'images/pad_horiz.png'),
    PadSprite((825, 32), 'images/pad_horiz.png'),
    PadSprite((875, 32), 'images/pad_horiz.png'),
    PadSprite((925, 32), 'images/pad_horiz.png'),

    PadSprite((180, 122), 'images/pad_horiz.png'),
    PadSprite((225, 122), 'images/pad_horiz.png'),
    PadSprite((275, 122), 'images/pad_horiz.png'),
    PadSprite((325, 122), 'images/pad_horiz.png'),
    PadSprite((375, 122), 'images/pad_horiz.png'),
    PadSprite((425, 122), 'images/pad_horiz.png'),
    PadSprite((475, 122), 'images/pad_horiz.png'),
    PadSprite((525, 122), 'images/pad_horiz.png'),
    PadSprite((575, 122), 'images/pad_horiz.png'),
    PadSprite((625, 122), 'images/pad_horiz.png'),
    PadSprite((675, 122), 'images/pad_horiz.png'),
    PadSprite((725, 122), 'images/pad_horiz.png'),
    PadSprite((775, 122), 'images/pad_horiz.png'),
    PadSprite((825, 122), 'images/pad_horiz.png'),


    PadSprite((950, 50), 'images/pad_vert.png'),
    PadSprite((950, 100), 'images/pad_vert.png'),
    PadSprite((950, 150), 'images/pad_vert.png'),
    PadSprite((950, 200), 'images/pad_vert.png'),
    PadSprite((950, 250), 'images/pad_vert.png'),
    PadSprite((950, 300), 'images/pad_vert.png'),
    PadSprite((950, 350), 'images/pad_vert.png'),
    PadSprite((950, 400), 'images/pad_vert.png'),
    PadSprite((950, 450), 'images/pad_vert.png'),
    PadSprite((950, 500), 'images/pad_vert.png'),
    PadSprite((950, 550), 'images/pad_vert.png'),
    PadSprite((950, 600), 'images/pad_vert.png'),
    PadSprite((950, 650), 'images/pad_vert.png'),
    PadSprite((950, 700), 'images/pad_vert.png'),


    PadSprite((841, 150), 'images/pad_vert.png'),
    PadSprite((841, 200), 'images/pad_vert.png'),
    PadSprite((841, 250), 'images/pad_vert.png'),
    PadSprite((841, 300), 'images/pad_vert.png'),
    PadSprite((841, 350), 'images/pad_vert.png'),
    PadSprite((841, 400), 'images/pad_vert.png'),
    PadSprite((841, 450), 'images/pad_vert.png'),
    PadSprite((841, 500), 'images/pad_vert.png'),
    PadSprite((841, 550), 'images/pad_vert.png'),
    PadSprite((841, 600), 'images/pad_vert.png'),

    PadSprite((180, 630), 'images/pad_horiz.png'),
    PadSprite((225, 630), 'images/pad_horiz.png'),
    PadSprite((275, 630), 'images/pad_horiz.png'),
    PadSprite((325, 630), 'images/pad_horiz.png'),
    PadSprite((375, 630), 'images/pad_horiz.png'),
    PadSprite((425, 630), 'images/pad_horiz.png'),
    PadSprite((475, 630), 'images/pad_horiz.png'),
    PadSprite((525, 630), 'images/pad_horiz.png'),
    PadSprite((575, 630), 'images/pad_horiz.png'),
    PadSprite((625, 630), 'images/pad_horiz.png'),
    PadSprite((675, 630), 'images/pad_horiz.png'),
    PadSprite((725, 630), 'images/pad_horiz.png'),
    PadSprite((775, 630), 'images/pad_horiz.png'),
    PadSprite((825, 630), 'images/pad_horiz.png'),

    PadSprite((75, 718), 'images/pad_horiz.png'),
    PadSprite((125, 718), 'images/pad_horiz.png'),
    PadSprite((175, 718), 'images/pad_horiz.png'),
    PadSprite((225, 718), 'images/pad_horiz.png'),
    PadSprite((275, 718), 'images/pad_horiz.png'),
    PadSprite((325, 718), 'images/pad_horiz.png'),
    PadSprite((375, 718), 'images/pad_horiz.png'),
    PadSprite((425, 718), 'images/pad_horiz.png'),
    PadSprite((475, 718), 'images/pad_horiz.png'),
    PadSprite((525, 718), 'images/pad_horiz.png'),
    PadSprite((575, 718), 'images/pad_horiz.png'),
    PadSprite((625, 718), 'images/pad_horiz.png'),
    PadSprite((675, 718), 'images/pad_horiz.png'),
    PadSprite((725, 718), 'images/pad_horiz.png'),
    PadSprite((775, 718), 'images/pad_horiz.png'),
    PadSprite((825, 718), 'images/pad_horiz.png'),
    PadSprite((875, 718), 'images/pad_horiz.png'),
    PadSprite((925, 718), 'images/pad_horiz.png')
    
    

  
]
pad_group = pygame.sprite.RenderPlain(*pads)


'''class Trophy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/trophy.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    def draw(self, screen):
        screen.blit(self.image, self.rect)

trophies = [Trophy((285,0))]
trophy_group = pygame.sprite.RenderPlain(*trophies)'''

# CREATE A CAR AND RUN
rect = screen.get_rect()
car = CarSprite('images/car.png', (100, 660))
car2 = CarSprite('images/car.png', (100, 600))
cars = [car, car2]
car_group = pygame.sprite.RenderPlain(*cars)
sensors = [SensorSprite(0, -150, car), 
            SensorSprite(100, -130, car),
            SensorSprite(-100, -130, car), 
            SensorSprite(150, 0, car), 
            SensorSprite(-150, 0, car),
            SensorSprite(0, 150, car),
            SensorSprite(100, 130, car),
            SensorSprite(-100, 130, car),
            SensorSprite(0, -150, car2), 
            SensorSprite(100, -130, car2),
            SensorSprite(-100, -130, car2), 
            SensorSprite(150, 0, car2), 
            SensorSprite(-150, 0, car2),
            SensorSprite(0, 150, car2),
            SensorSprite(100, 130, car2),
            SensorSprite(-100, 130, car2)]
sensor_group = pygame.sprite.RenderPlain(*sensors)

'''WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

mouse_position = (0, 0)
drawing = False
screen.fill(WHITE)
pygame.display.set_caption("ScratchBoard")

last_pos = None
i = 0
while i < 5000:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if last_pos is not None:
                pygame.draw.line(screen, BLACK, last_pos, mouse_position, 3)
            last_pos = mouse_position
    

    pygame.display.update()
    i += 1'''

#THE GAME LOOP
while 1:

    #USER INPUT
    t1 = time.time()
    dt = t1-t0
  
    

    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN 
        if win_condition == None: 
            if event.key == K_RIGHT: 
                car.k_right = down * -10
            elif event.key == K_LEFT: 
                car.k_left = down * 10
            elif event.key == K_UP: car.k_up = down * 2
            elif event.key == K_DOWN: car.k_down = down * -2
            if event.key == K_d: 
                car2.k_right = down * -10
            elif event.key == K_a: 
                car2.k_left = down * 10
            elif event.key == K_w: car2.k_up = down * 2
            elif event.key == K_s: car2.k_down = down * -2  
            elif event.key == K_ESCAPE: sys.exit(0) # quit the game
        elif win_condition == True and event.key == K_SPACE: level2.level2()
        elif win_condition == False and event.key == K_SPACE: 
            #level1()
            t0 = t1
        elif event.key == K_ESCAPE: sys.exit(0)    

    #COUNTDOWN TIMER
    seconds = round((20 - dt),2)
    if win_condition == None:
        timer_text = font.render(str(seconds), True, (255,255,0))
        '''if seconds <= 0:
            win_condition = False
            timer_text = font.render("Time!", True, (255,0,0))
            loss_text = win_font.render('Press Space to Retry', True, (255,0,0))'''
        

    #RENDERING
    screen.fill([128, 128, 128])
    car_group.update(deltat)
    sensor_group.update()
    collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, collided = None)
    #if collisions != {}:
        #win_condition = False
        #timer_text = font.render("Crash!", True, (255,0,0))
        #car.image = pygame.image.load('images/collision.png')
        #loss_text = win_font.render('Press Space to Retry', True, (255,0,0))
        #seconds = 0
        #car.MAX_FORWARD_SPEED = 0
        #car.MAX_REVERSE_SPEED = 0
        #car.k_right = 0
        #car.k_left = 0

    collisions2 = pygame.sprite.groupcollide(sensor_group, pad_group, False, False, collided = None)


    rect_list = []
    # use union rect function
    for key, value in collisions2.items():
        for val in value:
            newrect = val.rect.clip(key.rect)
            rect_list.append(newrect)
            #pygame.draw.rect(screen, (0, 255, 0), key.rect, width=2)
            pygame.draw.rect(screen, (0, 0, 255), [newrect.left, newrect.top, newrect.width, newrect.height], width=5)


    avg_distance = 0
    total_distance = 0
    #print(rect_list)
    for rec in rect_list:
        pygame.draw.rect(screen, (0, 255, 0), rec, width=2)
        total_distance += math.sqrt((rec.centerx - car.rect.centerx) ** 2 + (rec.centery - car.rect.centery) ** 2)
    if len(rect_list) > 0:
        avg_distance = total_distance / len(rect_list)
    else: 
        avg_distance = 0

    pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 15)

   
    textsurface = myfont.render(str(avg_distance), False, (0, 0, 0))

    screen.blit(textsurface,(10,10))


    '''trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
    if trophy_collision != {}:
        seconds = seconds
        timer_text = font.render("Finished!", True, (0,255,0))
        win_condition = True
        car.MAX_FORWARD_SPEED = 0
        car.MAX_REVERSE_SPEED = 0
        pygame.mixer.music.play(loops=0, start=0.0)
        win_text = win_font.render('Press Space to Advance', True, (0,255,0))
        if win_condition == True:
            car.k_right = -5
            
    '''
   
    pad_group.update(collisions)
    pad_group.draw(screen)
    car_group.draw(screen)
    
    #trophy_group.draw(screen)
    #Counter Render
    pygame.display.flip()


