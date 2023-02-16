import pygame as pg

class Game(): #Game class acts as framework for the game
    def __init__(self): #Constructor for game class and runs at start of game
        pg.init()
        self.init_variables()
        self.init_spritegroups()
        self.load_images()
        self.init_objects()
        self.screen_setup()
        self.gameloop()

    def init_variables(self):
        self.running = True
        self.clock = pg.time.Clock()
        self.toggle = False

    def init_spritegroups(self):
        self.player_sg = pg.sprite.Group()
        self.all_sg = pg.sprite.Group()

    def init_objects(self):
        self.player = Player(self)
        self.all_sg.add(self.player)
        self.player_sg.add(self.player)

    def load_images(self):
        pass

    def screen_setup(self): #Set up screen
        pg.display.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

    def gameloop(self): #Main loop that will run while running program
        while self.running == True:
            def events(): #Controls all inputs
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        pg.quit()
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.running = False
                            pg.quit()

            def draw():
                self.screen.fill(BLACK)
                self.player_sg.draw(self.screen)

                #Draw grid (temporary)
                for i in range (0, WIDTH, TILESIZE):
                    pg.draw.line(self.screen,(50,50,50), (i,0), (i,HEIGHT))
                for i in range (0, HEIGHT, TILESIZE):
                    pg.draw.line(self.screen,(50,50,50), (0,i), (WIDTH,i))

            def update():
                self.all_sg.update()
                self.clock.tick(FPS)
                pg.display.update()
            
            #Methods to call continuously:
            events()       
            draw()
            update()

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = 0
        self.image = pg.Surface((32,32))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.yspeed = 4
        self.xspeed = 4

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.rect.y -= self.yspeed
        if keys[pg.K_a]:
            self.rect.x -= self.xspeed
        if keys[pg.K_s]:
            self.rect.y += self.yspeed
        if keys[pg.K_d]:
            self.rect.x += self.xspeed

#Constants:
FPS = 60
TILESIZE = 32
WIDTH = 320 + TILESIZE*3
HEIGHT = 320
BLACK = (0,0,0)
RED = (255,0,0)

#Create game instance
game = Game()                                               