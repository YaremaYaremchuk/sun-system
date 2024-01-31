import pygame
import math
import random
pygame.init()



Width = 1280
Height = 720


win = pygame.display.set_mode((Width,Height))

pygame.display.set_caption("Star System")


Star_mass = 100
Planet_mass = 5
G = 5
FPS = 60

Planetlist = ["earth.png","saturn.png","strashno.png","jupiter.png"]
Star_Radius = 120
Planet_Radius = 30
VerScale = 100
line_color = [255,255,255]

Backgr = pygame.transform.scale(pygame.image.load("star.jpeg"),(Width,Height))
Star = pygame.transform.scale(pygame.image.load("star.png"),(Star_Radius*2,Star_Radius*2))
Planet = pygame.transform.scale(pygame.image.load(random.choice(Planetlist)),(Planet_Radius*2,Planet_Radius*2))


class Planets:
    def __init__(self, x, y, x_vel, y_vel, mass):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass

    def draw(self):
        win.blit(Planet,(int(self.x-30),int(self.y-30)))


if __name__=="__main__":
    state = True

    planets = []
    start_plan_pos = None

    while state:
        pygame.time.Clock().tick(FPS)
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
        if mouse_pressed[0] == True:
            start_plan_pos = mouse

        win.blit(Backgr,(0,0))

        win.blit(Star,((Width/2)-120,(Height/2)-120))

        if start_plan_pos:
            pygame.draw.line(win,line_color,start_plan_pos,mouse, 2)
            win.blit(Planet,(start_plan_pos[0]-30,start_plan_pos[1]-30))

            
        
        pygame.display.update()
    pygame.quit()
            









