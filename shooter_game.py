#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()


clock = time.Clock()

class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
   def update(self):
      self.rect.y += self.speed
      if self.rect.y < 0:
         self.kill()

class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 5:
         self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < win_width - 80:
         self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
      bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 35, 35, -15)
      bullets.add(bullet)

       


lost = 0
class Enemy(GameSprite):
   def update(self):
      self.rect.y += self.speed
      global lost
      if self.rect.y >= 560:
         lost = lost + 1
         self.rect.y = 0
         self.rect.x = randint(0, 800)
         
         
font.init()
font = font.SysFont('Arial', 36)
win = font.render('YOU WIN', True, (255, 255, 255))
lose = font.render("YOU LOSE", True, (180, 0, 0))


text_win = font.render('Сбито:' + str(lost), 1, (255, 255, 255))

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
   monster = Enemy('ufo.png', randint(50, 700), 10, 50, 100, randint(2, 9))
   monsters.add(monster)


win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.png'), (win_width, win_height))


#создаем спрайты
ship = Player('hero.jpg', 5, win_height - 100, 80, 100, 10)

finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
score = 0
num_fire = 0
rel_time = False
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
      if e.type == QUIT:
         run = False
      elif e.type == KEYDOWN:
         if e.key == K_SPACE:
            if num_fire < 5 and rel_time == False:
               num_fire = num_fire + 1
               ship.fire()
            

            if num_fire >= 5 and rel_time == False:
               last_time = timer()
               rel_time = True
                


            


      
      


   if not finish:
      #обновляем фон
      window.blit(background,(0,0))
      if rel_time == True:
               now_time = timer()
               if now_time - last_time < 3:
                  reload = font.render('Wait, reload...', 1, (150, 0, 0))
                  window.blit(reload, (260, 460))
               else:
                  num_fire = 0
                  rel_time = False


      #производим движения спрайтов
      ship.update()


      #обновляем их в новом местоположении при каждой итерации цикла
      ship.reset()
      monsters.draw(window)
      bullets.draw(window)
      monsters.update()
      bullets.update()
      text_lose = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
      window.blit(text_lose, (10, 10))
      sprites_list = sprite.groupcollide(monsters, bullets, True, True)
      for i in sprites_list:
         score += 1
         monster = Enemy('ufo.png', randint(50, 700), 10, 50, 100, randint(2, 9))
         monsters.add(monster)
      if score >= 10:
         finish = True
         window.blit(win, (200, 200))
      if lost >= 10:
         finish = True
         window.blit(lose, (200, 200))
      
      text = font.render('Счет: ' + str(score), 1, (255, 255, 255))
      window.blit(text, (10, 40))




      display.update()
   time.delay(50)


       
