import pygame
import random

class Bird:
    
    def __init__(self,x):
        self.x = x
        
        self.y = random.choice([220,250,270])
        
        self.width = 40
        self.height = 30
        
        self.speed = 8
        
        self.images = [
            pygame.transform.scale(
                pygame.image.load("assets/Bird1.png"),
                (self.width,self.height)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/Bird2.png"),
                (self.width,self.height)
            )
        ]
        
        self.current_frame = 0
        self.anim_timer = 0
        
        self.image = self.images[0]
        
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        
    def update(self):
        self.x -= self.speed

        # animation
        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.anim_timer = 0

        self.image = self.images[self.current_frame]

        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))