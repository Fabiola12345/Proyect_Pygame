# ¡Crea tu propio juego de disparos!

from pygame import *
from random import randint

init()

ANCHO = 500
ALTO = 500
FPS = 60

pantalla = display.set_mode((ANCHO,ALTO))

reloj = time.Clock()

# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

    def iscollision(self, objetos):
       return self.rect.colliderect(objetos.rect)

#lISTADO 
bullets = []

class Bullet(GameSprite):
    def moveUP(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            if self in bullets:
                bullets.remove(self)

# clase del jugador principal
class Player(GameSprite):

    def moves(self):

        keys = key.get_pressed()

        if keys[K_a] or keys[K_LEFT]:
            self.rect.x -= self.speed
        elif keys [K_d] or keys[K_RIGHT]:
            self.rect.x += self.speed

    def shoot(self):
        keys = key.get_pressed()

        if keys[K_SPACE]:
            bullet = Bullet('bullet.png',self.rect.x + 20,self.rect.y - 50,60,60,5)
            bullets.append(bullet)


class Enemy(GameSprite):

    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > ALTO + 20:
            self.rect.y = 0


jugador = Player('rocket.png',300,350,50,50,7)
enemigos = []

for i in range(randint(4, 11)):
    tmspeed = randint(1,7)
    tmpx = randint(0,ANCHO)
    enemigo = Enemy('ufo.png',tmpx,0,50,50,tmspeed)
    enemigos.append(enemigo)



background = transform.scale(image.load ('galaxy.jpg'),(ANCHO,ALTO))

game_over = False

while not game_over:
    for evento in event.get():
        if evento.type == quit:
            game_over = True

    pantalla.blit(background,(0,0))

    jugador.moves()
    jugador.reset()
    jugador.shoot()

    for enemy in enemigos:
        enemy.reset()
        enemy.moveDown()

        for bullet in bullets:
            bullet.reset()
            bullet.moveUP()

            if bullet.iscollision(enemy):
                if enemy in enemigos:
                    enemigo.remove (enemy)
        

        if enemy.iscollision(jugador):
            print('perdite')


    display.update()
    reloj.tick(FPS)