#===importations========================================================================================================
from level import Level
from player import Player
import pygame,sys
from settings import *
#===fin importations====================================================================================================


#===class Game==========================================================================================================
class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.__screen = pygame.display.set_mode((32*15, 500))
        self.__title = pygame.display.set_caption("Bomberman")
        self.__clock = pygame.time.Clock()
        self.__level = Level()
        self.__pressed1 = False
        self.__pressed2 = False
        self.__lock1 = False
        self.__lock2 = False
        self.__draw_col = False


        self.__posx_start = [32*POS_START_1[0],32*POS_START_2[0]]
        self.__posy_start = [32*POS_START_1[1],32*POS_START_2[1]]

        self.__player1 = Player(self.__posy_start[0],self.__posx_start[0])
        self.__player2 = Player(self.__posy_start[1],self.__posx_start[1])

        self.__bombes1 = self.list_bombe1()
        self.__bombes2 = self.list_bombe2()

        self.__bombe_collision1 = []
        self.__bombe_collision2 = []

        self.__explosion1 = self.list_explosion1()
        self.__explosion2 = self.list_explosion1()


#___création des listes_________________________________________________________________________________________________
    #___sprites des bombes / positions des bombes
    def list_bombe1(self):
        list = []
        for bombe in self.__player1.bombe():
            list.append((bombe.sprite(),(bombe.posy(),bombe.posx())))
        return list

    def list_bombe2(self):
        list = []
        for bombe in self.__player2.bombe():
            list.append((bombe.sprite(),(bombe.posy(),bombe.posx())))
        return list

    #___collisions des bombes
    def list_bombe1_col(self):
        return self.__player1.bombe_col()

    def list_bombe2_col(self):
        return self.__player2.bombe_col()

    #___sprites des explosion / positions des explosions
    def list_explosion1(self):
        list = []
        for explosion in self.__player1.explosion():
            for sprite in explosion.sprite():
                list.append((sprite[0], (sprite[1][1] * 32, sprite[1][0] * 32)))
        return list

    def list_explosion2(self):
        list = []
        for explosion in self.__player2.explosion():
            for sprite in explosion.sprite():
                list.append((sprite[0], (sprite[1][1] * 32, sprite[1][0] * 32)))
        return list

# ___updates____________________________________________________________________________________________________________
    #___playeurs
    def update_players(self):
        self.__player1.update(self.__pressed1,self.__lock1
                              )
        self.__player2.update(self.__pressed2,self.__lock2)
        for wall in self.__level.update_collision():
            rect = [wall[2] * 32, wall[1] * 32,32,32]
            self.__player1.collision(rect)
            self.__player2.collision(rect)
        for rect in self.__bombe_collision1:
            self.__player1.collision(rect)
        for rect in self.__bombe_collision2:
            self.__player2.collision(rect)

    #___dessin
    def update_draw(self):
        for i in range(len(PLATEAU)):
            for j in range(len(PLATEAU[0])):
                self.__level.display_surface.blit(self.__level.sprite(self.__level.valeur(i, j)),
                                                  (j * 32 + 0, i * 32 + 0))
                if self.__draw_col:
                    if self.__level.valeur(i,j) != 0:
                        pygame.draw.rect(self.__screen, "black", (j*32,i*32,32,32),3)

        for bombe1 in self.__bombes1:
            self.__level.display_surface.blit(bombe1[0],bombe1[1])
        for bombe2 in self.__bombes2:
            self.__level.display_surface.blit(bombe2[0],bombe2[1])

        for explosion in self.__explosion1:
            self.__level.display_surface.blit(explosion[0],explosion[1])
        for explosion in self.__explosion2:
            self.__level.display_surface.blit(explosion[0],explosion[1])

        if self.__draw_col:
            for bombe in self.__bombe_collision1:
                pygame.draw.rect(self.__screen, "black", [bombe[0], bombe[1], bombe[2], bombe[3]], 3)
            for bombe in self.__bombe_collision2:
                pygame.draw.rect(self.__screen, "black", [bombe[0], bombe[1], bombe[2], bombe[3]], 3)

        self.__level.display_surface.blit(self.__player1.image(self.__pressed1,self.__lock1),
                                          (self.__player1.posy(), self.__player1.posx()))
        self.__level.display_surface.blit(self.__player2.image(self.__pressed2,self.__lock2),(self.__player2.posy(), self.__player2.posx()))

        if self.__draw_col:
            pygame.draw.rect(self.__screen,"red",self.__player1.hitbox(),3)
            pygame.draw.rect(self.__screen,"red",self.__player2.hitbox(),3)

    #__mur qui ce cassent
    def update_wall(self):
        for i in range(len(PLATEAU)):
            for j in range(len(PLATEAU[0])):
                for explosion in self.__player1.explosion():
                    for sprite in explosion.sprite():
                        if len(sprite) != 0:
                            if sprite[1] == (i,j) or sprite[1] == (i,j):
                                if self.__level.valeur(i,j) == 3:
                                    self.__level.wall_break(i,j)
                for explosion in self.__player2.explosion():
                    for sprite in explosion.sprite():
                        if len(sprite) != 0:
                            if sprite[1] == (i,j) or sprite[1] == (i,j):
                                if self.__level.valeur(i, j) == 3:
                                    self.__level.wall_break(i, j)

# ___run du scripte avec la boucle principale___________________________________________________________________________
    def run(self):
        while True:
            keys = pygame.key.get_pressed()

            # move player 1
            self.__pressed1 = False
            if not self.__lock1:
                if keys[pygame.K_z]:
                    self.__player1.get_sens("top")
                    self.__pressed1 = True
                if keys[pygame.K_s]:
                    self.__player1.get_sens("bottom")
                    self.__pressed1 = True
                if keys[pygame.K_d]:
                    self.__player1.get_sens("right")
                    self.__pressed1 = True
                if keys[pygame.K_q]:
                    self.__player1.get_sens("left")
                    self.__pressed1 = True



            #move player 2
            self.__pressed2 = False
            if not self.__lock2:
                if keys[pygame.K_UP]:
                    self.__player2.get_sens("top")
                    self.__pressed2 = True
                if keys[pygame.K_DOWN]:
                    self.__player2.get_sens("bottom")
                    self.__pressed2 = True
                if keys[pygame.K_RIGHT]:
                    self.__player2.get_sens("right")
                    self.__pressed2 = True
                if keys[pygame.K_LEFT]:
                    self.__player2.get_sens("left")
                    self.__pressed2 = True




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if self.__player1.pose_possible() and not self.__lock1:
                            self.__player1.create_bombe()
                    if event.key == pygame.K_m:
                        if self.__player2.pose_possible() and not self.__lock2:
                            self.__player2.create_bombe()
                    if event.key == pygame.K_v:
                        if self.__draw_col:
                            self.__draw_col = False
                        else:
                            self.__draw_col = True

            if self.__player1.is_dead(self.__explosion1,self.__explosion2):
                self.__lock1 = True
            if self.__player2.is_dead(self.__explosion1,self.__explosion2):
                self.__lock2 = True

            self.__player1.update_bombe()
            self.__player2.update_bombe()

            self.__bombes1 = self.list_bombe1()
            self.__bombes2 = self.list_bombe2()

            self.__bombe_collision1 = self.list_bombe1_col()
            self.__bombe_collision2 = self.list_bombe2_col()

            self.__explosion1 = self.list_explosion1()
            self.__explosion2 = self.list_explosion2()

            self.__screen.fill('white')
            self.update_players()

            self.update_wall()
            #affichage
            self.update_draw()

            pygame.display.update()
            self.__clock.tick(60)
#===fin class Game======================================================================================================


#===lancement du jeu====================================================================================================
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
#===fin lancement du jeu================================================================================================
