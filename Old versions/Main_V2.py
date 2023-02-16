import pygame as pg
import csv


class Game(): #Game class acts as framework for the game
    def __init__(self): #Constructor for game class and runs at start of game
        pg.init()
        self.init_variables()
        self.init_spritegroups()
        self.load_images()
        self.game_text()
        self.init_objects()
        self.screen_setup()
        self.new_room(self.roomx,self.roomy)
        self.gameloop()

    def init_variables(self):
        self.running = True
        self.clock = pg.time.Clock()
        self.roomx = 0
        self.roomy = 0
        self.border_colour = (100,100,100)
        self.showtextbox = False

        self.current_time = 0 #By default game time is 0
        self.timepoint = 0 #Point in time for an event default to 0
        self.timepassed = 0 #Time elapsed from timepoint to current time default 0
        self.timelock = False #lock used to instantaneously get a timepoint

        self.phase = 0 #Refers to the stage of the game

        self.font35 = pg.font.SysFont("Aerial", 35)
        self.font25 = pg.font.SysFont("Aerial", 25)
        self.textcount = 0 #Used to cycle through textbox pages

        self.action = False #Toggle for when action key is pressed

    def init_spritegroups(self):
        self.player_sg = pg.sprite.Group() #Player only
        self.all_sg = pg.sprite.Group() #All sprites (used to update all sprites)

        self.floor_sg = pg.sprite.Group() #Floor tile sprite group
        self.wall_sg = pg.sprite.Group() #Wall tile sprite group

        self.border_sg = pg.sprite.Group() #Sprite group for border tiles
        self.textbox_sg = pg.sprite.Group() #Group for all textbox components

    def init_objects(self):
        self.player = Player(self,2*TILESIZE,2*TILESIZE)
        self.all_sg.add(self.player)
        self.player_sg.add(self.player)

    def load_images(self):
        #Player images
        self.p_d_animate = [] #Packet of frames for down animation
        self.p_d_animate.append(pg.image.load("Player/PlayerAnimation/p_d_1.png"))
        self.p_d_animate.append(pg.image.load("Player/PlayerAnimation/p_d_2.png"))
        self.p_d_animate.append(pg.image.load("Player/PlayerAnimation/p_d_3.png"))
        self.p_d_animate.append(pg.image.load("Player/PlayerAnimation/p_d_4.png"))
        self.p_l_animate = [] #Packet of frames for left animation
        self.p_l_animate.append(pg.image.load("Player/PlayerAnimation/p_l_1.png"))
        self.p_l_animate.append(pg.image.load("Player/PlayerAnimation/p_l_2.png"))
        self.p_l_animate.append(pg.image.load("Player/PlayerAnimation/p_l_3.png"))
        self.p_l_animate.append(pg.image.load("Player/PlayerAnimation/p_l_4.png"))
        self.p_r_animate = [] #Packet of frames for right animation
        self.p_r_animate.append(pg.image.load("Player/PlayerAnimation/p_r_1.png"))
        self.p_r_animate.append(pg.image.load("Player/PlayerAnimation/p_r_2.png"))
        self.p_r_animate.append(pg.image.load("Player/PlayerAnimation/p_r_3.png"))
        self.p_r_animate.append(pg.image.load("Player/PlayerAnimation/p_r_4.png"))
        self.p_u_animate = [] #Packet of frames for up animation
        self.p_u_animate.append(pg.image.load("Player/PlayerAnimation/p_u_1.png"))
        self.p_u_animate.append(pg.image.load("Player/PlayerAnimation/p_u_2.png"))
        self.p_u_animate.append(pg.image.load("Player/PlayerAnimation/p_u_3.png"))
        self.p_u_animate.append(pg.image.load("Player/PlayerAnimation/p_u_4.png"))

        #UI images
        self.textbox_img = pg.image.load("UI/textbox.png")
        
    def screen_setup(self): #Set up screen
        pg.display.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        icon = pg.image.load("Tiles/tile40.png")
        pg.display.set_icon(icon)
        pg.display.set_caption("MINI RPG")

        self.create_border()

    def create_border(self):
        #Black Border
        tile_image = pg.image.load("Tiles/tile0.png")
        #Top and bottom horizontal black lines
        for x in range(0, WIDTH, TILESIZE):
            new_tile = Tile(x,0,tile_image)
            self.border_sg.add(new_tile)
            new_tile = Tile(x,HEIGHT-TILESIZE,tile_image)
            self.border_sg.add(new_tile)

        #Left and right vertical black lines
        for y in range(0, HEIGHT, TILESIZE):
            new_tile = Tile(0,y,tile_image)
            self.border_sg.add(new_tile)
            new_tile = Tile(WIDTH-TILESIZE,y,tile_image)
            self.border_sg.add(new_tile)

    def onscreen_text(self,colour1,title,x1,y1,colour2,text,x2,y2):
        self.titletext_surface = self.font35.render(title,True,colour1)
        self.text_surface = self.font25.render(text,True,colour2)
        self.titletext_x = x1
        self.titletext_y = y1
        self.text_x = x2
        self.text_y = y2

    def draw_tiles(self,roomx,roomy):  
        #Clear old tiles
        self.floor_sg.empty()
        self.wall_sg.empty()

        #Add tiles to sprite groups
        self.layers = ["MAP_Floors.csv", "MAP_Walls.csv"] #Layers of the tilemap
        
        for layer in self.layers: #Go through all layers
            csv_file = open(layer,"r") #Open file
            data = csv.reader(csv_file) #Read as a csv file
            
            for ypos, yvalue in enumerate(data): #For every row in data and return the index of each row in variable called y
                if ypos >= roomy*11 and ypos < (11 + roomy*11): #If y index (row position) between the 11 rows wanted:

                    for xpos, xvalue in enumerate(yvalue): #For every tile in row and return the index of each tile in variable called x
                        if xpos >= roomx*14 and xpos < (14 + roomx*14): #If x index (tile position) between the 14 rows wanted:
                            
                            tile = xvalue
                            if tile != "-1": #If tile is not an empty space:
                                image = pg.image.load("Tiles/tile"+ tile +".png") #Image is the file matching the tile number with the filename

                                #create new tile(border space + tilepos*size subtracting this to map any room back into the 0,0 postition essentially, same maths for y location)
                                new_tile = Tile(TILESIZE + (TILESIZE*xpos) - roomx*11*TILESIZE, TILESIZE + (TILESIZE*ypos) - roomy*11*TILESIZE, image) #Create new tile

                                if layer == "MAP_Walls.csv": #If on wall layer:
                                    self.wall_sg.add(new_tile) #Classify this new tile as a wall tile
                                if layer == "MAP_Floors.csv": #If on floor layer
                                    self.floor_sg.add(new_tile) #Classify this new tile as a floor tile
                                                               
    def new_room(self,roomx,roomy):
        self.draw_tiles(roomx,roomy)
    
    def game_text(self): #Loads text used in textboxes
        self.gametext1 = []
        self.gametext1.append("Welcome, test subject 48")
        self.gametext1.append("Use the WASD keys to move around")
    
    def timer(self,delay):
        if self.timelock == False:
            self.timepoint = pg.time.get_ticks()
            self.timelock = True
        if self.timepassed > delay:
            self.timelock = False
            return True

    def open_textbox(self,colour1,title,x1,y1,colour2,text_array,x2,y2): #Textbox setup requiring parameters for the title and the text
        self.player.movelock = True
        self.showtextbox = True

        self.onscreen_text(colour1, title, x1, y1, colour2, text_array[self.textcount], x2, y2)
        if self.action == True: #If action key pressed
            if self.textcount < len(text_array) - 1: #If count less than 1 minus the length of the text array
                self.textcount += 1 #Increment count
            else:
                self.textcount = 0 #Reset count
                self.clear_textbox() 
                return True
        print(self.textcount,self.action)
        
    def clear_textbox(self):
        self.showtextbox = False
        self.onscreen_text(BLACK,"",0,0,BLACK,"",0,0) #No text
        self.player.movelock = False

    def chunk_event(self,x,y):
        if x == 0 and y == 0: #ROOM 0,0
            if self.phase == 0:
                if self.timer(2000):
                    self.phase = 1
            if self.phase == 1:
                if self.open_textbox(BLACK, "???", TILESIZE*3, TILESIZE*7, BLACK, self.gametext1, TILESIZE*2.5, TILESIZE*8.5):
                    self.phase = 2
                 
    def gameloop(self): #Main loop that will run while running program
        while self.running == True:
            def events(): #Controls all inputs
                for event in pg.event.get():
                    if event.type == pg.QUIT: #Quit game if X of window pressed
                        self.running = False
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE: #Quit game if esc key pressed
                            self.running = False
                            pg.quit()
                    
                        if event.key == pg.K_o:
                                self.action = True

            if self.action == True:
                self.action = False
                        
            def draw_all():
                #Draw background of screen
                self.screen.fill(GREY)
                
                #Draw sprites
                self.floor_sg.draw(self.screen)
                self.player_sg.draw(self.screen)
                self.wall_sg.draw(self.screen)


                #Draw textbox
                if self.showtextbox == True:
                    self.screen.blit(self.textbox_img,(TILESIZE*1.5,TILESIZE*6.5))
                    self.screen.blit(self.titletext_surface,(self.titletext_x, self.titletext_y))
                    self.screen.blit(self.text_surface,(self.text_x, self.text_y))

       

                #Draw grid (TEMP)
                #for i in range (0, WIDTH, TILESIZE):
                    #pg.draw.line(self.screen,(50,50,50), (i,0), (i,HEIGHT))
                #for i in range (0, HEIGHT, TILESIZE):
                    #pg.draw.line(self.screen,(50,50,50), (0,i), (WIDTH,i))

                #Border
                self.border_sg.draw(self.screen)

                #Border edge lines
                pg.draw.line(self.screen, self.border_colour, (TILESIZE,TILESIZE), (TILESIZE,HEIGHT-TILESIZE))
                pg.draw.line(self.screen, self.border_colour, (TILESIZE,HEIGHT-TILESIZE), (WIDTH-TILESIZE,HEIGHT-TILESIZE))
                pg.draw.line(self.screen, self.border_colour, (WIDTH-TILESIZE,TILESIZE), (WIDTH-TILESIZE,HEIGHT-TILESIZE))
                pg.draw.line(self.screen, self.border_colour, (TILESIZE,TILESIZE), (WIDTH-TILESIZE, TILESIZE))

            def update():
                self.all_sg.update()
                self.clock.tick(FPS)
                pg.display.update()
            
            #Methods to call continuously:
            events()       
            draw_all()
            update()
            self.chunk_event(self.roomx,self.roomy)
            
            #Time in frames of the game
            self.current_time = pg.time.get_ticks()
            self.timepassed = self.current_time - self.timepoint
    
            #print(self.current_time,self.timepoint,self.timepassed,self.timelock,self.roomx,self.roomy,self.player.movelock,self.action)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Gives a copy of the game to this class

        self.current_image = 0 #Will be used to time animations
        self.image = self.game.p_d_animate[1] #Start with player frame (down2)
        self.image.set_colorkey(WHITE) #Define transparent background colour of png image

        self.rect = self.image.get_rect()
        self.rect.x = x #Hitbox x pos
        self.rect.y = y #Hitbox y pos

        self.x = x #Player x pos
        self.y = y #Player y pos
        self.dy = 0 #Current yspeed
        self.dx = 0 #Current xspeed 
        self.speed = 2 #Speed increment
        self.direction = 0 #Will change to x or y indicating axis of movement
        self.movelock = True #Will be used to toggle player movement

    def check_wall_collision(self,axis):
        if axis == "x":
            hit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls x?
            if hit:
                if self.dx > 0: #If moving right (x increasing)
                    self.x = hit[0].rect.left - self.rect.width #set player x (left side) to equal the xpos of object hit minus the player width (collision right)
                if self.dx < 0: #If moving left (x decreasing)
                    self.x = hit[0].rect.right #set player x (right side) to equal the xpos of object hit (collision left)
                self.dx = 0 #Else x velocity is 0 as not moving horizontally
                self.rect.x = self.x #Update x rect or "hitbox"
                
        if axis == "y":
            hit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls y?
            if hit:
                if self.dy < 0: #If moving up (y incresing)
                    self.y = hit[0].rect.bottom #set player y (bottom side) to equal the ypos of object hit (collision up)
                if self.dy > 0: #If moving down (y decreasing)
                    self.y = hit[0].rect.top - self.rect.height #set player y (top side) to equal the ypos of object hit minus the player height (collision down)
                self.dy = 0 #Else y velocity is 0 as not moving vertically
                self.rect.y = self.y

    def check_offscreen(self):
        if self.y > HEIGHT - TILESIZE - 5: #If offscreen down:
            self.game.roomy += 1
            self.game.new_room(self.game.roomx, self.game.roomy) #New room with y coordinate +1
            self.y = 6 #Mirror player position on opposite edge of screen 

        if  self.y <= 5: #If offscreen up:
            self.game.roomy -= 1
            self.game.new_room(self.game.roomx, self.game.roomy)
            self.y = HEIGHT - TILESIZE - 6

    def animate(self, direction):
        if direction == "up":
            self.current_image += 0.1
            if self.current_image >= len(self.game.p_u_animate):
                self.current_image = 0
            self.image = self.game.p_u_animate[int(self.current_image)]
            #Defines transparent bg colour for player image
            self.image.set_colorkey(WHITE) 
        if direction == "down":
            self.current_image += 0.1
            if self.current_image >= len(self.game.p_d_animate):
                self.current_image = 0
            self.image = self.game.p_d_animate[int(self.current_image)]
            #Defines transparent bg colour for player image
            self.image.set_colorkey(WHITE) 
        if direction == "left":
            self.current_image += 0.1
            if self.current_image >= len(self.game.p_l_animate):
                self.current_image = 0
            self.image = self.game.p_l_animate[int(self.current_image)]
            #Defines transparent bg colour for player image
            self.image.set_colorkey(WHITE) 
        if direction == "right":
            self.current_image += 0.1
            if self.current_image >= len(self.game.p_r_animate):
                self.current_image = 0
            self.image = self.game.p_r_animate[int(self.current_image)]
            #Defines transparent bg colour for player image
            self.image.set_colorkey(WHITE) 
        
    def basic_movement(self):
        keys = pg.key.get_pressed()

        #Basic movement
        self.dy, self.dx = 0, 0 #Current x and y speed change = 0 by default
        if self.movelock == False:
            if keys[pg.K_w]:
                self.dy = -self.speed #Set delta y to - player speed 
                self.animate("up")
            if keys[pg.K_a]:
                self.dx = -self.speed #Set delta x to - player speed
                self.animate("left")
            if keys[pg.K_s]:
                self.dy = self.speed #Set delta y to  player speed 
                self.animate("down")
            if keys[pg.K_d]:
                self.dx = self.speed #Set delta x to  player speed
                self.animate("right")
        
        self.x += self.dx #Change player x position by delta x per frame
        self.y += self.dy #Change player y position by delta y per frame
        
    def update(self):
        #Check for WASD inputs
        self.basic_movement()

        #Calls check wall collision method
        self.rect.x = self.x #Set player x rect hitbox equal to player x location
        self.check_wall_collision("x") #Check x axis wall collisions
        self.rect.y = self.y #Set player x rect hitbox equal to player x location
        self.check_wall_collision("y") #Check y axis wall collisions

        #Check if player has moved offscreen
        self.check_offscreen()

        #Check if player movement is locked
        #print(self.movelock)
        if self.movelock == True:
            self.speed = 0
        else:
            self.speed = 2
        
class Tile(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

#Constants:
FPS = 60
TILESIZE = 32
#Screen size 16x13Tiles
WIDTH = TILESIZE*16 
HEIGHT = TILESIZE*13
#Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Create game instance
game = Game()
