import gym
import numpy as np
from gym import spaces
from gym.envs.registration import EnvSpec
import pygame, math, sys, time
from pygame.locals import *




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
        #pygame.draw.rect(screen, (255, 255, 0), self.rect, width=2)



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
        if obj.rect.centerx < self.xnew and y_pos > 0:
            #left, top, width, height
            self.rect = pygame.Rect(obj.rect.centerx, obj.rect.centery, x_pos, y_pos)

        elif obj.rect.centerx > self.xnew and y_pos > 0:
             self.rect = pygame.Rect(self.xnew, obj.rect.centery, abs(x_pos), y_pos)

        elif obj.rect.centerx < self.xnew and y_pos < 0:
            self.rect = pygame.Rect(obj.rect.centerx, self.ynew, x_pos, abs(y_pos))

        else:
            self.rect = pygame.Rect(self.xnew, self.ynew, abs(x_pos), abs(y_pos))
        #self.rect = pygame.draw.line(screen,(255,0,0),(obj.rect.centerx, obj.rect.centery), (self.xnew, obj.rect.centery + y_pos), width=5)
    def update(self):

        rad = -self.obj.direction * math.pi / 180
        s = math.sin(rad);
        c = math.cos(rad);
        x = self.obj.rect.centerx
        y = self.obj.rect.centery

        xnew = c*(self.xpos) - s *(self.ypos) + x
        ynew = s*(self.xpos) + c *(self.ypos) + y

        if x < xnew and y < ynew:
            #left, top, width, height
            self.rect = pygame.Rect(x , y, abs(x - xnew), abs(y - ynew))

        elif x > xnew and y < ynew:
             self.rect = pygame.Rect(xnew , y, abs(x - xnew), abs(y - ynew))

        elif x < xnew and y > ynew:
            self.rect = pygame.Rect(x , ynew, abs(x - xnew), abs(y - ynew))

        else:
            self.rect = pygame.Rect(xnew , ynew, abs(x - xnew), abs(y - ynew))

        #self.rect = pygame.draw.line(screen,(255, 0, 0),(x, y),(xnew, ynew), width=2)




class PadSprite(pygame.sprite.Sprite):
    normal = None
    #hit = pygame.image.load('collision.png')
    def __init__(self, position, image):
        self.image = pygame.image.load(image)
        super(PadSprite, self).__init__()
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = position
    def update(self, hit_list):
        if self in hit_list: 
            #self.image = self.hit
            self.position = (50, 50)
        else: self.image = self.normal


class CheckPointSprite(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, val):
        super(CheckPointSprite, self).__init__()
        self.rect = pygame.Rect(left, top, width, height)
        self.val = val




# environment for all agents in the multiagent world
# currently code assumes that no agents will be created/destroyed at runtime!
class MultiCarEnv(gym.Env):
    metadata = {
        'render.modes' : ['human', 'console']
    }

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self):
        super(MultiCarEnv, self).__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        self.screen.fill([128, 128, 128])
        pygame.display.update()

        self.pads = [
            PadSprite((50, 50), 'pad_vert.png'),
            PadSprite((50, 100), 'pad_vert.png'),
            PadSprite((50, 150), 'pad_vert.png'),
            PadSprite((50, 200), 'pad_vert.png'),
            PadSprite((50, 250), 'pad_vert.png'),
            PadSprite((50, 300), 'pad_vert.png'),
            PadSprite((50, 350), 'pad_vert.png'),
            PadSprite((50, 400), 'pad_vert.png'),
            PadSprite((50, 450), 'pad_vert.png'),
            PadSprite((50, 500), 'pad_vert.png'),
            PadSprite((50, 550), 'pad_vert.png'),
            PadSprite((50, 600), 'pad_vert.png'),
            PadSprite((50, 650), 'pad_vert.png'),
            PadSprite((50, 700), 'pad_vert.png'),

            PadSprite((160, 150), 'pad_vert.png'),
            PadSprite((160, 200), 'pad_vert.png'),
            PadSprite((160, 250), 'pad_vert.png'),
            PadSprite((160, 300), 'pad_vert.png'),
            PadSprite((160, 350), 'pad_vert.png'),
            PadSprite((160, 400), 'pad_vert.png'),
            PadSprite((160, 450), 'pad_vert.png'),
            PadSprite((160, 500), 'pad_vert.png'),
            PadSprite((160, 550), 'pad_vert.png'),
            PadSprite((160, 600), 'pad_vert.png'),

            PadSprite((75, 32), 'pad_horiz.png'),
            PadSprite((125, 32), 'pad_horiz.png'),
            PadSprite((175, 32), 'pad_horiz.png'),
            PadSprite((225, 32), 'pad_horiz.png'),
            PadSprite((275, 32), 'pad_horiz.png'),
            PadSprite((325, 32), 'pad_horiz.png'),
            PadSprite((375, 32), 'pad_horiz.png'),
            PadSprite((425, 32), 'pad_horiz.png'),
            PadSprite((475, 32), 'pad_horiz.png'),
            PadSprite((525, 32), 'pad_horiz.png'),
            PadSprite((575, 32), 'pad_horiz.png'),
            PadSprite((625, 32), 'pad_horiz.png'),
            PadSprite((675, 32), 'pad_horiz.png'),
            PadSprite((725, 32), 'pad_horiz.png'),
            PadSprite((775, 32), 'pad_horiz.png'),
            PadSprite((825, 32), 'pad_horiz.png'),
            PadSprite((875, 32), 'pad_horiz.png'),
            PadSprite((925, 32), 'pad_horiz.png'),

            PadSprite((180, 122), 'pad_horiz.png'),
            PadSprite((225, 122), 'pad_horiz.png'),
            PadSprite((275, 122), 'pad_horiz.png'),
            PadSprite((325, 122), 'pad_horiz.png'),
            PadSprite((375, 122), 'pad_horiz.png'),
            PadSprite((425, 122), 'pad_horiz.png'),
            PadSprite((475, 122), 'pad_horiz.png'),
            PadSprite((525, 122), 'pad_horiz.png'),
            PadSprite((575, 122), 'pad_horiz.png'),
            PadSprite((625, 122), 'pad_horiz.png'),
            PadSprite((675, 122), 'pad_horiz.png'),
            PadSprite((725, 122), 'pad_horiz.png'),
            PadSprite((775, 122), 'pad_horiz.png'),
            PadSprite((825, 122), 'pad_horiz.png'),


            PadSprite((950, 50), 'pad_vert.png'),
            PadSprite((950, 100), 'pad_vert.png'),
            PadSprite((950, 150), 'pad_vert.png'),
            PadSprite((950, 200), 'pad_vert.png'),
            PadSprite((950, 250), 'pad_vert.png'),
            PadSprite((950, 300), 'pad_vert.png'),
            PadSprite((950, 350), 'pad_vert.png'),
            PadSprite((950, 400), 'pad_vert.png'),
            PadSprite((950, 450), 'pad_vert.png'),
            PadSprite((950, 500), 'pad_vert.png'),
            PadSprite((950, 550), 'pad_vert.png'),
            PadSprite((950, 600), 'pad_vert.png'),
            PadSprite((950, 650), 'pad_vert.png'),
            PadSprite((950, 700), 'pad_vert.png'),


            PadSprite((841, 150), 'pad_vert.png'),
            PadSprite((841, 200), 'pad_vert.png'),
            PadSprite((841, 250), 'pad_vert.png'),
            PadSprite((841, 300), 'pad_vert.png'),
            PadSprite((841, 350), 'pad_vert.png'),
            PadSprite((841, 400), 'pad_vert.png'),
            PadSprite((841, 450), 'pad_vert.png'),
            PadSprite((841, 500), 'pad_vert.png'),
            PadSprite((841, 550), 'pad_vert.png'),
            PadSprite((841, 600), 'pad_vert.png'),

            PadSprite((180, 630), 'pad_horiz.png'),
            PadSprite((225, 630), 'pad_horiz.png'),
            PadSprite((275, 630), 'pad_horiz.png'),
            PadSprite((325, 630), 'pad_horiz.png'),
            PadSprite((375, 630), 'pad_horiz.png'),
            PadSprite((425, 630), 'pad_horiz.png'),
            PadSprite((475, 630), 'pad_horiz.png'),
            PadSprite((525, 630), 'pad_horiz.png'),
            PadSprite((575, 630), 'pad_horiz.png'),
            PadSprite((625, 630), 'pad_horiz.png'),
            PadSprite((675, 630), 'pad_horiz.png'),
            PadSprite((725, 630), 'pad_horiz.png'),
            PadSprite((775, 630), 'pad_horiz.png'),
            PadSprite((825, 630), 'pad_horiz.png'),

            PadSprite((75, 718), 'pad_horiz.png'),
            PadSprite((125, 718), 'pad_horiz.png'),
            PadSprite((175, 718), 'pad_horiz.png'),
            PadSprite((225, 718), 'pad_horiz.png'),
            PadSprite((275, 718), 'pad_horiz.png'),
            PadSprite((325, 718), 'pad_horiz.png'),
            PadSprite((375, 718), 'pad_horiz.png'),
            PadSprite((425, 718), 'pad_horiz.png'),
            PadSprite((475, 718), 'pad_horiz.png'),
            PadSprite((525, 718), 'pad_horiz.png'),
            PadSprite((575, 718), 'pad_horiz.png'),
            PadSprite((625, 718), 'pad_horiz.png'),
            PadSprite((675, 718), 'pad_horiz.png'),
            PadSprite((725, 718), 'pad_horiz.png'),
            PadSprite((775, 718), 'pad_horiz.png'),
            PadSprite((825, 718), 'pad_horiz.png'),
            PadSprite((875, 718), 'pad_horiz.png'),
            PadSprite((925, 718), 'pad_horiz.png')
        ]
        self.pad_group = pygame.sprite.RenderPlain(*self.pads)

        car = CarSprite('car.png', (100, 660))
        car2 = CarSprite('car.png', (100, 600))
        self.cars = [car, car2]
        self.car_group = pygame.sprite.RenderPlain(*self.cars)
        sensors1 = [SensorSprite(0, -150, car), 
              SensorSprite(100, -130, car),
              SensorSprite(-100, -130, car), 
              SensorSprite(150, 0, car), 
              SensorSprite(-150, 0, car),
              SensorSprite(0, 150, car),
              SensorSprite(100, 130, car),
              SensorSprite(-100, 130, car)]
        sensors2 = [
              SensorSprite(0, -150, car2), 
              SensorSprite(100, -130, car2),
              SensorSprite(-100, -130, car2), 
              SensorSprite(150, 0, car2), 
              SensorSprite(-150, 0, car2),
              SensorSprite(0, 150, car2),
              SensorSprite(100, 130, car2),
              SensorSprite(-100, 130, car2)]
        self.sensors = [sensors1, sensors2]
        self.sensor_group = []
        for sensor in self.sensors:
          self.sensor_group.append(pygame.sprite.RenderPlain(*sensor))

        self.checkpoints = [CheckPointSprite(55, 35, 100, 100, 5)]
        self.check_group = pygame.sprite.RenderPlain(*self.checkpoints)
    
        self.time = 0

        self.action_space = []
        self.observation_space = []
        #Left, right up, down
        action_space = spaces.Discrete(4)
        #distance to another object, checkpoint, time of lap
        obs_space = spaces.Box(low=0, high=+np.inf,
                                        shape=(10,), dtype=np.float32)
        for agent in self.cars:
            self.action_space.append(action_space)
            self.observation_space.append(obs_space)

        

    def step(self, action_n):
        obs_n = []
        reward_n = []
        done = False
        info_n = {}

        clock = pygame.time.Clock()
        deltat = clock.tick(30)
        self.time += deltat
        # set and perform action for each agent
        for i in range(0, len(action_n)):
            cur_action = action_n[i]
            if cur_action == self.LEFT:
                self.cars[i].k_left = 10
            elif cur_action == self.RIGHT:
                self.cars[i].k_right = -10
            elif cur_action == self.DOWN:
                self.cars[i].k_down = -2
            else:
                self.cars[i].k_up = 2
        self.car_group.update(deltat)
        for i in range(0, len(action_n)):
          self.sensor_group[i].update()

        # record observation for each agent
        j = 0
        for car in self.cars:
            current_obs = np.zeros(10)
            current_reward = 0
            closest_obj = float("inf")
            for i in range(0, len(self.sensors[j])):
                cur_sensor = self.sensors[j][i]
                pad_near = pygame.sprite.spritecollide(cur_sensor, self.pad_group, False, collided = None)
                car_near = pygame.sprite.spritecollide(cur_sensor, self.car_group, False, collided = None)
                nearest_dist = float("inf")
                rect_list = []
                # use clip rect function
                for pad in pad_near:
                    newrect = pad.rect.clip(cur_sensor.rect)
                    rect_list.append(newrect)
                for other_car in car_near:
                    newrect = other_car.rect.clip(cur_sensor.rect)
                    rect_list.append(newrect)
                for rec in rect_list:
                    cur_dist = math.sqrt((rec.centerx - car.rect.centerx) ** 2 + (rec.centery - car.rect.centery) ** 2)
                    if  cur_dist < nearest_dist:
                        nearest_dist = cur_dist
                current_obs[i] = nearest_dist
                if nearest_dist < closest_obj:
                    closest_obj = nearest_dist
               

            checks = pygame.sprite.spritecollide(car, self.check_group, False, collided = None)
            max_check = 0;
            for check in checks:
                if check.val > max_check:
                    max_check = check.val

            current_obs[8] = max_check     
            current_obs[9] = self.time

            current_reward += closest_obj * 10
            current_reward += max_check * 10
            current_reward += self.time

            if pygame.sprite.spritecollideany(car, self.pad_group, collided = None): 
                current_reward -= 10000
            if not pygame.sprite.spritecollideany(car, self.check_group, collided = None):
                current_reward -= 10000
            for k in range(0, len(self.cars)):
                if k != j and car.rect.colliderect(self.cars[k].rect):
                    current_reward -= 10000

            obs_n.append(current_obs)
            reward_n.append(current_reward)
            j += 1


        return obs_n, reward_n, done, info_n

    def reset(self):
       
        # record observations for each agent
        obs_n = []
        

        car = CarSprite('car.png', (100, 660))
        car2 = CarSprite('car.png', (100, 600))
        self.cars = [car, car2]
        self.car_group = pygame.sprite.RenderPlain(*self.cars)
        sensors1 = [SensorSprite(0, -150, car), 
              SensorSprite(100, -130, car),
              SensorSprite(-100, -130, car), 
              SensorSprite(150, 0, car), 
              SensorSprite(-150, 0, car),
              SensorSprite(0, 150, car),
              SensorSprite(100, 130, car),
              SensorSprite(-100, 130, car)]
        sensors2 = [
              SensorSprite(0, -150, car2), 
              SensorSprite(100, -130, car2),
              SensorSprite(-100, -130, car2), 
              SensorSprite(150, 0, car2), 
              SensorSprite(-150, 0, car2),
              SensorSprite(0, 150, car2),
              SensorSprite(100, 130, car2),
              SensorSprite(-100, 130, car2)]
        self.sensors = [sensors1, sensors2]
        self.sensor_group = []
        for sensor in self.sensors:          
          self.sensor_group.append(pygame.sprite.RenderPlain(*sensor))

        self.time = 0

         # record observation for each agent
        j = 0
        for car in self.cars:
            current_obs = np.zeros(10)
            current_reward = 0
            closest_obj = float("inf")
            for i in range(0, len(self.sensors[j])):
                cur_sensor = self.sensors[j][i]
                pad_near = pygame.sprite.spritecollide(cur_sensor, self.pad_group, False, collided = None)
                car_near = pygame.sprite.spritecollide(cur_sensor, self.car_group, False, collided = None)
                nearest_dist = float("inf")
                rect_list = []
                # use clip rect function
                for pad in pad_near:
                    newrect = pad.rect.clip(cur_sensor.rect)
                    rect_list.append(newrect)
                for other_car in car_near:
                    newrect = other_car.rect.clip(cur_sensor.rect)
                    rect_list.append(newrect)
                for rec in rect_list:
                    cur_dist = math.sqrt((rec.centerx - car.rect.centerx) ** 2 + (rec.centery - car.rect.centery) ** 2)
                    if  cur_dist < nearest_dist:
                        nearest_dist = cur_dist
                current_obs[i] = nearest_dist
                if nearest_dist < closest_obj:
                    closest_obj = nearest_dist
               

            checks = pygame.sprite.spritecollide(car, self.check_group, False, collided = None)
            max_check = 0;
            for check in checks:
                if check.val > max_check:
                    max_check = check.val

            current_obs[8] = max_check     
            current_obs[9] = self.time

            obs_n.append(current_obs)
            j += 1



        return obs_n


    # render environment
    def render(self, mode='human'):
        self.screen.fill([128, 128, 128])
        self.pad_group.draw(self.screen)
        self.car_group.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()



        
