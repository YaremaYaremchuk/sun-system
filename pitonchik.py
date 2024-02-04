import pygame
import math
import random
from time import time
pygame.init()



Width = 1280
Height = 720


win = pygame.display.set_mode((Width,Height))

pygame.display.set_caption("Star System")


Star_mass = 400
Planet_mass = 5
G = 6
FPS = 60


Planetlist = ["earth.png","saturn.png","strashno.png","jupiter.png"]
Star_Radius = 120
Planet_Radius = 30
VerLimit = 90
line_color = [255,255,255]
bg = [0,0,0]

font = pygame.font.Font('freesansbold.ttf', 32)
Gtext = font.render('G-force', True, line_color)
Startext = font.render('Star Mass', True, line_color)
Planettext = font.render('Planet Mass', True, line_color)

Backgr = pygame.transform.scale(pygame.image.load("star.jpeg"),(Width,Height))
Star = pygame.transform.scale(pygame.image.load("star.png"),(Star_Radius*2,Star_Radius*2))
Planet = pygame.transform.scale(pygame.image.load(random.choice(Planetlist)),(Planet_Radius*2,Planet_Radius*2))
t = time()

class Stars:
    def __init__(self,x,y,mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(Star, (self.x-Star_Radius, self.y-Star_Radius))



class Planets:
    def __init__(self, x, y, x_vel, y_vel, mass, image):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.image = image

    def move(self, star=None):
        distance = math.sqrt((self.x-star.x)**2 + (self.y-star.y)**2)
        grav = (G * self.mass * Star_mass) / distance**2
        acceleration = grav/self.mass
        theta = math.atan2(star.y-self.y, star.x-self.x)
        self.x_vel += acceleration * math.cos(theta)
        self.y_vel += acceleration *  math.sin(theta)
       
        self.x+=self.x_vel
        self.y+=self.y_vel


    def draw(self):
        win.blit(self.image,(int(self.x-Planet_Radius),int(self.y-Planet_Radius)))


class Menu:
    def __init__(self):
        self.sliders = [
            Slider(((Width//2)-320,Height-50), (300,30), 0.13, 100, 3000),
            Slider((Width//2,Height-50), (300,30), 0.05, 1, 500),
            Slider(((Width//2)+320,Height-50), (300,30), 0.06, 1, 100),
        ]
        self.menu_container = pygame.Rect(self.sliders[0].slider_left, self.sliders[0].slider_top, len(self.sliders)*320+10, 30)
    def run(self, mouse, mouse_pressed):
        for slider in self.sliders:
            if slider.containter.collidepoint(mouse) and mouse_pressed[0]:
                slider.move(mouse)
                
            slider.draw()
        

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val:float, min:int, max:int):
        self.pos = pos
        self.size = size

        self.slider_left = self.pos[0] - (self.size[0]//2)
        self.slider_right = self.pos[0] + (self.size[0]//2)
        self.slider_top = self.pos[1] - (self.size[1]//2)
        self.slider_bottom = self.pos[1] + (self.size[1]//2)


        self.min = min
        self.max = max
        self.initial_val = (self.slider_right-self.slider_left)*initial_val

        self.containter = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button = pygame.Rect(self.slider_left+self.initial_val-5, self.slider_top, 10, self.size[1])
    def move(self, mouse):
        self.button.centerx = mouse[0]


    def get_value(self):
        range = self.slider_right - self.slider_left - 1
        value = self.button.centerx - self.slider_left 

        return(int((value/range)*(self.max-self.min)+self.min))

    def draw(self):
        pygame.draw.rect(win, "white", self.containter)
        pygame.draw.rect(win, "black", self.button)

def planet_create(location, mouse):
    t_x,t_y=location
    l_x,l_y=mouse
    vel_x=(l_x-t_x)/VerLimit
    vel_y=(l_y-t_y)/VerLimit
    obj = Planets(t_x,t_y,vel_x,vel_y,Planet_mass,Planet)
    return obj

def display_values(Startext,StarRect,Planettext,PlanRect,Gtext,GRect):
    win.blit(Startext,StarRect)
    win.blit(Planettext,PlanRect)
    win.blit(Gtext,GRect)


if __name__=="__main__":
    state = True
    StarRect = Startext.get_rect()
    StarRect.center = ((Width//2)-320,Height-90)
    GRect = Gtext.get_rect()
    GRect.center = ((Width//2)+320, Height-90)
    PlanRect = Planettext.get_rect()
    PlanRect.center = ((Width//2), Height-90)
    planets = []
    start_plan_pos = None
    star = Stars(Width//2, Height//2, Star_mass)
    menu = Menu()
    while state:
        pygame.time.Clock().tick(FPS)
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False

        if mouse_pressed[0] == True and time()-t>0.4 and not menu.menu_container.collidepoint(mouse):
            if start_plan_pos:
                    obj = planet_create(start_plan_pos,mouse)
                    planets.append(obj)
                    start_plan_pos=None
                    Planet = pygame.transform.scale(pygame.image.load(random.choice(Planetlist)),(Planet_Radius*2,Planet_Radius*2))

            else:
                start_plan_pos = mouse
            t=time()

        win.blit(Backgr,(0,0))

        if start_plan_pos:
            pygame.draw.line(win,line_color,start_plan_pos,mouse, 2)
            win.blit(Planet,(start_plan_pos[0]-Planet_Radius,start_plan_pos[1]-Planet_Radius))
        

        display_values(Startext,StarRect,Planettext,PlanRect,Gtext,GRect)
        for obj in planets[:]:
            obj.draw()
            obj.move(star)
            destroy = math.sqrt((obj.x-star.x)**2 + (obj.y-star.y)**2 ) <= Star_Radius
            cleanup = obj.x<0 or obj.x>Width or obj.y<0 or obj.y>Height
            collide = False
            for cur in planets[:]:
                if math.sqrt((cur.x-obj.x)**2 + (cur.y-obj.y)**2 ) <= Planet_Radius and math.sqrt((cur.x-obj.x)**2 + (cur.y-obj.y)**2 ) > 3:
                    collide = True
            if cleanup or destroy or collide:
                planets.remove(obj)
        



        star.draw()
        menu.run(mouse, mouse_pressed)
        Star_mass = menu.sliders[0].get_value()
        Planet_mass = menu.sliders[1].get_value()
        G = menu.sliders[2].get_value()
        pygame.display.update()
        
    pygame.quit()
            









