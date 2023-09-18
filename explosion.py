import pygame
from settings import *


class Explosion:

    def __init__(self, posy, posx, puissance):
        pygame.init()
        self.__posy = posy
        self.__posx = posx
        self.__puissance = puissance
        self.__sprite = self.sprites(self.list_type_explosion())
        self.__timer = 60 * 1/3


    def sprite(self):
        return self.__sprite

    def posx(self):
        return self.__posx // 32 * 32

    def posy(self):
        return self.__posy // 32 * 32

    def case(self):
        return self.posy() // 32, self.posx() // 32

    def update_timer(self):
        if self.__timer != 0:
            self.__timer -= 1

    def explosion_end(self):
        if self.__timer == 0:
            return True
        return False

    def list_type_explosion(self):
        """ type, coord, sens"""
        global increment
        x = self.__posx // 32
        y = self.__posy // 32
        list = []


        for i,sens in enumerate(["mid", "top", "right", "bottom", "left"]):
            list.append([])
            for taille in range(1,self.__puissance+1):
                if sens == "top" or sens == "left":
                    increment = -taille
                elif sens == "right" or sens == "bottom":
                    increment = taille

                if sens == "mid":
                    list[i].append([0, (x,y), "mid"])
                    break

                if sens == "top" or sens == "bottom":
                    if self.pos_explosion_possible(x + increment, y):
                        list[i].append([1, (x + increment, y), sens])
                        if self.mur_1_2(x + increment,y):
                            list[i].pop()
                            break
                        if self.mur_3(x + increment,y):
                            break
                if sens == "left" or sens == "right":
                    if self.pos_explosion_possible(x, y + increment):
                        list[i].append([1, (x, y + increment), sens])
                        if self.mur_1_2(x,y + increment):
                            list[i].pop()
                            break
                        if self.mur_3(x,y + increment):
                            break
        for sens in list:
            if len(sens) != 0 and sens[-1][2] != "mid":
                sens[-1][0] = 2

        return list

    def sprites(self, list_type):
        list = []
        for sens in list_type:
            for pos in sens:
                list.append([self.definir_image(pos[0], pos[2]), pos[1]])
        return list

    def pos_explosion_possible(self,i,j):
        if 0 <= i <= 12 or 0 <= j <= 14:
            return True
        return False

    def mur_3(self,i,j):
        if PLATEAU[i][j] == 3:
            return True
        return False

    def mur_1_2(self,i,j):
        if PLATEAU[i][j] == 1 or PLATEAU[i][j] == 2:
            return True
        return False

    def definir_image(self, type, sens):
        sprite = 0
        if type == 0:
            sprite = pygame.image.load("Images/items/explosion/mid.png").convert_alpha()
        elif type == 1:
            if sens == "top" or sens == "bottom":
                sprite = pygame.image.load("Images/items/explosion/vertical.png").convert_alpha()
            if sens == "right" or sens == "left":
                sprite = pygame.image.load("Images/items/explosion/horizontal.png").convert_alpha()
        elif type == 2:
            sprite = pygame.image.load(f"Images/items/explosion/{sens}.png").convert_alpha()
        return sprite
