#Definir vencedor
#Gerar matriz de cores a cada jogada
#Importar em csv a matriz de cores por jogada do jogador (pode ser em formato de numeros ja) + coordenada x da jogada
#Treinar a rede SOM
# arq = open("nome do arquivo.csv", "w")
#arq.write(str())
#arq.close()

import pygame
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
from sys import exit
import numpy as np

pygame.init()
tela = pygame.display.set_mode((720, 480), 0, 32)
circulo = np.empty( (4,7), dtype=object)

class circ:
    def __init__(self, x, y, cor):
        self.cor =  cor
        self.x = x
        self.y = y
    def setColor (self, color):
        self.cor = color
        pygame.draw.circle(tela, color, (self.x,self.y), 48)        
    def move (self, x, y, cor):
        pygame.draw.circle(tela, (0, 0, 0), (self.x,self.y), 48)
        self.x = x
        self.y = y
        pygame.draw.circle(tela, cor, (self.x,self.y), 48)
        
        

class jogador:
    def __init__(self, id):
        self.id = id
        if(id): #jogador real
            self.cor = (0, 255, 255)
        else:
            self.cor = (255, 255, 0)
            
def winner():
    global circulo
    white = (255, 255, 255)
    for i in range (0,3):
        for j in range(0, 7-2):
            if(circulo[i,j].cor == circulo[i,j+1].cor and circulo[i,j].cor == circulo[i,j+2].cor):
                return circulo[i,j].cor
    for j in range (0,7):
        for i in range(0, 3-2):
            if(circulo[i,j].cor == circulo[i+1,j].cor and circulo[i,j].cor == circulo[i+2,j].cor):
                return circulo[i,j].cor
    return white
def desenhar_tabu():
    lin= 3
    cols = 0
    raio = 48
    global circulo
    for i in range(0, 8, 2):
        for j in range(0, 14, 2):
            pygame.draw.circle(tela, (255,255, 255), (raio+j*raio, 480 - raio*i - raio), raio)
            circulo[lin, cols] = circ(raio+j*raio, 480 - raio*i - raio, (255, 255, 255))
            cols= cols +1
            
        cols = 0
        lin = lin -1

def pintar_peca(player, linha, coluna):
    global circulo
    circulo[linha, coluna].setColor(player.cor)
    
def testa_branco(col, jogador):
    global circulo
    white = (255, 255, 255)
    for i in range (3, -1, -1):
        if circulo[i, col].cor == white:
            pintar_peca(jogador, i, col)
            return True
    return False
            

def find_column (coordx):
    global circulo
    for col in range(0, 7):
        if(circulo[1, col].x == coordx):
            print(col)
            return col
        
    
pygame.display.set_caption('Color_Puzzle')

espaco = 0


print(pygame.font.get_fonts())

events = pygame.event.get()
turn = True
desenhar_tabu()
while True: #while da partida
    pessoa = jogador(True)
    computador = jogador(False)
    print(winner())
    if(turn):
        escolha = circ(48,48, pessoa.cor)
        pygame.draw.circle(tela, pessoa.cor, (48, 48), 48)
        
    else:
        escolha = circ(48, 48, computador.cor)
        pygame.draw.circle(tela, computador.cor, (48, 48), 48)
    while True: #While da jogada de cada player
        antes=  turn
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    if(escolha.x < 624):
                        pygame.draw.circle(tela, (0, 0, 0), (escolha.x, escolha.y), 48)
                        escolha.x = escolha.x + 96
                        escolha.move(escolha.x, escolha.y, escolha.cor)                          
     
                elif e.key == pygame.K_LEFT:
                    if(escolha.x >48):
                        pygame.draw.circle(tela, (0, 0, 0), (escolha.x, escolha.y), 48)
                        escolha.x = escolha.x - 96
                        escolha.move(escolha.x, escolha.y, escolha.cor)

                elif (e.key == pygame.K_SPACE):
                   if(turn):
                       player = pessoa
                   else:
                        player = computador

                   if(testa_branco(find_column(escolha.x), player)):
                        pygame.draw.circle(tela, (0, 0, 0), (escolha.x, escolha.y), 48)
                        turn =  not turn
                        
        if (antes is not turn):
            break

    #pygame.display.flip()
    pygame.display.update()