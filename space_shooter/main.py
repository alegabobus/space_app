# подключаем модули
import pygame
import sys
from bonus import Bonus
from random import randint
from const import *
from ship import Ship
from bg import Background
from meteor import Meteor
from patrons import Bullet
from text import TextObject

#НАСТРОЙКА ИГРЫ (ИНИЦИАЛИЗАЦИЯ)
#инициализация библиотеки
pygame.init()
#создание экрана, указываем ширину и высоту в кортеже
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# создаем часы для отслеживания FPS
clock = pygame.time.Clock()
shoot_sound= pygame.mixer.Sound('res/sfx_laser2.ogg')
#создание групп
score = 0
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
bonus_sprites = pygame.sprite.Group()
#создание игровых объектов
hp = 100

player_ship = Ship()
bg1 = Background(0,0)
bg2 = Background(0,-SCREEN_HEIGHT)
meteors = []
text_score = TextObject(10,10, lambda : str(score),YELLOW,"Arial", 28)
for i in range(15):
    meteor = Meteor()
    meteors.append(meteor)
#добавление в группы
all_sprites.add(bg1)
all_sprites.add(bg2)
all_sprites.add(player_ship)
for i in range(15):
    all_sprites.add(meteors[i])
    meteor_sprites.add(meteors[i])

def draw_hp_bar(screen,x,y,hp):
    if hp < 0:
        hp = 0
    fill = hp/100 * HP_BAR_WIDTH
    circuit_rect = pygame.Rect(x,y,HP_BAR_WIDTH,HP_BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,HP_BAR_HEIGHT)
    pygame.draw.rect(screen,GREEN, fill_rect)
    pygame.draw.rect(screen,WHITE, circuit_rect,2)
# переменная для управления циклом
run = True
# основной игровой цикл
while run:
    #0 задержка для фиксированного FPS
    clock.tick(FPS)
    #1 обработка событий
    for event in pygame.event.get():
        # если тип события - закрытие окна программы
        if event.type == pygame.QUIT:
            # выйти из программы
            run = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_x :
                    bullet = Bullet(player_ship.rect.centerx,player_ship.rect.top)
                    all_sprites.add(bullet)
                    bullet_sprites.add(bullet)
                    shoot_sound.play()
                    
    #2 действия и взаимодействия
    all_sprites.update()
    #проверка столкновений
    hits = pygame.sprite.spritecollide(player_ship, meteor_sprites, True)
    for meteor in hits:
        #спавн нового метеора взамен удаленного
        new_meteor = Meteor()
        all_sprites.add(new_meteor)
        meteor_sprites.add(new_meteor)
        hp -= meteor.rect.width // 3
        #конец игры
    if hp <= 0:
        run = False
    bullet_hits = pygame.sprite.groupcollide(meteor_sprites,bullet_sprites, True,True)
    for meteor in bullet_hits:
        chance = randint(1,1000)
        if chance < 100:
            bonus = Bonus(meteor.rect.centerx,meteor.rect.centery,meteor.speedy)
            all_sprites.add(bonus)
            bonus_sprites.add(bonus)
        new_meteor = Meteor()
        all_sprites.add(meteor)
        meteor_sprites.add(meteor)
        score += 1
    bonus_hits = pygame.sprite.spritecollide(ship,bonus_sprites,True) 
    for bonus in bonus_hits:
        if bonus.type == 'pill':
            hp += 15
            if hp > 100:
                hp = 100
            hp += 15
        if bonus.type == 'shield':
        
    #3 отрисовка
    screen.fill(GREY)
    all_sprites.draw(screen)
    text_score.draw(screen)
    draw_hp_bar(screen,SCREEN_WIDTH - 120,20,hp)
    pygame.display.update()
#здесь основной цикл игры закончился
# завершить pygame
pygame.quit()
# выйти
sys.exit()
