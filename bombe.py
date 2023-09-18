#===importaions=========================================================================================================
import pygame
#===fin importation=====================================================================================================

#===class Bombe=========================================================================================================
class Bombe:
    def __init__(self, posx, posy):
        pygame.init()
        self.__posy = posy
        self.__posx = posx
        self.__sprite = pygame.image.load("Images/items/bombe/bombe.png").convert_alpha()
        self.__timer = 60 * 5

#___juste les return simple_____________________________________________________________________________________________
    def posx(self):
        return self.__posx // 32 * 32

    def posy(self):
        return self.__posy // 32 * 32

    def sprite(self):
        return self.__sprite

    def hitbox(self):
        return [self.posy(), self.posx(), 32, 32]

    def case(self):
        return self.posy() // 32, self.posx() // 32

#___vérifications_______________________________________________________________________________________________________
    def hitbox_on(self, tuple):
        if self.case() == tuple:
            return False
        return True

    def update_timer(self):
        if self.__timer != 0:
            self.__timer -= 1

    def explosion(self):
        if self.__timer == 0:
            return True
        return False


#===fin class Bombe=====================================================================================================