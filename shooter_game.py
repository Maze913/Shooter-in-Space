#Создай собственный Шутер!

from pygame import *
from random import *
#создай игру "Лабиринт"!

#создай окно игры
window = display.set_mode((700,500))
display.set_caption("Догонялки")
lost = 0
win = 0
bullets = sprite.Group()
#задай фон сцены
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 20, 20)
        bullets.add(bullet)
            
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=  self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(80, 600)
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        

background = transform.scale(image.load("sky-828648_1920.jpg"), (700, 500))
hero = Player('rocket.png', 25, 400, 10, 65, 65)



monsters = sprite.Group()
monsters2 = sprite.Group()
for i in range(0, 25):
    enemy = Enemy('ufo.png', randint(80, 600), -590, randint(1, 5), 60, 60)
    monsters.add(enemy)
for i in range(0, 3):
    enemy2 = Enemy('asteroid.png', randint(80, 600), -590, randint(1, 3), 60, 60)
    monsters2.add(enemy2)






clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
finish = False
x1, y1 = 300, 300
font.init()
font = SysFont('Aria', 35)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if not finish:
        window.blit(background,(0, 0))
        hero.reset()
        hero.update()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        monsters2.update()
        monsters2.draw(window)
        text_lose = font.render("Пропущено " + str(lost), True, (205, 215, 0))
        text_win = font.render("Счет " + str(win), True, (235, 205, 0))
        window.blit(text_lose, (10, 20))
        window.blit(text_win, (10, 60))
        
        if sprite.groupcollide(monsters, bullets, True, True):
            win = win + 1
            window.blit(text_win, (10, 60))
        if sprite.groupcollide(monsters2, bullets, False, True):
            pass
        if win == 20:
            finish = True
            text = font.render("Вы Выиграли", True, (235, 205, 0))
            window.blit(text, (275,150))
        if lost > 3 or sprite.spritecollide(hero, monsters, False):
            finish = True
            text = font.render("Вы Проиграли", True, (235, 205, 0))
            window.blit(text, (275,150))
        if lost > 3 or sprite.spritecollide(hero, monsters2, False):
            finish = True
            text = font.render("Вы Проиграли", True, (235, 205, 0))
            window.blit(text, (275,150))
        display.update()
        clock.tick(FPS)
