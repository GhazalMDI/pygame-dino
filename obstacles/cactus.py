import pygame

class Cactus:
    
    def __init__(self,x):
        self.x = x
        self.y= 300
        
        self.width = 30
        self.height = 50
        
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.image = pygame.image.load('assets/cactus.png')
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        
    def update(self):
        """use the - becouse Cactus move to left """
        self.x -= self.speed
        
        if self.x < -50:
            self.x = 800
            
        self.rect.x = self.x
        self.rect.y = self.y
            
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        
        
        
        