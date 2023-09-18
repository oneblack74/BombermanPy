#===importations========================================================================================================
from settings import  *
import pygame
#===fin importations====================================================================================================


#===class Level=========================================================================================================
class Level:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.get_surface()

        self.__wall_collision = self.update_collision()
        self.__sprite = self.create_sprite()

#___creation des sprites________________________________________________________________________________________________
    def create_sprite(self):
        list = []
        list.append(pygame.image.load("Images/plateau/ground.png").convert_alpha())
        list.append(pygame.image.load("Images/plateau/wall_in.png").convert_alpha())
        list.append(pygame.image.load("Images/plateau/wall_out.png").convert_alpha())
        list.append(pygame.image.load("Images/plateau/wall_breakable.png").convert_alpha())
        return list

#___revoie des variables du init________________________________________________________________________________________
    def wall_collision(self):
        return self.__wall_collision

    def sprite(self,i):
        return self.__sprite[i]

    def valeur(self, i, j):
        return PLATEAU[i][j]

    def wall_break(self,i,j):
        PLATEAU[i][j] = 0


    def plateau(self,i,j):
        return PLATEAU[i][j]

#___update______________________________________________________________________________________________________________
    def update_collision(self):
        list = []
        for i in range(len(PLATEAU)):
            for j in range(len(PLATEAU[0])):
                if PLATEAU[i][j] != 0:
                    list.append([PLATEAU[i][j],i,j])
        return list
#===fin class Level=====================================================================================================

