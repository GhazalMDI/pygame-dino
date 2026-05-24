import pygame

class Player:
    """create player class (Dino)"""
    def __init__(self):
        self.x = 50
        # dino  y-axis
        self.y = 300
        self.width = 45
        self.height = 45
        
        self.run_images = [
            pygame.transform.scale(
                pygame.image.load("assets/Chrome_T-Rex_Left_Run.png"),
                (self.width,self.height)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/Chrome_T-Rex_Right_Run.png"),
                (self.width,self.height)
            )
        ]
        self.current_frame = 0
        self.animation_timer = 0
        
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        self.color = (0,0,0)
        # speed dino (y)
        self.velocity_y = 0
        self.gravity = 1
        
        self.jump_force = -15
        # ground 
        self.ground_y = 290
        self.jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
        self.die_sound = pygame.mixer.Sound("sounds/die.mp3")
        self.pint_sound = pygame.mixer.Sound("sounds/point.mp3")
        
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.y == self.ground_y:
            self.velocity_y = self.jump_force
            self.jump_sound.play()
            
        self.velocity_y +=self.gravity
        
        self.y += self.velocity_y
        
        if self.y >= self.ground_y:
            self.y =  self.ground_y
            self.velocity_y = 0 
            
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.animation_timer +=1
        if self.animation_timer >= 10:
            self.current_frame += 1
            if self.current_frame >= len(self.run_images):
                self.current_frame = 0
            self.animation_timer = 0
        
    
    def draw(self,screen):
        screen.blit(self.run_images[self.current_frame],(self.x,self.y))