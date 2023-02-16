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
        self.init_object_status()
        self.screen_setup()
        self.new_room(self.roomx,self.roomy)
        self.gameloop()

    def init_variables(self): #Initialise global game variables
        self.running = True
        self.clock = pg.time.Clock()
        self.roomx = 0
        self.roomy = 0
        self.border_colour = (153,50,204)
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

    def init_spritegroups(self): #Initialise sprite groups
        self.player_sg = pg.sprite.Group() #Player only
        self.all_sg = pg.sprite.Group() #All sprites (used to update all sprites)

        self.floor_sg = pg.sprite.Group() #Floor tile sprite group
        self.deco_sg = pg.sprite.Group() #For background decoration that can be walked over
        self.wall_sg = pg.sprite.Group() #Wall tile sprite group

        self.border_sg = pg.sprite.Group() #Sprite group for border tiles
        self.textbox_sg = pg.sprite.Group() #Group for all textbox components

    def init_objects(self): #Initialise objects
        self.player = Player(self,3*TILESIZE,3*TILESIZE)
        self.all_sg.add(self.player)
        self.player_sg.add(self.player)

    def init_object_status(self): #Initialise the default status of objects
        #Doors:
        self.door_status = [False,False,0,0,0,0,0,0,0,0,0,0,0,0,0] #List to hold status of all doors, starting with default
        self.button_status = [False,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #List to hold status of all buttons, starting with default

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
        self.arrow = pg.image.load("UI/arrow.png")
        self.arrow_show = False
        self.arrow.set_colorkey(WHITE)
        self.arrowx = TILESIZE*13.5
        self.arrowy = TILESIZE*10

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
        self.draw_tiles(roomx,roomy) #Spawn all the static tiles needed for the current room
        if roomx == 0 and roomy == 0:
            self.button0 = Button(self, roomx, roomy, 0, TILESIZE*4, TILESIZE*7, "up")

            #Spawn doors
            self.door0 = Door(self, roomx, roomy, 0, TILESIZE*3, TILESIZE*11)
            self.door1 = Door(self, roomx, roomy, 1, TILESIZE*12, TILESIZE*5)
                
            #Spawn animated tile
            self.atile = ATile(self, roomx, roomy, TILESIZE*8, TILESIZE*2, 0, 4, 0.05, BLACK)
            #Spawn animated tile
            self.atile = ATile(self, roomx, roomy, TILESIZE*6, TILESIZE*2, 0, 4, 0.05, BLACK)

    def game_text(self): #Loads text used in textboxes
        self.gametext1 = []
        self.gametext1.append("Welcome, test subject 48. (Press O)")
        self.gametext1.append("Use the WASD keys to move around.")

        self.gametext2 = []
        self.gametext2.append("Walk over to that button to open the door")
         
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

        #Show arrow
        self.arrow_show = True
        
        self.onscreen_text(colour1, title, x1, y1, colour2, text_array[self.textcount], x2, y2) #Setup text to show on screen
        if self.action == True: #If action key pressed
            if self.textcount < len(text_array) - 1: #If count less than 1 minus the length of the text array
                self.textcount += 1 #Increment count
            else:
                self.textcount = 0 #Reset count
                self.clear_textbox() 
                return True
          
    def clear_textbox(self):
        self.showtextbox = False
        self.arrow_show = False
        self.onscreen_text(BLACK,"",0,0,BLACK,"",0,0) #No text
        self.player.movelock = False

    def chunk_event(self,x,y):
        if x == 0 and y == 0: #ROOM 0,0
        
            if self.phase == 0:
                if self.timer(2000):
                    self.phase = 1
            if self.phase == 1:
                if self.open_textbox(BLACK, "???", TILESIZE*3, TILESIZE*7, BLACK, self.gametext1, TILESIZE*2.5, TILESIZE*9):
                    self.phase = 2
            if self.phase == 2:
                if self.player.y > TILESIZE*6:
                    if self.open_textbox(BLACK, "???", TILESIZE*3, TILESIZE*7, BLACK, self.gametext2, TILESIZE*2.5, TILESIZE*9):
                        self.phase = 3
            if self.phase == 3:
                if self.player.y == TILESIZE*7 and (self.player.x >= TILESIZE*3.5 and self.player.x <= TILESIZE*4.5):
                    if self.action == True:
                        self.button0.switch()
                       
    def button_event(self): #Events to occur when a specific button is pressed
        if self.button_status[0] == False:
            self.door_status[0] = False
            self.wall_sg.add(self.door0)                                       
            self.door_status[1] = False
            self.wall_sg.add(self.door1)  
        else:
            self.door_status[0] = True
            self.door_status[1] = True

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
                        if event.key == pg.K_o: #If event key pressed, toggle action variable on
                                self.action = True

                        #Temp
                        if event.key == pg.K_e: 
                            print(self.player.x, self.player.y, self.player.x/TILESIZE, self.player.y/TILESIZE)
            
            def draw_all():
                #Draw background of screen
                self.screen.fill(GREY)
                
                #Draw sprites
                self.floor_sg.draw(self.screen)
                self.deco_sg.draw(self.screen)
                self.player_sg.draw(self.screen)
                self.wall_sg.draw(self.screen)

                #Draw textbox
                if self.showtextbox == True:
                    self.screen.blit(self.textbox_img,(TILESIZE*1.5,TILESIZE*6.5)) #Draw box
                    self.screen.blit(self.titletext_surface,(self.titletext_x, self.titletext_y)) #Draw title
                    self.screen.blit(self.text_surface,(self.text_x, self.text_y)) #Draw text
                if self.arrow_show == True:
                    self.screen.blit(self.arrow,(self.arrowx,self.arrowy))

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
                self.chunk_event(self.roomx,self.roomy)
                self.button_event()
                self.all_sg.update()
                self.clock.tick(FPS)
                pg.display.update()

                #Update arrow movement 
                if self.arrowy < TILESIZE*10.5:
                    self.arrowy += 0.3
                else:
                    self.arrowy = TILESIZE*10
            
            #Methods to call continuously:
            events()       
            draw_all()
            update()
            
            #Time in frames of the game
            self.current_time = pg.time.get_ticks()
            self.timepassed = self.current_time - self.timepoint

            #Set is action button pressed? to false by default
            if self.action == True:
                self.action = False
            
            #print(self.current_time,self.timepoint,self.timepassed,self.timelock,self.action)
            print("wall count ",len(self.wall_sg)," ","all count ",len(self.all_sg)," ","deco count ",len(self.deco_sg))
    
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
    
    def update(self):
        pass

class Door(pg.sprite.Sprite):
    def __init__(self, game, roomx, roomy, id, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game to this class
        self.id = id #Used to identify which specific door this is
        self.game.all_sg.add(self) #Add self to all sprites group
        self.game.deco_sg.add(self) #Add self to all sprites group

        if self.game.door_status[self.id] == False:
            self.game.wall_sg.add(self) #Add self to wall sprite group
        
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x,y
        self.image = pg.image.load("2stateTiles/door_closed.png") #Closed door image is loaded by default
        self.colourkey = WHITE
        self.image.set_colorkey(self.colourkey)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0,0
        self.rect.topleft = (x,y)
    
    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the door's chunk doesnt match player chunk:
            self.game.wall_sg.remove(self)
            self.game.deco_sg.remove(self)
            self.game.all_sg.remove(self)

        if self.game.door_status[self.id] == False:
            self.image = pg.image.load("2stateTiles/door_closed.png")
            self.image.set_colorkey(WHITE)
        else:
            self.image = pg.image.load("2stateTiles/door_open.png")
            self.image.set_colorkey(WHITE)
            self.game.wall_sg.remove(self)

        #print(self.game.door_status)
        #print(self.game.roomx,self.game.roomy,self.roomx,self.roomy)
        
class Button(pg.sprite.Sprite):
    def __init__(self, game, roomx, roomy, id, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.deco_sg.add(self)
        self.game.all_sg.add(self)
        self.image = pg.image.load("2StateTiles/button_unpressed.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.roomx, self.roomy = roomx, roomy
        self.rect.x, self.rect.y = x,y
        self.id = id #Used to identify which specific button this is
    
    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the buttons's chunk doesnt match player chunk:
            self.game.deco_sg.remove(self)
            self.game.all_sg.remove(self)

        if self.game.button_status[self.id] == True: #If button pressed:
            self.image = pg.image.load("2StateTiles/button_pressed.png")
            self.image.set_colorkey(WHITE)
        else: #If button unpressed:
            self.image = pg.image.load("2StateTiles/button_unpressed.png")
            self.image.set_colorkey(WHITE)
        
    def switch(self):
        if self.game.button_status[self.id] == True: #If button is pressed:
            self.game.button_status[self.id] = False
        else: #If button is unpressed:
            self.game.button_status[self.id] = True

class ATile(pg.sprite.Sprite):
    def __init__(self, game, roomx, roomy, x ,y, frameA, frameB, animationspeed, colourkey):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x,y

        self.game.wall_sg.add(self) #Add self to wall sprite group
        self.game.all_sg.add(self) #Add self to all sprites group

        self.image = pg.image.load("ATiles/Atile0.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.current_image = 0
        self.setup_animation(frameA,frameB)
        self.animation_speed = animationspeed
        self.colourkey = colourkey

    def setup_animation(self,frameA,frameB):
        self.image_animation = [] #Array to store all frames of animation
        for i in range(frameA, frameB+1): #From frameA to frameB (Indicates which animated tiles to load)
            self.image_animation.append(pg.image.load("ATiles/Atile"+ str(i) +".png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the Atile's chunk doesnt match player chunk:
            self.game.wall_sg.remove(self)
            self.game.all_sg.remove(self)
        
        self.current_image += self.animation_speed
        if self.current_image >= len(self.image_animation):
            self.current_image = 0
        self.image = self.image_animation[int(self.current_image)]
        self.image.set_colorkey(self.colourkey)
        
#Constants:
FPS = 60
TILESIZE = 32
#Screen size 16x13Tiles
WIDTH = TILESIZE*16  #512x416
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