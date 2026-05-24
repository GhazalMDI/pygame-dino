import random

import pygame

class Cactus:
    
    def __init__(self,x):
        self.x = x
        self.y= 300
        
        self.width = 25
        self.height = 50
        
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.images = [
                pygame.transform.scale(
                    pygame.image.load("assets/1_Cactus.png"),
                    (40, 50)
                ),
                pygame.transform.scale(
                    pygame.image.load("assets/3_Cactus.png"),
                    (45, 50)   
                )
        ]
        
        self.image = random.choice(self.images)
        
    def update(self):
        """use the - becouse Cactus move to left """
        self.x -= self.speed
        
        if self.x < -50:
            self.x = 800
            
        self.rect.x = self.x
        self.rect.y = self.y
            
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        
        
        
        