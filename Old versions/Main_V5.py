#IMPLEMENTATION FOR NEA 2022 - 2023 "MINI RPG" BY ISMAEL

#LIBRARIES:
import pygame as pg     #Pygame - used for OOP in python (imported as "pg" as shorthand to improve efficiency when coding)
import csv              #CSV    - used to read the csv files that will store the map data of the game
import random           #Random - used to randomise certain events to make the gameplay more interesting

#CLASSES:
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
        self.gamemode = "MENU"

        self.roomx = 0
        self.roomy = 0
        self.border_colour = (153,50,204)
        self.showtextbox = False
        self.movelock = True 

        self.current_image = 0
        self.current_time = 0 #By default game time is 0
        self.timepoint = 0 #Point in time for an event default to 0
        self.timepassed = 0 #Time elapsed from timepoint to current time default 0
        self.timelock = False #lock used to instantaneously get a timepoint

        self.phase = 0 #Refers to the stage of the game

        self.font35 = pg.font.SysFont("Aerial", 35)
        self.font25 = pg.font.SysFont("Aerial", 25)

        self.action = False #Toggle for when action key is pressed

    def init_spritegroups(self): #Initialise sprite groups
        self.player_sg = pg.sprite.Group() #Player only
        self.enemy_sg = pg.sprite.Group()
        self.all_sg = pg.sprite.Group() #All sprites (used to update all sprites)

        #Tile layers:
        self.floor_sg = pg.sprite.Group() #Floor tile sprite group
        self.bgdeco_sg = pg.sprite.Group() #For background decoration that can be walked over
        self.fgdeco_sg = pg.sprite.Group() #For foreground decoration that will be above the player
        self.wall_sg = pg.sprite.Group() #Wall tile sprite group

        self.border_sg = pg.sprite.Group() #Sprite group for border tiles
        self.textbox_sg = pg.sprite.Group() #Group for all textbox components

    def init_objects(self): #Initialise objects
        self.player = Player(self,3*TILESIZE,3*TILESIZE)
        self.all_sg.add(self.player)
        self.player_sg.add(self.player)

    def init_object_status(self): #Initialise the default status of objects
        #Doors:
        self.textbox_status = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.door_status = [False,False,0,0,0,0,0,0,0,0,0,0,0,0,0] #List to hold status of all doors, starting with default
        self.button_status = [False,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #List to hold status of all buttons, starting with default

    def load_images(self): #Loads all images that will be used in the program
        #Border images
        self.border_image = pg.image.load("Tiles/tile0.png")

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

        #Door images:
        self.door_images = [] #Array that holds all the door images
        self.door_images.append("2stateTiles/doors/tile0.png") 
        self.door_images.append("2stateTiles/doors/tile1.png")
        self.door_images.append("2stateTiles/doors/tile2.png") 
        self.door_images.append("2stateTiles/doors/tile3.png")

        #Slime
        self.slime_images = ["Slime/tile0.png", "Slime/tile1.png"] #Array that holds all the door images
    
        #UI images:
        #Textbox
        self.textbox_img = pg.image.load("UI/textbox.png")
        #Textbox arrow
        self.arrow = pg.image.load("UI/arrow.png")
        self.arrow.set_colorkey(WHITE)
        self.arrowx = TILESIZE*13.5
        self.arrowy = TILESIZE*10
        #Query icon
        self.qicon = pg.image.load("UI/query_icon.png")
        self.qicon.set_colorkey(WHITE)
        self.qiconx = TILESIZE*1.2
        self.qicony = TILESIZE*1.2

        #Backgrounds:
        self.menubg_animate = []
        self.menubg_animate.append(pg.image.load("Backgrounds/bg1.png"))
        self.menubg_animate.append(pg.image.load("Backgrounds/bg2.png"))
        
    def screen_setup(self): #Set up screen
        pg.display.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        icon = pg.image.load("Tiles/tile40.png")
        pg.display.set_icon(icon)
        pg.display.set_caption("MINI RPG")

        self.create_border()

    def create_border(self): #Set the border around the display
        #Black Border
        #Top and bottom horizontal black lines
        for x in range(0, WIDTH, TILESIZE):
            new_tile = Tile(self, "static", self.roomx, self.roomy, x, 0, self.border_image, 0, 0, 0, 0, WHITE)
            self.border_sg.add(new_tile)
            new_tile = Tile(self, "static", self.roomx, self.roomy, x, HEIGHT-TILESIZE, self.border_image, 0, 0, 0, 0, WHITE)
            self.border_sg.add(new_tile)

        #Left and right vertical black lines
        for y in range(0, HEIGHT, TILESIZE):
            new_tile = Tile(self, "static", self.roomx, self.roomy, 0, y, self.border_image, 0, 0, 0, 0, WHITE)
            self.border_sg.add(new_tile)
            new_tile = Tile(self, "static", self.roomx, self.roomy, WIDTH-TILESIZE, y, self.border_image, 0, 0, 0, 0, WHITE)
            self.border_sg.add(new_tile)

    def spawn_tiles(self,roomx,roomy): #Initialise the static tiles in a given room
        #Clear old tiles
        self.floor_sg.empty()
        self.wall_sg.empty()
        self.fgdeco_sg.empty()

        #Add tiles to sprite groups
        self.layers = ["MAP_Floors.csv", "MAP_Walls.csv", "MAP_ForegroundDecoration.csv"] #Layers of the tilemap
        
        for layer in self.layers: #Go through all layers
            csv_file = open(layer,"r") #Open file
            data = csv.reader(csv_file) #Read as a csv file
            
            for ypos, yvalue in enumerate(data): #For every row in data and return the index of each row in variable called y
                if ypos >= roomy*11 and ypos < (11 + roomy*11): #If y index (row position) between the 11 rows wanted (11 because excluding borders):

                    for xpos, xvalue in enumerate(yvalue): #For every tile in row and return the index of each tile in variable called x
                        if xpos >= roomx*14 and xpos < (14 + roomx*14): #If x index (tile position) between the 14 rows wanted:
                            
                            tile = xvalue
                            if tile != "-1": #If tile is not an empty space:
                                image = pg.image.load("Tiles/tile"+ tile +".png") #Image is the file matching the tile number with the filename

                                #Set x and y equal to border space + tilepos*size subtracting a multiple of the screen size to map any room back into the 0,0 postition
                                x = TILESIZE + (TILESIZE*xpos) - roomx*14*TILESIZE
                                y = TILESIZE + (TILESIZE*ypos) - roomy*11*TILESIZE
                                #Create new tile, static type, local room position, x and y pos, image, 0s indicate placeholder since these parameters are not needed for static tiles, colourkey
                                new_tile = Tile(self, "static", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE) 

                                if layer == "MAP_Walls.csv": #If on wall layer:
                                    self.wall_sg.add(new_tile) #Classify this new tile as a wall tile
                                if layer == "MAP_Floors.csv": #If on floor layer
                                    self.floor_sg.add(new_tile) #Classify this new tile as a floor tile
                                if layer == "MAP_ForegroundDecoration.csv": #If on fg deco layer
                                    self.fgdeco_sg.add(new_tile) #Classify this new tile as a fg deco tile
                                self.all_sg.add(new_tile)
                                                               
    def new_room(self,roomx,roomy): #Initalise the animated tiles and objects for all rooms
        self.all_sg.empty() #Clear the all sprite group
        self.all_sg.add(self.player) #Re add the player
        self.spawn_tiles(roomx,roomy) #Spawn all the animated tiles needed for the current room
        if roomx == 0 and roomy == 0: #ROOM 00
            self.button0 = Button(self, roomx, roomy, 0, TILESIZE*4, TILESIZE*7, "up") #Spawn button
            self.door0 = Door(self, roomx, roomy, 0, 0, 1, TILESIZE*3, TILESIZE*11) #Spawn door
            self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*12, TILESIZE*2, 0, 1, 0, 4, 0.05, BLACK) #Spawn animated tiles
            self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*12, TILESIZE*5, 0, 1, 0, 4, 0.05, BLACK)
            self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*12, TILESIZE*8, 0, 1, 0, 4, 0.05, BLACK)
        if roomx == 0 and roomy == 1: #ROOM 01
            if self.phase == 2:
                self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*3, TILESIZE*6, 0, 3, 0, 1, 0.02, WHITE) #NPC1
                self.slime = Enemy(self, "slime", roomx, roomy, TILESIZE*9, TILESIZE*3, 1, 0.05, 0.05) #Slime ##########################################
            self.door1 = Door(self, roomx, roomy, 1, 2, 3, TILESIZE*5, TILESIZE*7) #Spawn door
        if roomx == 1 and roomy == 1: #ROOM 11
            self.door2 = Door(self, roomx, roomy, 2, 0, 1, TILESIZE*13, TILESIZE*3) #Spawn door
        if roomx == 1 and roomy == 0: #ROOM 10
            self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*3, TILESIZE*8, 0, 2, 0, 1, 0.02, WHITE)
            self.atile = Tile(self, "animated", roomx, roomy, TILESIZE*9, TILESIZE*8, 0, 2, 0, 1, 0.035, WHITE)
       
    def game_text(self): #Loads text used in textboxes
        #Dialogue text:
        self.gametext1 = []
        self.gametext1.append("Use WASD keys to move and the O key")

        #Sign text:
        self.signtext1 = ["Supply Room (V)      Tunnel A (>)"]

        #NPC text:
        self.npctext1 = []
        self.npctext1.append("Ah good youre awake")
        self.npctext1.append("I can't open the door to the supply room")
        self.npctext1.append("I'd do it easily if i had my screwdriver")
        self.npctext1.append("But I can't find it anywhere :/")
        self.npctext1.append("Can you help me find it?")

        #Object text:
        self.objecttext1 = ["Looks like a pump of some sort", "It emits an ominous green glow", "what is this place?"]
        self.objecttext2 = ["The monitors look broken and stuck in a", "looping pattern yet they seem somewhat", "familiar"]
        self.objecttext3 = ["These hospital beds are hooked up to IVs","full of a green liquid"]

    def timer(self,delay): #Used to allow a delay (NEEDS FIXING)
        if self.timelock == False:
            self.timepoint = pg.time.get_ticks()
            self.timelock = True
        if self.timepassed > delay:
            self.timelock = False
            return True

    def ui_update(self): #Updates to the query icon, textbox arrow etc
        #Update arrow movement 
        if self.arrowy < TILESIZE*10.5:
            self.arrowy += 0.3
        else:
            self.arrowy = TILESIZE*10

        #Update query icon movement
        if self.qicony < TILESIZE*1.4:
            self.qicony += 0.1
        else:
            self.qicony = TILESIZE*1.2

    def setup_textbox(self,textboxtype,colour1,title,x1,y1,colour2,text_array,x2,y2): #Configures a new textbox with given parameters
        #Parameters: textboxtype: Is the textbox manually action spawned or auto spawned?
        #            colour1, colour2 : Colours for the title and text
        #            x1, x2 , x3, x4: Positions for the text
        #            title, text_array: The text that will be displayed as the title and text respectively
        if self.showtextbox == False:
            self.movelock = True #Lock movement while the textbox is true
            self.textcount = 0 #Used to cycle through textbox pages
            self.textcount2 = 0 #Used in the case where there is only one textbox page
            self.textboxtype = textboxtype
            self.textcolour1, self.textcolour2 = colour1, colour2
            self.titletext, self.text_array = title, text_array
            self.titletext_x, self.titletext_y = x1, y1
            self.text_x, self.text_y = x2, y2
            self.showtextbox = True #Will update all textbox components in gameloop update section
    
    def draw_textbox(self): #Draws all components of the textbox onto the screen
        self.titletext_surface = self.font35.render(self.titletext,True,self.textcolour1) #Create the text surface with the parameters
        self.text_surface = self.font25.render(self.text_array[self.textcount-1],True,self.textcolour2) 

        self.screen.blit(self.textbox_img,(TILESIZE*1.5,TILESIZE*6.5)) #Draw box
        self.screen.blit(self.titletext_surface,(self.titletext_x, self.titletext_y)) #Draw title
        self.screen.blit(self.text_surface,(self.text_x, self.text_y)) #Draw text
        self.screen.blit(self.arrow,(self.arrowx,self.arrowy))
        
        if self.action:
            #The case where the textbox has more than one page:
            if len(self.text_array) > 1:
                if self.textcount < len(self.text_array): 
                    self.textcount += 1 #Increment count
                else:
                    self.textcount = 0 #Reset count
                    self.clear_textbox()
            
            #The case where the textbox has only one page
            else:
                if self.textboxtype == "auto":
                    x = 0
                else:
                    x = 1
                if self.textcount2 < x:
                    self.textcount2 += 1 #Increment count2
                else:
                    self.textcount2 = 0 #Reset count2
                    self.clear_textbox()

    def clear_textbox(self): #Removes the textbox
        self.showtextbox = False
        self.arrow_show = False
        self.textcolour1, self.textcolour2 = BLACK, BLACK
        self.titletext_x, self.titletext_y = -100, -100
        self.text_x, self.text_y = -100, -100
        self.movelock = False

    def room_event(self,x,y): #All events in each specific room
        #ROOM 0,0------------------------------------------------------------------------------------------------------------
        if x == 0 and y == 0:
            if self.phase == 0:
                if self.timer(2000):
                    self.phase = 1
            if self.phase == 1:
                self.setup_textbox("auto", BLACK, "???", TILESIZE*3, TILESIZE*7, BLACK, self.gametext1, TILESIZE*2.5, TILESIZE*9)
                self.phase = 2
            
            #Textbox appears explaining controls
            if (self.player.y >= TILESIZE*7 and self.player.y <= TILESIZE*7.5) and (self.player.x >= TILESIZE*3.5 and self.player.x <= TILESIZE*4.5):
                self.qicon_show = True
                if self.action == True:
                    self.button0.switch()
            #Inspect pump in room 00
            elif self.player.x == TILESIZE*14:
                self.qicon_show = True
                if self.action == True:
                    self.setup_textbox("manual", BLACK, "---", TILESIZE*3, TILESIZE*7, BLACK, self.objecttext1, TILESIZE*2.5, TILESIZE*9)
            else:
                self.qicon_show = False
        
        #ROOM 0,1------------------------------------------------------------------------------------------------------------
        if x == 0 and y == 1: 
            #Sign1
            if (self.player.y == TILESIZE*2) and (self.player.x >= TILESIZE*4.5 and self.player.x <= TILESIZE*5.5):
                self.qicon_show = True
                if self.action == True:
                    self.setup_textbox("manual", BLACK, "---", TILESIZE*3, TILESIZE*7, BLACK, self.signtext1, TILESIZE*2.5, TILESIZE*9)
            #NPC1
            elif (self.player.y > TILESIZE*5) and (self.player.x >= TILESIZE*2.5 and self.player.x <= TILESIZE*3.5):
                if self.phase == 2:
                    self.qicon_show = True
                    if self.action == True:
                        self.setup_textbox("manual", BLACK, "Janitor", TILESIZE*2, TILESIZE*7, BLACK, self.npctext1, TILESIZE*2.5, TILESIZE*9)
            else:
                self.qicon_show = False
        
        #ROOM 1,0------------------------------------------------------------------------------------------------------------
        if x == 1 and y == 0:
            if (self.player.y == TILESIZE*9) and ((self.player.x >= TILESIZE*2.5 and self.player.x <= TILESIZE*3.5) or (self.player.x >= TILESIZE*8.5 and self.player.x <= TILESIZE*9.5)):
                self.qicon_show = True
                if self.action == True:
                    self.setup_textbox("manual", BLACK, "---", TILESIZE*3, TILESIZE*7, BLACK, self.objecttext2, TILESIZE*2.5, TILESIZE*9)
            elif (self.player.y == TILESIZE*9) and (self.player.x >= TILESIZE*5.5 and self.player.x <= TILESIZE*6.5):
                self.qicon_show = True
                if self.action == True:
                    self.setup_textbox("manual", BLACK, "---", TILESIZE*3, TILESIZE*7, BLACK, self.objecttext3, TILESIZE*2.5, TILESIZE*9)
            else:
                self.qicon_show = False
            
    def button_event(self): #Events to occur when a specific button is pressed
        if self.button_status[0] == False:
            self.door_status[0] = False
            self.wall_sg.add(self.door0)                                        
        else:
            self.door_status[0] = True

    def gameloop(self): #Main loop that will run while running program
        
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
                        if self.gamemode == "MENU":
                            self.gamemode = "GAME"
                
                    #Temporary code:
                    if event.key == pg.K_e: 
                        print(self.player.x, self.player.y, self.player.x/TILESIZE, self.player.y/TILESIZE)
        
        def draw_all(): #Draws all components onto the screen    
            #Draw sprites
            self.floor_sg.draw(self.screen)
            self.bgdeco_sg.draw(self.screen)
            self.player_sg.draw(self.screen)
            self.wall_sg.draw(self.screen)
            self.fgdeco_sg.draw(self.screen)

            #Draw textbox
            if self.showtextbox == True:
                self.draw_textbox()
    
            #Draw grid (TEMPORARY)
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

            #Query icon
            if self.qicon_show == True:
                self.screen.blit(self.qicon,(self.qiconx,self.qicony))
        
        def update(): #Updates screen, player and all objects
            if self.gamemode == "GAME": #Run these methods only if the program is running the game
                self.room_event(self.roomx,self.roomy)
                self.button_event()
                self.all_sg.update()
                self.ui_update()

            #Run this regardless of gamemode
            self.clock.tick(FPS) 
            pg.display.update()
        
        while self.running == True: #GAME LOOP---------------------------------------------------------------------------------------
            events()
            update()

            if self.gamemode == "MENU": #If in mode: Menu
                self.image = self.menubg_animate[int(self.current_image)]
                self.screen.blit(self.image, (0,0))
                self.current_image += 0.05
                if self.current_image >= len(self.menubg_animate):
                    self.current_image = 0
            
            elif self.gamemode == "GAME": #If in mode: Game
                #Methods to call continuously:
                draw_all() 
                
                #Time in frames of the game
                self.current_time = pg.time.get_ticks()
                self.timepassed = self.current_time - self.timepoint

                #Set action status to false by default
                if self.action == True:
                    self.action = False
                
                #print(self.current_time,self.timepoint,self.timepassed,self.timelock,self.action)
                #print("wall count ",len(self.wall_sg)," ","all count ",len(self.all_sg)," ","deco count ",len(self.bgdeco_sg)," ", "floor count ",len(self.floor_sg))

class Player(pg.sprite.Sprite): #The object that will be directly 
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Gives a copy of the game to this class

        self.current_image = 0 #Will be used to time animations
        self.image = self.game.p_d_animate[1] #Start with player frame (down2)
        self.image.set_colorkey(WHITE) #Define transparent background colour of png image

        #self.rect = self.image.get_rect()
        self.rect = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)

        self.rect.x = x #Hitbox x pos
        self.rect.y = y #Hitbox y pos
        self.x = x #Player x pos
        self.y = y #Player y pos
        self.dy = 0 #Current yspeed
        self.dx = 0 #Current xspeed 
        self.speed = 2 #Speed increment
        self.direction = 0 #Will change to x or y indicating axis of movement

        self.uplock, self.rightlock, self.downlock, self.leftlock = False, False, False, False

    def check_collision(self,axis):
        #Wall collisions
        if axis == "x":
            self.wallhit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls x?
            if self.wallhit:
                if self.dx > 0: #If moving right (x increasing)
                    self.x = self.wallhit[0].rect.left - self.rect.width #set player x (left side) to equal the xpos of object hit minus the player width (collision right)
                if self.dx < 0: #If moving left (x decreasing)
                    self.x = self.wallhit[0].rect.right #set player x (right side) to equal the xpos of object hit (collision left)
                self.dx = 0 #Else x velocity is 0 as not moving horizontally
                self.rect.x = self.x #Update x rect or "hitbox"
                
        if axis == "y":
            self.wallhit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls y?
            if self.wallhit:
                if self.dy < 0: #If moving up (y incresing)
                    self.y = self.wallhit[0].rect.bottom #set player y (bottom side) to equal the ypos of object hit (collision up)
                if self.dy > 0: #If moving down (y decreasing)
                    self.y = self.wallhit[0].rect.top - self.rect.height #set player y (top side) to equal the ypos of object hit minus the player height (collision down)
                self.dy = 0 #Else y velocity is 0 as not moving vertically
                self.rect.y = self.y
        
        #Enemy collsisions
        self.enemyhit = pg.sprite.spritecollide(self, self.game.enemy_sg, False)
        if self.enemyhit:
            pass

    def check_offscreen(self):
        if self.y > HEIGHT - TILESIZE - 10: #If close enough to the edge, lock perpendicular movement to avoid wall clipping
            self.uplock, self.rightlock, self.downlock, self.leftlock = False, True, False, True
            if self.y > HEIGHT - TILESIZE - 5: #If offscreen down:
                self.game.roomy += 1
                self.game.new_room(self.game.roomx, self.game.roomy) #New room with y coordinate +1
                self.y = 6 #Mirror player position on opposite edge of screen 

        elif self.y <= 10:
            self.uplock, self.rightlock, self.downlock, self.leftlock = False, True, False, True
            if  self.y <= 5: #If offscreen up:
                self.game.roomy -= 1
                self.game.new_room(self.game.roomx, self.game.roomy)
                self.y = HEIGHT - TILESIZE - 6
        
        elif self.x > WIDTH - TILESIZE - 20:
            self.uplock, self.rightlock, self.downlock, self.leftlock = True, False, True, False
            if self.x > WIDTH - TILESIZE - 5: #If offscreen right:
                self.game.roomx += 1
                self.game.new_room(self.game.roomx, self.game.roomy) #New room with y coordinate +1
                self.x = 6 #Mirror player position on opposite edge of screen 
        
        elif self.x < TILESIZE + 5:
            self.uplock, self.rightlock, self.downlock, self.leftlock = True, False, True, False
            if self.x < 5: #If offscreen left:
                self.game.roomx -= 1
                self.game.new_room(self.game.roomx, self.game.roomy) #New room with y coordinate +1
                self.x = WIDTH - TILESIZE - 6 #Mirror player position on opposite edge of screen
        else:
            self.uplock, self.rightlock, self.downlock, self.leftlock = False, False, False, False 

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
        if self.game.movelock == False:
            if keys[pg.K_w]: #UP
                if self.uplock == False:
                    self.dy = -self.speed #Set delta y to - player speed 
                    self.animate("up")
            if keys[pg.K_a]: #LEFT
                if self.leftlock == False:
                    self.dx = -self.speed #Set delta x to - player speed
                    self.animate("left")
            if keys[pg.K_s]: #DOWN
                if self.downlock == False:
                    self.dy = self.speed #Set delta y to  player speed 
                    self.animate("down")
            if keys[pg.K_d]: #RIGHT
                if self.rightlock == False:
                    self.dx = self.speed #Set delta x to  player speed
                    self.animate("right")
        
        self.x += self.dx #Change player x position by delta x per frame
        self.y += self.dy #Change player y position by delta y per frame
        
    def update(self):
        #Check for WASD inputs
        self.basic_movement()

        #Calls check wall collision method
        self.rect.x = self.x #Set player x rect hitbox equal to player x location
        self.check_collision("x") #Check x axis wall collisions
        self.rect.y = self.y #Set player y rect hitbox equal to player y location
        self.check_collision("y") #Check y axis wall collisions

        #Check if player has moved offscreen
        self.check_offscreen()

        #Check if player movement is locked
        if self.game.movelock == True:
            self.speed = 0
        else:
            self.speed = 2
        
        #print(self.uplock, self.rightlock, self.downlock, self.leftlock)
            
class Door(pg.sprite.Sprite): #Two state door object
    def __init__(self, game, roomx, roomy, id, closedimageid, openimageid, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game to this class
        self.id = id #Used to identify which specific door this is
        self.closedimageid, self.openimageid = closedimageid, openimageid #The id of the graphics for the open and closed door

        self.game.all_sg.add(self) #Add self to all sprites group
        self.game.bgdeco_sg.add(self) #Add self to all sprites group

        if self.game.door_status[self.id] == False:
            self.game.wall_sg.add(self) #Add self to wall sprite group
        
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x,y
        
        self.image = pg.image.load(self.game.door_images[self.closedimageid])
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.rect.topleft = (x,y)
    
    def update(self):
        if self.game.door_status[self.id] == False: #If door closed:
            self.image = pg.image.load(self.game.door_images[self.closedimageid])
            self.image.set_colorkey(WHITE)
            self.game.wall_sg.add(self) #Add to wall sg hence adding collisions
        else: #If door open:
            self.image = pg.image.load(self.game.door_images[self.openimageid])
            self.image.set_colorkey(WHITE)
            self.game.wall_sg.remove(self)
        
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the door's chunk doesnt match player chunk:
            self.game.wall_sg.remove(self) #Remove door from the following sprite groups:
            self.game.bgdeco_sg.remove(self)
            self.game.all_sg.remove(self) 

        #print(self.game.door_status)
        #print(self.game.roomx,self.game.roomy,self.roomx,self.roomy)

    def switch(self):
        if self.game.door_status[self.id] == True: #If door is closed:
            self.game.door_status[self.id] = False
        else: #If door is open:
            self.game.door_status[self.id] = True

class Button(pg.sprite.Sprite): #Two state button object
    def __init__(self, game, roomx, roomy, id, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.bgdeco_sg.add(self)
        self.game.all_sg.add(self)
        self.image = pg.image.load("2StateTiles/tile1.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.roomx, self.roomy = roomx, roomy
        self.rect.x, self.rect.y = x,y
        self.id = id #Used to identify which specific button this is
    
    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the buttons's chunk doesnt match player chunk:
            self.game.bgdeco_sg.remove(self)
            self.game.all_sg.remove(self)

        if self.game.button_status[self.id] == True: #If button pressed:
            self.image = pg.image.load("2StateTiles/tile0.png")
            self.image.set_colorkey(WHITE)
        else: #If button unpressed:
            self.image = pg.image.load("2StateTiles/tile1.png")
            self.image.set_colorkey(WHITE)
        
    def switch(self):
        if self.game.button_status[self.id] == True: #If button is pressed:
            self.game.button_status[self.id] = False
        else: #If button is unpressed:
            self.game.button_status[self.id] = True

class Tile(pg.sprite.Sprite): #Square graphics that make up the game
    def __init__(self, game, type, roomx, roomy, x ,y, image, folderid, frameA, frameB, animationspeed, colourkey):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game class
        self.type = type
        self.x, self.y = x, y #Initialise x and y positions
        self.colourkey = colourkey

        #STATIC TILE
        if self.type == "static":
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.image.set_colorkey(self.colourkey)

        #ANIMATED TILE
        elif self.type == "animated": 
            self.roomx, self.roomy = roomx, roomy #Set the local room position
            self.colourkey = colourkey 

            self.game.wall_sg.add(self) #Add self to wall sprite group
            self.game.all_sg.add(self) #Add self to all sprites group
            
            #Array for the different animated tile folders
            self.folders = ["folder0","folder1","folder2","folder3"] 

            self.image = pg.image.load("ATiles/" + self.folders[folderid] + "/Atile0.png") #Default image
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.image.set_colorkey(self.colourkey)
            self.current_image = 0
            self.setup_animation(folderid,frameA,frameB)
            self.animation_speed = animationspeed
        
    def setup_animation(self, folderid, frameA, frameB):
        self.image_animation = [] #Array to store all frames of animation
        for i in range(frameA, frameB+1): #From frameA to frameB (Indicates which animated tiles to load)
            #Add this image to the array: image with file path that matches this below:
            self.image_animation.append(pg.image.load("ATiles/" + self.folders[folderid] + "/Atile"+ str(i) +".png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.type == "animated":
            if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the Atile's chunk doesnt match player chunk:
                self.game.wall_sg.remove(self)
                self.game.all_sg.remove(self)

            #Animation
            self.current_image += self.animation_speed
            if self.current_image >= len(self.image_animation):
                self.current_image = 0
            self.image = self.image_animation[int(self.current_image)]
            self.image.set_colorkey(self.colourkey)

            
        #print(len(self.game.wall_sg))

class Enemy(pg.sprite.Sprite): #Enemy class with functions for each type
    def __init__(self, game, type, roomx, roomy, x, y, chasetype, speed, animationspeed):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game structure class to this object
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.speed = speed
        self.chasetype = chasetype
        self.animation_speed = animationspeed

        self.init_type(type) #Call specific init function and give it the type

        #Image and hitbox
        self.current_image = 0
        self.image = pg.image.load(self.default_image)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #Add to sprite groups
        self.game.all_sg.add(self)
        self.game.enemy_sg.add(self)
        self.game.bgdeco_sg.add(self)
    
    def init_type(self, type): #Initialisation specific to the type of enemy
        if type == "slime":
            self.default_image = self.game.slime_images[0] 
            self.image_array = self.game.slime_images

    def animate(self): #Animation
        self.current_image += self.animation_speed
        if self.current_image >= len(self.image_array):
            self.current_image = 0
        self.image = pg.image.load(self.image_array[int(self.current_image)])
        self.image.set_colorkey(WHITE)

    def chase1(self): #Smooth chasing
        if self.game.movelock == False: #If movelock not on:
            if self.x > self.game.player.x:
                self.dx -= self.speed
            if self.x < self.game.player.x:
                self.dx += self.speed
            if self.y > self.game.player.y:
                self.dy -= self.speed
            if self.y < self.game.player.y:
                self.dy += self.speed
        else:
            self.dx, self.dy = 0,0
    
    def chase2(self): #Sharp chasing
        if self.game.movelock == False: #If movelock not on:
            #Horizontal
            if self.x < self.game.player.x + 16 and self.x > self.game.player.x - 16:
                self.dx = 0
                if self.y > self.game.player.y:
                    self.dy -= self.speed
                if self.y < self.game.player.y:
                    self.dy += self.speed
            #Vertical
            elif self.y < self.game.player.y + 16 and self.y > self.game.player.y - 16:
                self.dy = 0
                if self.x > self.game.player.x:
                    self.dx -= self.speed
                if self.x < self.game.player.x:
                    self.dx += self.speed
            else:
                self.dx, self.dy = 0,0
        else:
            self.dx, self.dy = 0,0

    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the Enemy's chunk doesnt match player chunk:
            self.game.all_sg.remove(self)
            self.game.enemy_sg.remove(self)
            self.game.bgdeco_sg.remove(self)

        #Animate the slime
        self.animate()

        #Chase the player
        if self.chasetype == 0:
            pass
        elif self.chasetype == 1:
            self.chase1() 
        elif self.chasetype == 2:
            self.chase2()
       
        #Calls check wall collision method
        self.rect.x = self.x #Set slime x rect hitbox equal to slime x location
        self.check_collision("x") #Check x axis wall collisions
        self.rect.y = self.y #Set slime y rect hitbox equal to slime y location
        self.check_collision("y") #Check y axis wall collisions

        self.x += self.dx #Change player x position by delta x per frame
        self.y += self.dy #Change player y position by delta y per frame

    def check_collision(self,axis):
        #Wall collisions:
        if axis == "x":
            wallhit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls x?
            if wallhit:
                if self.dx > 0: #If moving right (x increasing)
                    self.x = wallhit[0].rect.left - self.rect.width #set player x (left side) to equal the xpos of object hit minus the player width (collision right)
                if self.dx < 0: #If moving left (x decreasing)
                    self.x = wallhit[0].rect.right #set player x (right side) to equal the xpos of object hit (collision left)
                self.dx = 0 #Else x velocity is 0 as not moving horizontally
                self.rect.x = self.x #Update x rect or "hitbox"
                
        if axis == "y":
            wallhit = pg.sprite.spritecollide(self, self.game.wall_sg, False) #Player collides with walls y?
            if wallhit:
                if self.dy < 0: #If moving up (y incresing)
                    self.y = wallhit[0].rect.bottom #set player y (bottom side) to equal the ypos of object hit (collision up)
                if self.dy > 0: #If moving down (y decreasing)
                    self.y = wallhit[0].rect.top - self.rect.height #set player y (top side) to equal the ypos of object hit minus the player height (collision down)
                self.dy = 0 #Else y velocity is 0 as not moving vertically
                self.rect.y = self.y

        #Offscreen block:
        if self.y < TILESIZE + 5: #If touching top border:
            self.y = TILESIZE + 9
            self.dy = 0
        if self.y > HEIGHT - TILESIZE - 5: #If touching bottom border:
            self.y = HEIGHT - TILESIZE - 7
            self.dy = 0
        if self.x > WIDTH - TILESIZE - 20: #If touching right border:
            self.x = WIDTH - TILESIZE - 24
            self.dx = 0
        if self.x < TILESIZE + 5: #If touching left border:
            self.x = TILESIZE + 9
            self.dx = 0
        
#CONSTANTS:
FPS = 60
TILESIZE = 32
#Screen size (16x13 Tiles, 512x416 Pixels)
WIDTH = TILESIZE*16  
HEIGHT = TILESIZE*13
#Colours (RGB)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#GAME INSTANCE
game = Game()