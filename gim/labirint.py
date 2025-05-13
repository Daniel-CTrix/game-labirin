import pygame
from pygame import *

# Inisialisasi
pygame.init()
font.init()
window = display.set_mode((500, 500))
display.set_caption('Labirin')

# Warna dan font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font_game = font.SysFont('Arial', 40)
pesan_menang = font_game.render('MENANG!', True, (0, 255, 0))
pesan_kalah = font_game.render('KALAH!', True, (255, 0, 0))

# Background
background = image.load('bg.jpg')
background = transform.scale(background, (500, 500))

# Grup Sprite
group_enemy = sprite.Group()
barriers = sprite.Group()
group_bullet = sprite.Group()

# Kelas dasar
class GameSprite(sprite.Sprite):
    def __init__(self, image_file, height, width, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image_file), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image_file, height, width, x, y, speed_x, speed_y):
        super().__init__(image_file, height, width, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        platform_touched = sprite.spritecollide(self, barriers, False)
        for p in platform_touched:
            if self.speed_x > 0:
                self.rect.right = min(self.rect.right, p.rect.left)
            elif self.speed_x < 0:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.rect.y += self.speed_y
        platform_touched = sprite.spritecollide(self, barriers, False)
        for p in platform_touched:
            if self.speed_y > 0:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.speed_y < 0:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('pluru.png', 30, 10, self.rect.right, self.rect.centery, 15)
        group_bullet.add(bullet)

class Enemy(GameSprite):
    def __init__(self, image_file, height, width, x, y, x_awal, x_akhir, speed):
        super().__init__(image_file, height, width, x, y)
        self.x_awal = x_awal
        self.x_akhir = x_akhir
        self.speed = speed

    def update_pos(self):
        self.rect.x += self.speed
        if self.rect.x < self.x_awal or self.rect.x > self.x_akhir:
            self.speed *= -1

class Bullet(GameSprite):
    def __init__(self, image_file, height, width, x, y, speed):
        super().__init__(image_file, height, width, x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 500:
            self.kill()

class Wall(GameSprite):
    def _init_(self, image_file, height, width, x, y):
        super()._init_(image_file, height, width, x, y)

class Finish(GameSprite):
    def _init_(self, image_file, height, width, x, y):
        super().__init__(image_file, height, width, x, y)

class Button(GameSprite):
    def __init__(self, image_file, height, width, x, y):
        super().__init__(image_file, height, width, x, y)

# Objek
finish = Finish('finish.jpeg', 50, 50, 450, 450)
player = Player('peu.png', 90, 90, 0, 0, 0, 0)
btn = Button('play.jpeg', 300, 300, 100, 100)

# Buat level
def create_level(level):
    group_enemy.empty()
    barriers.empty()

    if level == 1:
        enemy = Enemy('pou.png', 90, 90, 200, 200, 100, 400, 2)  
        group_enemy.add(enemy)
        barriers.add(Wall('dinding.jpeg', 200, 50, 150, 150))

    elif level == 2:
        enemy = Enemy('pou.png', 90, 90, 330, 330, 10, 500, 3)
        enemy1 = Enemy('pou.png', 90, 90, 100, 200, 10, 300, 2)
        enemy2 = Enemy('pou.png', 90, 90, 400, 0, 50, 450, 2)
        group_enemy.add(enemy, enemy1, enemy2)
        barriers.add(Wall('dinding.jpeg', 300, 50, 100, 100))
        barriers.add(Wall('dinding.jpeg', 150, 50, 200, 350))

# Game Loop
level = 1
create_level(level)
done = False
run = True
Menu = True

while run:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            run = False

    if Menu:
        window.blit(background, (0, 0))
        btn.reset()
        for e in events:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn.rect.collidepoint(x, y):
                    Menu = False
        display.update()
        continue

    if not done:
        time.delay(50)
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        finish.reset()
        barriers.draw(window)
        group_enemy.draw(window)
        group_bullet.draw(window)

        for bullet in group_bullet:
            bullet.update()

        sprite.groupcollide(group_bullet, barriers, True, False)
        sprite.groupcollide(group_bullet, group_enemy, True, True)

        for enemy in group_enemy:
            enemy.update_pos()

        if sprite.collide_rect(player, finish):
            if level == 1:
                level = 2
                create_level(level)
                player.rect.x = 0
                player.rect.y = 0
            else:
                window.blit(pesan_menang, (50, 50))
                done = True
        if sprite.spritecollide(player, group_enemy, False):
            window.blit(pesan_kalah, (50, 50))
            done = True

        for e in events:
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_a:
                    player.speed_x = -5
                if e.key == K_d:
                    player.speed_x = 5
                if e.key == K_w:
                    player.speed_y = -5
                if e.key == K_s:
                    player.speed_y = 5
                if e.key == K_f:
                    player.fire()
                    
            if e.type == KEYUP:
                if e.key in [K_a, K_d]:
                    player.speed_x = 0
                if e.key in [K_w, K_s]:
                    player.speed_y = 0

    display.update()

pygame.quit()