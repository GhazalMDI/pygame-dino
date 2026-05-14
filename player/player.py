import pygame

class Player:
    """create player class (Dino)"""
    
    def __init__(self):
        self.x = 50
        
        # dino  y-axis
        self.y = 300
        self.width = 40
        self.height = 40
        
        self.image = pygame.image.load('assets/dino.png')
        self.image = pygame.transform.scale(self.image,(self.width, self.height))
        
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        
        self.color = (0,0,0)
        
        # speed dino (y)
        self.velocity_y = 0
        self.gravity = 1
        
        self.jump_force = -15
        
        # ground 
        self.ground_y = 300
        
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.y == self.ground_y:
            self.velocity_y = self.jump_force
            
            
        self.velocity_y +=self.gravity
        
        self.y += self.velocity_y
        
        if self.y >= self.ground_y:
            self.y =  self.ground_y
            self.velocity_y = 0 
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))