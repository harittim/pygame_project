import pygame
import os
import sys
import random
import time
import json

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class user_car:
    def __init__(self):
        self.pos = [[165, 510], [235, 640]]
        self.image = load_image('user_car.png')

    def move(self, x):
        if x >= 0 and self.pos[1][0] + x < 400:
            self.pos[1][0] += x
            self.pos[0][0] += x
        if x < 0 and self.pos[0][0] + x > 0:
            self.pos[1][0] += x
            self.pos[0][0] += x

    def crash(self, mas):
        ax1, ay1, ax2, ay2 = map(int, [self.pos[0][0], self.pos[0][1], self.pos[1][0], self.pos[1][1]])


        bx1, by1, bx2, by2 = map(int, [mas[0][0], mas[0][1], mas[1][0], mas[1][1]])


        s1 = (ax1 >= bx1 and ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
        s2 = (ay1 >= by1 and ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
        s3 = (bx1 >= ax1 and bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
        s4 = (by1 >= ay1 and by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)

        if (s1 and s2) or (s3 and s4) or (s1 and s4) or (s3 and s2):
            print(1)
            return True
        else:
            return False


class line:
    def __init__(self, x, y):
        self.pos = [x, y]

    def move(self, x):
        if x >= 0 and self.pos[1] + x - 70 < 600:
            self.pos[1] += x
        else:
            self.pos[1] = -70


class foren_car:
    def __init__(self):
        x = random.choice([25, 120, 210, 310])
        self.pos = [[x, -130], [x + 70, 0]]
        self.image = load_image('foren_car.png')

    def move(self, x):
        if x >= 0 and self.pos[1][0] + x < 400:
            self.pos[1][1] += x
            self.pos[0][1] += x

    def posit(self, x):
        self.pos[0][1] = x - 130
        self.pos[1][1] = x


def rec():
    with open('data/records.json', 'r', encoding='utf-8') as f:  # открыли файл
        text = json.load(f)  # загнали все из файла в переменную

    mas = []

    for i in range(len(text)):
        a = str(i + 1) + '. ' + str(text[i])
        mas.append(a)
    return mas


def rec_write(x):
    with open('data/records.json', 'r', encoding='utf-8') as f:  # открыли файл
        text = json.load(f)  # загнали все из файла в переменную
    text.append(x)
    text.sort()
    text = text[::-1]
    text = text[:5]
    with open('data/records.json', 'w') as f:
        json.dump(text, f)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Hi')
    size = width, height = 400, 650
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    running = True
    mouse = load_image('mouse.png')
    background = load_image('back.jpg')
    start = load_image('start.png')
    records = load_image('records.png')
    pygame.mouse.set_visible(False)
    type = 'menu'
    v = 3
    fullname = os.path.join('data', 'fon.mp3')
    pygame.mixer.music.load(fullname)
    masli = [105, 200, 295]
    maslin = []

    for i in masli:
        for y in range(50, 750, 125):
            a = line(i, y)
            maslin.append(a)

    while running:
        # установка заднего фона
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and type == 'menu':
                if 120 < event.pos[0] < 280 and 295 < event.pos[1] < 355:
                    type = 'running'
                    pygame.mixer.music.play()
                    user_car1 = user_car()
                    mas = []
                    points = 0

                    for i in range(1, 4):
                        a = foren_car()
                        a.posit(-1 * (i * 300))
                        mas.append(a)

                elif 120 < event.pos[0] < 280 and 355 < event.pos[1] < 415:
                    type = 'records'
            elif event.type == pygame.MOUSEBUTTONDOWN and type == 'pause':
                if 80 < event.pos[0] < 320 and 295 < event.pos[1] < 355:
                    type = 'running'
                    pygame.mixer.music.play()
            elif event.type == pygame.KEYDOWN and type == 'running':
                if event.key == pygame.K_LEFT:
                    user_car1.move(-45)
                if event.key == pygame.K_RIGHT:
                    user_car1.move(45)
                if event.key == pygame.K_ESCAPE:
                    type = 'pause'
                    pygame.mixer.music.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN and type == 'records':
                if 70 < event.pos[0] < 330 and 400 < event.pos[1] < 460:
                    type = 'menu'
                    pygame.mixer.music.stop()

        if type == 'running':
            myfont = pygame.font.SysFont('timesnewroman', 20)
            textsurface = myfont.render('Счёт: ' + str(points), False, (255, 255, 255))

            for i in range(len(maslin)):
                pygame.draw.line(screen, (255, 255, 0),
                                 maslin[i].pos,
                                 [maslin[i].pos[0], maslin[i].pos[1] + 70], 4)
                maslin[i].move(2)

            for i in range(len(mas)):
                if user_car1.crash(mas[i].pos):
                    pygame.mixer.music.stop()
                    rec_write(points)
                    type = 'zastavka'
                if mas[i].pos[0][1] >= 650:
                    mas[i] = foren_car()
                    points += 1
                screen.blit(mas[i].image, mas[i].pos)
                mas[i].move(1)
            v = 1 - points // 15
            screen.blit(textsurface, (300, 0))
            screen.blit(user_car1.image, user_car1.pos)

        elif type == 'menu':
            for i in range(len(maslin)):
                pygame.draw.line(screen, (255, 255, 0),
                                 maslin[i].pos,
                                 [maslin[i].pos[0], maslin[i].pos[1] + 70], 4)
            screen.blit(start, [120, 295])
            screen.blit(records, [81, 375])
            if pygame.mouse.get_focused():
                screen.blit(mouse, pygame.mouse.get_pos())

        elif type == 'pause':
            for i in range(len(maslin)):
                pygame.draw.line(screen, (255, 255, 0),
                                 maslin[i].pos,
                                 [maslin[i].pos[0], maslin[i].pos[1] + 70], 4)
            myfont = pygame.font.SysFont('timesnewroman', 48)
            textsurface = myfont.render('Продолжить', False, (255, 255, 255))
            screen.blit(textsurface, [80, 295])
            if pygame.mouse.get_focused():
                screen.blit(mouse, pygame.mouse.get_pos())
            for i in range(len(mas)):
                screen.blit(mas[i].image, mas[i].pos)
            screen.blit(user_car1.image, user_car1.pos)

        elif type == 'zastavka':
            for i in range(len(maslin)):
                pygame.draw.line(screen, (255, 255, 0),
                                 maslin[i].pos,
                                 [maslin[i].pos[0], maslin[i].pos[1] + 70], 4)
            myfont = pygame.font.SysFont('timesnewroman', 48)
            textsurface = myfont.render('Твой счёт: ' + str(points), False, (255, 255, 255))
            screen.blit(textsurface, [80, 295])
            pygame.display.flip()
            time.sleep(2)
            type = 'menu'

        elif type == 'records':
            for i in range(len(maslin)):
                pygame.draw.line(screen, (255, 255, 0),
                                 maslin[i].pos,
                                 [maslin[i].pos[0], maslin[i].pos[1] + 70], 4)
            myfont = pygame.font.SysFont('timesnewroman', 48)
            textsurface = myfont.render('Рекорды', False, (255, 255, 255))
            screen.blit(textsurface, [115, 100])
            textsurface = myfont.render('Главное меню', False, (255, 255, 255))
            screen.blit(textsurface, [70, 400])
            rec_out = rec()
            myfont = pygame.font.SysFont('timesnewroman', 30)
            for i in range(len(rec_out)):
                textsurface = myfont.render(rec_out[i], False, (255, 255, 255))
                screen.blit(textsurface, [140, 170 + i * 40])

            if pygame.mouse.get_focused():
                screen.blit(mouse, pygame.mouse.get_pos())

        pygame.display.flip()
        pygame.time.delay(5)

    pygame.quit()