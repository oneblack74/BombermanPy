import pygame
from bombe import Bombe
from explosion import Explosion

class Player():

    def __init__(self, posx, posy):
        #___posisions
        self.__posy = posy
        self.__posx = posx - 18

        #___sprites
        self.__sprites_still = self.still()
        self.__sprites_walk = self.walk()
        self.__sprite_dead = self.sprite_dead()

        #___id des prites
        self.__walk_id = 0
        self.__dead_id = 0

        #___compteurs
        self.__compteur_sprite = 0
        self.__compteur_sprite_dead = 0

        #___listes
        self.__hitbox = self.hitbox()
        self.__bombe = []
        self.__explosion = []
        self.__bombe_collision = []

        #___variables
        self.__bombe_max = 3
        self.__bombe_restante = 0
        self.__puissance = 2
        self.__vitesse = 2
        self.__dead = False
        self.__end = False
        self.__sens = "right"

#___renvoie des variables du init_______________________________________________________________________________________
    def explosion(self):
        return self.__explosion

    def dead(self):
        return self.__dead

    def bombe(self):
        return self.__bombe

    def bombe_col(self):
        return self.__bombe_collision

    def hitbox(self):
        return [self.__posy + 1, self.__posx + 19, 30, 30]

    def image(self, pressed, dead):
        if pressed:
            return self.__sprites_walk[self.__sens][self.__walk_id]
        if dead:
            return self.__sprite_dead[self.__dead_id]
        return self.__sprites_still[self.__sens]

    def posy(self):
        return self.__posy

    def posx(self):
        return self.__posx

    def case(self):
        posy = self.__posy + 16
        posx = self.__posx + 34
        return posy // 32, posx // 32

#___création des listes/dico des sprites________________________________________________________________________________
    def still(self):
        dico = {}
        dico["top"] = pygame.image.load("Images/bombardier/still/top.png").convert_alpha()
        dico["bottom"] = pygame.image.load("Images/bombardier/still/bottom.png").convert_alpha()
        dico["right"] = pygame.image.load("Images/bombardier/still/right.png").convert_alpha()
        dico["left"] = pygame.image.load("Images/bombardier/still/left.png").convert_alpha()
        return dico

    def walk(self):
        dico = {}

        #bottom
        list = []
        for i in range(6):
            list.append(pygame.image.load(f"Images/bombardier/walk/bottom_{i}.png").convert_alpha())
        dico["bottom"] = list

        #top
        list = []
        for i in range(6):
            list.append(pygame.image.load(f"Images/bombardier/walk/top_{i}.png").convert_alpha())
        dico["top"] = list

        #right
        list = []
        for i in range(6):
            list.append(pygame.image.load(f"Images/bombardier/walk/right_{i}.png").convert_alpha())
        dico["right"] = list

        #left
        list = []
        for i in range(6):
            list.append(pygame.image.load(f"Images/bombardier/walk/left_{i}.png").convert_alpha())
        dico["left"] = list

        return dico


    def sprite_dead(self):
        list = []
        for i in range(6):
            list.append(pygame.image.load(f"Images/bombardier/dead/{i}.png").convert_alpha())
        return list

#___conditions / vérifications__________________________________________________________________________________________
    def pose_possible(self):
        if self.__bombe_restante == 0:
            return False
        for bombe in self.__bombe:
            if bombe.case() == self.case():
                return False
        return True

    def is_dead(self, explo1, explo2):

        for case_explosion in explo1:
            case = (case_explosion[1][0] // 32, case_explosion[1][1] // 32)
            if case == self.case():
                return True
        for case_explosion in explo2:
            case = (case_explosion[1][0] // 32, case_explosion[1][1] // 32)
            if case == self.case():
                return True
        return False

#___id__________________________________________________________________________________________________________________
    def walk_id(self):

        if self.__walk_id >= 5:
            self.__walk_id = 0
        else:
            self.__walk_id += 1

    def dead_id(self):
        if self.__dead_id == 5:
            self.__end = True
        if not self.__end:
            if self.__dead_id >= 5:
                self.__dead_id = 0
            else:
                self.__dead_id += 1

#___compteurs___________________________________________________________________________________________________________
    def compteur_sprite(self):
        if self.__compteur_sprite >= 5:
            self.__compteur_sprite = 0
        else:
            self.__compteur_sprite += 1

    def compteur_sprite_dead(self, dead):
        if dead:

            if self.__compteur_sprite_dead == 10:
                self.__compteur_sprite_dead = 0
            else:
                self.__compteur_sprite_dead += 1

#___collisions__________________________________________________________________________________________________________
    def collision(self,histbox_wall):
        """hitbox_wall --> y, x, taille, taille
        coin --> haut gauche, haut droit, bas gauche, bas droit
        if haut gauche < i + taille and haut droit < i + taille

        """
        #coin player
        hitbox_player = self.hitbox()
        y = hitbox_player[0]
        x = hitbox_player[1]
        t_y = hitbox_player[2]
        t_x = hitbox_player[3]
        coin_player = [(y, x), (y, x + t_x), (y + t_y, x), (y + t_y, x + t_x)]


        #coin wall
        y = histbox_wall[0]
        x = histbox_wall[1]
        t_y = histbox_wall[2]
        t_x = histbox_wall[3]
        coin_wall = [(y, x), (y, x + t_x), (y + t_y, x), (y + t_y, x + t_x)]

        #haut gauche et haut droit vers le haut
        if self.__sens == "top":
            if coin_player[0][1] < coin_wall[1][1] and coin_player[0][1] > coin_wall[2][1] and coin_player[0][0] >= coin_wall[1][0] and coin_player[0][0] <= coin_wall[2][0] or coin_player[2][1] < coin_wall[1][1] and coin_player[2][1] > coin_wall[2][1] and coin_player[2][0] >= coin_wall[1][0] and coin_player[2][0] <= coin_wall[2][0]:
                self.__posx += self.__vitesse

        # bas gauche et bas droit vers le bas
        if self.__sens == "bottom":
            if coin_player[1][1] > coin_wall[0][1] and coin_player[1][1] < coin_wall[1][1] and coin_player[1][0] >= coin_wall[0][0] and coin_player[1][0] <= coin_wall[2][0] or coin_player[3][1] > coin_wall[0][1] and coin_player[3][1] < coin_wall[1][1] and coin_player[3][0] >= coin_wall[0][0] and coin_player[3][0] <= coin_wall[2][0]:
                self.__posx -= self.__vitesse

        #haut gauche et bas gauche vers gauche
        if self.__sens == "left":
            if coin_player[0][0] < coin_wall[2][0] and coin_player[0][0] > coin_wall[0][0] and coin_player[0][1] >= coin_wall[0][1] and coin_player[0][1] <= coin_wall[1][1] or coin_player[1][0] < coin_wall[2][0] and coin_player[1][0] > coin_wall[0][0] and coin_player[1][1] >= coin_wall[0][1] and coin_player[1][1] <= coin_wall[1][1]:
                self.__posy += self.__vitesse

        #haut droit et bas droit vers la droite
        if self.__sens == "right":
            if coin_player[2][0] > coin_wall[0][0] and coin_player[2][0] < coin_wall[2][0] and coin_player[2][1] >= coin_wall[0][1] and coin_player[2][1] <= coin_wall[1][1] or coin_player[3][0] > coin_wall[0][0] and coin_player[3][0] < coin_wall[2][0] and coin_player[3][1] >= coin_wall[0][1] and coin_player[3][1] <= coin_wall[1][1]:
                self.__posy -= self.__vitesse

        if self.__sens == "top":
            if coin_wall[1][1] > coin_player[0][1] > coin_wall[2][1] and coin_wall[2][0] > coin_player[0][0] > coin_wall[2][0] - 16:
                self.__posy += self.__vitesse
            if coin_wall[2][1] < coin_player[2][1] < coin_wall[1][1] and coin_wall[2][0] - 16 > coin_player[2][0] > coin_wall[0][0]:
                self.__posy -= self.__vitesse
        if self.__sens == "bottom":
            if coin_wall[1][1] > coin_player[1][1] > coin_wall[2][1] and coin_wall[2][0] > coin_player[0][0] > coin_wall[2][0] - 16:
                self.__posy += self.__vitesse
            if coin_wall[2][1] < coin_player[3][1] < coin_wall[1][1] and coin_wall[2][0] - 16 > coin_player[2][0] > coin_wall[0][0]:
                self.__posy -= self.__vitesse
        if self.__sens == "left":
            if coin_wall[1][0] < coin_player[0][0] < coin_wall[3][0] and coin_wall[3][1] > coin_player[0][1] > coin_wall[2][1] + 16:
                self.__posx += self.__vitesse
            if coin_wall[1][0] < coin_player[0][0] < coin_wall[3][0] and coin_wall[2][1] < coin_player[1][1] < coin_wall[2][1] + 16:
                self.__posx -= self.__vitesse
        if self.__sens == "right":
            if coin_wall[1][0] < coin_player[2][0] < coin_wall[3][0] and coin_wall[0][1] + 16 < coin_player[2][1] < coin_wall[1][1]:
                self.__posx += self.__vitesse
            if coin_wall[1][0] < coin_player[2][0] < coin_wall[3][0] and coin_wall[0][1] < coin_player[3][1] < coin_wall[1][1] - 16:
                self.__posx -= self.__vitesse

#___déplacement_________________________________________________________________________________________________________
    def move(self):
        if self.__sens == "top":
            self.__posx -= self.__vitesse
        elif self.__sens == "bottom":
            self.__posx += self.__vitesse
        elif self.__sens == "right":
            self.__posy += self.__vitesse
        elif self.__sens == "left":
            self.__posy -= self.__vitesse


#___updates_____________________________________________________________________________________________________________
    def update_collision_bombe(self):
        list = []
        for bombe in self.__bombe:
            if bombe.case() != self.case():
                list.append(bombe.hitbox())
        return list

    def update(self, pressed, dead):
        self.compteur_sprite()
        self.compteur_sprite_dead(dead)
        if self.__compteur_sprite == 0:
            self.walk_id()
        if pressed:
            self.move()
        if dead and self.__compteur_sprite_dead == 10 and not self.__end:
            self.dead_id()
        self.hitbox()

    def update_bombe(self):
        self.__bombe_restante = self.__bombe_max - len(self.__bombe)
        if len(self.__bombe) != 0:
            if self.__bombe[0].explosion():
                self.__explosion.append(Explosion(self.__bombe[0].posy(), self.__bombe[0].posx(), self.__puissance))
                self.__bombe.pop(0)
        if len(self.__explosion) != 0:
            if self.__explosion[0].explosion_end():
                self.__explosion.pop(0)
        for bombe in self.__bombe:
            bombe.update_timer()
        for explosion in self.__explosion:
            explosion.update_timer()
        self.__bombe_collision = self.update_collision_bombe()

#___modifier une variable du init_______________________________________________________________________________________
    def get_sens(self, new_sens):
        self.__sens = new_sens

#___creer une bombe_____________________________________________________________________________________________________
    def create_bombe(self):
        self.__bombe.append(Bombe(self.__posx + 34, self.__posy + 16))
        self.__bombe_restante -= 1














