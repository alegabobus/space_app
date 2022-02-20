import pygame
import random
class Bonus(pygame.sprite.Sprite):
    types_list = ['bolt','pill','shield','star','things']
    image_name_list = ["bolt_silver.png", "star_gold.png",
                        "pill_blue.png", "shield_gold.png","things_gold.png"]
    powerups_images = dict(zip(types_list,image_name_list))
    def __init__(self,x,y,speedy):
        pygame.sprite.Sprite.__init__(self)
        #выдать случайное число от 0 до 4
        self_type = random.choice(Bonus.types_list)
        file_name = Bonus.powerups_images[self_type]
        self.image = pygame.image.load("images/" + file_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 3
        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom <= 0:
                self.kill()
        