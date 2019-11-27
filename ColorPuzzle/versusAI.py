#Definir vencedor |  OK
#Gerar matriz de cores a cada jogada
#Importar em csv a matriz de cores por jogada do jogador (pode ser em formato de numeros ja) + coordenada x da jogada
#Treinar a rede SOM
# arq = open("nome do arquivo.csv", "w")
#arq.write(str())
#arq.close()

import pygame
from pygame.locals import Rect, QUIT
from sys import exit
import numpy as np
import csv
from scipy.spatial import distance
import pandas as pd

neuronios = pd.read_csv("https://raw.githubusercontent.com/lucasboot/ColorPuzzle/master/ColorPuzzle/neuronios.csv")
neuro = neuronios.iloc[:, :-1].values
classes = neuronios.iloc[:,-1]

arq = open("partida.csv", "a")
#writer = csv.writer(arq, delimiter=',', quotechar='|', quoting=csv.)

pygame.init()
tela = pygame.display.set_mode((720, 480), 0, 32)
circulo = np.empty((4,7), dtype=object)

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

def empate(): #ainda nao foi adicionada ao jogo
    global circulo
    sequence = 0
    for i in range(0,4):
        for j in range(0,7):
            if(circulo[i,j].cor != (255, 255, 255)):
                sequence = sequence + 1
    if(sequence == 4*7):
        print("Empatou")
        return True
    else:
        return False
              

def winner():
    global circulo
    white = (255, 255, 255)
    cont = 0
    #Horizontal acho que ok
    for i in range (0,4):
        for j in range(0, 5):
            cont = cont +1
            if((circulo[i,j].cor == circulo[i,j+1].cor) and (circulo[i,j].cor == circulo[i,j+2].cor) and (circulo[i,j].cor != white)):
                return circulo[i,j].cor
            
    #Vertical ok
    for j in range (0,7):
        for i in range(0, 2):
            if((circulo[i,j].cor == circulo[i+1,j].cor) and (circulo[i,j].cor == circulo[i+2,j].cor) and (circulo[i,j].cor != white)):
                #print("oi")
                return circulo[i,j].cor
    #Diagonais
    for i in range(0, 4): 
        for j in range(0, 7):
            if(j + 2 <= 6 and i+2  <= 3):
                if((circulo[i,j].cor == circulo[i+1,j+1].cor) and (circulo[i,j].cor == circulo[i+2,j+2].cor) and (circulo[i,j].cor != white)):
                    return circulo[i,j].cor
            if(j+2 <= 6 and i-2 >=0):
                if((circulo[i,j].cor == circulo[i-1,j+1].cor) and (circulo[i,j].cor == circulo[i-2,j+2].cor) and (circulo[i,j].cor != white)):
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
    '''
    if(jogador.cor == (255, 255, 0)): #amarelo para ciano (0, 255, 255)
        for i in range (0, 4):
            for j in range(0,7):
                if (circulo[i,j].cor == (255, 255, 255)):
                    cor = 0
                elif(circulo[i,j].cor == (255, 255, 0)):
                    cor = 1
                else:
                    cor = 2
                arq.write(str(cor) + ", ")
        arq.write(str(col))
        arq.write("\n")
        '''    
    for i in range (3, -1, -1):
        if circulo[i, col].cor == (255, 255, 255):
            pintar_peca(jogador, i, col)
            return True
    return False
            

def find_column (coordx):
    global circulo
    for col in range(0, 7):
        if(circulo[1, col].x == coordx):
            #print(col)
            return col
        
    
pygame.display.set_caption('Color_Puzzle')

espaco = 0


print(pygame.font.get_fonts())

events = pygame.event.get()
turn = True
desenhar_tabu()
while not (empate()): 
    pessoa = jogador(True)
    computador = jogador(False)
    cabou= winner()
    if(cabou == (255, 255, 0)):
       print("O amarelo venceu")
       arq.close()
       pygame.quit()
       exit()       
       
    elif (cabou == (0,255,255)):
        print("O ciano venceu")
        arq.close()
        pygame.quit()
        exit()        
        
    #print(winner())
    if(turn):
        escolha = circ(48,48, pessoa.cor)
        pygame.draw.circle(tela, pessoa.cor, (48, 48), 48)
        
    else:
        escolha = circ(48, 48, computador.cor)
        pygame.draw.circle(tela, computador.cor, (48, 48), 48)
    while True: #While da jogada de cada player
        antes=  turn
        pygame.display.update()
        if(turn):
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
                           player = pessoa
                           if(testa_branco(find_column(escolha.x), player)):
                               pygame.draw.circle(tela, (0, 0, 0), (escolha.x, escolha.y), 48)
                               turn = not turn
                               
                           
        else:
             player = computador
             jogada = np.empty((1, 28), dtype=object)
             cont = 0
             for i in range (0,4):
                 for j in range (0, 7):
                     if (circulo[i,j].cor == (255, 255, 255)):
                         cor = 0
                     elif(circulo[i,j].cor == (255, 255, 0)):
                         cor = 1
                     else:
                         cor = 2                                
                     jogada[0, cont] = cor
                     cont = cont +1
             distancias = np.empty((64,1), dtype=object)
             for k in range (64):
                 #distancias.append(distance.euclidean(neuro[k, :],distancias))
                 distancias[k, 0] = distance.euclidean(neuro[k, :],jogada[0, :])
             menor = distancias[0,0]
             indice = k

             for i in range (64):
                 if(distancias[i,0] < menor):
                     menor = distancias[i,0]
                     indice = i
             col = classes[indice]
             print(col)

             if(testa_branco(find_column(col), player)):
                 pygame.draw.circle(tela, (0, 0, 0), (escolha.x, escolha.y), 48)
                 turn =  not turn                                 
    
        
        if (antes is not turn):
            break

    #pygame.display.flip()
    pygame.display.update()