import pygame
from pygame import font
from pygame.locals import *
from pygame.constants import KEYDOWN, QUIT
import time
import random
from pygame.mixer import Sound

tamanho = 30
#background = (255, 0, 255)

class Apple:
    def __init__(self, quadrado):
        self.apple = pygame.image.load("resources/amarelo.jpg").convert()
        self.quadrado = quadrado
        self.x = tamanho*3
        self.y = tamanho*3

    def draw(self):
        self.quadrado.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x= random.randint(0,28) * tamanho #move banana
        self.y= random.randint(0,16) * tamanho # o vezes tamanho faz ficar na pos certa pra funfa



class Snake:
    def __init__(self, quadrado, largura):
        self.largura = largura
        self.quadrado = quadrado
        self.block = pygame.image.load("resources/block.jpg").convert()
    
        self.x = [tamanho]*largura #larg x tamanho = o x
        self.y = [tamanho]*largura
    
        self.direction = "right" #começa andando pra baixo

    def mais_largura(self):
        self.largura += 1
        self.x.append(-1) # para de dar erro no self.x[i] = self.x[i-1]
        self.y.append(-1)

    def draw(self):
        #self.quadrado.fill(background) #cor
        for i in range(self.largura):
            self.quadrado.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()



    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_right(self):
        self.direction = "right"
 
    def move_left(self):
        self.direction = "left"

    def walk(self): #funcao para continuar andando

        for i in range(self.largura -1, 0, -1):      #largura da minhoca serve pra ela ficar grudada
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        if self.direction == "up":
            self.y[0] -= tamanho

        if self.direction == "down":
            self.y[0] += tamanho

        if self.direction == "left":
            self.x[0] -= tamanho

        if self.direction == "right":
            self.x[0] += tamanho
    
        self.draw()


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init() #musica

        music = pygame.mixer.Sound('resources/background2.mp3')
        pygame.mixer.Sound.play(music)

        self.surface = pygame.display.set_mode((854,480)) #tamanho da janela 
        #self.surface.fill(background) #para carregar a img novamente (cor)
        
        self.snake = Snake(self.surface, 1) #a cobrinha e sua quantidade
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()




    def is_collision (self, x1, y1, x2, y2): #colisão
        if x1 == x2:
            if y1 == y2:
                return True
        return False


    def gameplay(self): #pega a colisao e confere se aconteceu ou nao
        self.snake.walk()
        self.apple.draw() 
        self.pontos() 
        self.render() #wallpaper
        
        
        #colisao da banana
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            print('bananas')
            ara = pygame.mixer.Sound('resources/ara ara.mp3') #som da banana
            pygame.mixer.Sound.play(ara) #play som
            self.apple.move()
            self.snake.mais_largura()

        #colisao da cobra
        for i in range(2, self.snake.largura):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                death = pygame.mixer.Sound('resources/death.mp3')
                pygame.mixer.Sound.play(death)
                print('ur gay')
                raise "game_over" #INICIA O GAMEOVER
                
        

    def game_over(self):
        font = pygame.font.SysFont('Anime Ace BB', 30)
        line1 = font.render(f'UR GAY! {self.snake.largura} pontos', True, (255, 255, 255))
        self.surface.blit(line1, (400,250))
        pygame.display.flip()

          
    def restart(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    def pontos(self):
        font = pygame.font.SysFont('Anime Ace BB', 30)
        pontos = font.render(f'pontos: {self.snake.largura}', True, (255, 255, 255))
        self.surface.blit(pontos, (650,10))
        pygame.display.flip()

    def render(self):
        img = pygame.image.load('resources/kurumi19.jpg')
        self.surface.blit(img, (0,0))

    


    def run(self):
        running = True
        pause = False
    
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.gameplay()
            except Exception as e:
                self.game_over()
                pause = True
                self.restart()
            time.sleep(0.2)

game = Game() #abre o game
game.run()

