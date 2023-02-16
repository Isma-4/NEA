#IMPLEMENTATION FOR NEA 2022 - 2023 "MINI RPG" BY ISMAEL

#LIBRARIES:
import pygame as pg             #Pygame - used for OOP in python (imported as "pg" as shorthand to improve efficiency when coding)
from pygame import mixer        #Used for the sounds that will be played within the program
import csv                      #CSV    - used to read the csv files that will store the map data of the game
import random                   #Random - used to randomise certain events to make the gameplay more interesting
import os, sys
import tkinter as tk            #Library used for creating a GUI
from tkinter import messagebox  #Fetch all resources from the library
from tkinter import * 
import sqlite3                  #Library used to embed an SQL database into the python program
import uuid                     #Universally Unique Identifiers - Will be used to create the ID (Primary key) for the user

#CLASSES:
class GUI(): #GUI for sign up/log in before game runs
    def __init__(self):
        self.setupTables() #Calls the method to create the database tables
        self.default_gamedata_values = "'0','0','0','96','96','0,0,0,0,0,0,0,0,0'"
        self.default_gamedata = "phase ='0',roomx='0',roomy='0',x='96',y='96',switch='0,0,0,0,0,0,0,0,0'"
        self.root = Tk()
        self.root.resizable(width=0,height=0) # size change Not allowed 
        self.root.geometry("220x200")
        self.root.title("Login")
        self.login_button = Button(self.root, width=30, height=6, bg="light green", text="[LOGIN]", command=self.login)
        self.login_button.grid(column=1, row=0)
        self.cnu_button = Button(self.root, width=30, height=6, bg="light blue", text="[SIGN UP]", command=self.signUp)
        self.cnu_button.grid(column=1, row=1)
        self.root.mainloop()

    def setupTables(self):
        self.con = sqlite3.connect("MINI_RPG_NEA_DATABASE.db") #Connects the python program to the sqlite3 database 
        self.cur = self.con.cursor() #Allows for fetching data from query returns and allows for embeded SQL statements within the python code

        #self.cur.execute('''DROP TABLE users''')
        #self.cur.execute('''DROP TABLE gamedata''')
        
        #User table
        try: #Tries to create the user table
            self.cur.execute('''CREATE TABLE users (id text, username text, password text)''')
            self.con.commit()
        except: #If table already exists, ignore the error.
            pass
        
        try: #Tries to create the gamedata table
            self.cur.execute('''CREATE TABLE gamedata (id text, phase text, roomx text, roomy text, x text, y text, switch text)''')
            self.con.commit()
        except: #If table already exists, ignore the error.
            pass
        
    def login(self):
        self.login_button.grid_remove()
        self.cnu_button.grid_remove()

        self.username_label = tk.Label(self.root, text="Username:", width=8, bg="grey")
        self.username_label.grid(column=0, row=0)
        self.password_label = tk.Label(self.root, text="Password:", width=8, bg="grey")
        self.password_label.grid(column=0, row=1)

        self.username_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.username_textbox.grid(column=1, row=0)
        self.password_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.password_textbox.grid(column=1, row=1)

        self.login_button = tk.Button(self.root, text="[LOGIN]", width=22, height=10, bg="light green", command=self.loginVerification)
        self.login_button.grid(column=1, row=2) 

        self.back_button = tk.Button(self.root, text="[BACK]", width=8, height=10, bg="light blue", command=self.back)
        self.back_button.grid(column=0, row=2) 

    def signUp(self):
        self.login_button.grid_remove()
        self.cnu_button.grid_remove()

        self.username_label = tk.Label(self.root, text="Username:", width=8, bg="grey")
        self.username_label.grid(column=0, row=0)
        self.password_label = tk.Label(self.root, text="Password:", width=8, bg="grey")
        self.password_label.grid(column=0, row=1)

        self.username_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.username_textbox.grid(column=1, row=0)
        self.password_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.password_textbox.grid(column=1, row=1)

        self.login_button = tk.Button(self.root, text="[SIGN UP]", width=22, height=10, bg="light green", command=self.signUpVerification)
        self.login_button.grid(column=1, row=2) 

        self.back_button = tk.Button(self.root, text="[BACK]", width=8, height=10, bg="light blue", command=self.back)
        self.back_button.grid(column=0, row=2) 

    def loginVerification(self):
        self.username = self.username_textbox.get("1.0", tk.END)
        self.password = self.password_textbox.get("1.0", tk.END)

        self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE username='" + self.username + "'")
        if self.res.fetchone()[0] == 1: #Is count of matching username equal to 1? (Does username exist in database?)
            self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE password='" + self.password + "'")
            if self.res.fetchone()[0] == 1: #Is count of matching password equal to 1? (Does password exist in database?)
                #messagebox.showinfo(title="LOG IN", message="Log In Complete, welcome " + self.username)

                self.cur.execute("SELECT id FROM users WHERE username='" + self.username + "'") #Get the id of the current user
                id_object = self.cur.fetchall() #Returns the id as a list within an SQL object
                for item in id_object: #Cycle through the items within the list (only the id in this case)
                    item = str(item) #Convert to string form
                    self.currentID = item[2:len(item)-3] #Removes the quotation marks and brackets from the start and end of the id
                self.chooseGame()
            else:
                messagebox.showinfo(title="ERROR", message="Password incorrect")
        else:
            messagebox.showinfo(title="ERROR", message="Username incorrect")
        
    def signUpVerification(self):
        self.username = self.username_textbox.get("1.0", tk.END)
        self.password = self.password_textbox.get("1.0", tk.END)

        specialChars = ["!","£","$","%","^","&","*","?","#","@"] #List of accepted special chars
        passwordContainsSpecialChar = False #By default this value is set to false
        newUuid = str(uuid.uuid4()) #Creates a new unique identifier which will be used as the primary key for the user

        if len(self.username) >= 4 and len(self.username) <= 20: #Checks if the length of username is valid
            self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE username='" + self.username + "'") #Returns count of how many IDs match that username in the database
            if self.res.fetchone()[0] == 0: #Is count of matching username equal to 0?
                if len(self.password) >= 4 and len(self.password) <= 12: #Checks if the length of password is valid
                    for char in self.password: #Loop through each character in password
                        if specialChars.count(char) > 0: #Check if the number of times that the current char = one of the special chars is greater than 0
                            passwordContainsSpecialChar = True 
                    if passwordContainsSpecialChar == True: #If entered password contains atleast one special char:
                        self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE password='" + self.password + "'") #Returns count of how many IDs match that password in the database
                        if self.res.fetchone()[0] == 0: #Is count of matching password equal to 0?
                            self.cur.execute("INSERT INTO users VALUES ('" + newUuid + "','" + self.username + "','" + self.password + "')") #Create new user with the following fields
                            self.con.commit()
                            self.cur.execute("INSERT INTO gamedata VALUES ('" + newUuid + "'," + self.default_gamedata_values + ")") 
                            self.con.commit()
                            self.back()


                        else:
                            messagebox.showinfo(title="ERROR", message="Password taken")   
                    else:
                        messagebox.showinfo(title="ERROR", message="Password must containt atleast one of [!,£,$,%,^,&,*,?,#,@]")   
                else:
                    messagebox.showinfo(title="ERROR", message="Password must be between 3 and 12")      
            else:
                messagebox.showinfo(title="ERROR", message="Username taken")
        else:
            messagebox.showinfo(title="ERROR", message="Username must be between 3 and 20 char")

    def chooseGame(self):
        self.login_button.grid_remove()
        self.back_button.grid_remove()
        self.username_label.grid_remove()
        self.password_label.grid_remove()
        self.username_textbox.grid_remove()
        self.password_textbox.grid_remove()
        
        self.new_game_button = Button(self.root, width=30, height=6, bg="light pink", text="[NEW GAME]", command=self.newGame)
        self.new_game_button.grid(column=1, row=0)
        self.load_game_button = Button(self.root, width=30, height=6, bg="light blue", text="[LOAD GAME]", command=self.loadGame)
        self.load_game_button.grid(column=1, row=1)

    def newGame(self):
        self.cur.execute("UPDATE gamedata SET " + self.default_gamedata + "  WHERE id='" + self.currentID + "'") #Override current user's game data with default data
        self.con.commit()
        self.root.destroy()
        game = Game(self) #Instantiate game class with GUI object passed as parameter
        
    def loadGame(self):
        self.root.destroy()
        game = Game(self) #Instantiate game class with GUI object passed as parameter

    def back(self):
        self.root.destroy()
        GUI()

class Game(): #Game class acts as framework for the gam
    def __init__(self, gui): #Constructor for game class and runs at start of game
        pg.init()
        self.gui = gui
        self.load_gamedata()
        self.init_variables()
        mixer.init()
        self.init_spritegroups()
        self.load_media()
        self.game_text()
        self.init_objects()
        self.init_object_status()
        self.screen_setup()
        self.new_room(self.roomx,self.roomy)
        self.gameloop()

    def load_gamedata(self):
        self.gui.cur.execute("SELECT * FROM gamedata WHERE id='" + self.gui.currentID + "'") #Get the id of the current user
        self.user_record = self.gui.cur.fetchall() #Returns the record as a list within an SQL object

        x = list(self.user_record[0][6])    #Converts data from the gamedata table into a readable integer array
        self.switch_status = []
        for item in x:
            if item != ',':
                self.switch_status.append(int(item))

    def save_gamedata(self):

        print(self.switch_status)
        for index, item in enumerate(self.switch_status):
            self.switch_status[index] = str(item)
        switch_status = ' '.join(self.switch_status)

        self.current_gamedata = "phase='"+str(self.phase)+"',roomx='"+str(self.roomx)+"',roomy='"+str(self.roomy)+"',x='"+str(self.player.x)+"',y='"+str(self.player.y)+"',switch='"+switch_status+"'"
        self.gui.cur.execute("UPDATE gamedata SET " + self.current_gamedata + "  WHERE id='" + self.gui.currentID + "'") #Override current user's game data with default data
        self.gui.con.commit()
        self.running = False
        
    def init_variables(self): #Initialise global game variables
        self.running = True
        self.clock = pg.time.Clock()
        self.gamemode = "MENU"

        self.phase = int(self.user_record[0][1])
        self.roomx = int(self.user_record[0][2])
        self.roomy = int(self.user_record[0][3])
        self.border_colour = (153,50,204)
        self.showtextbox = False
        self.textcount = 0 #Used to cycle through textbox pages
        self.textcount2 = 0 #Used in the case where there is only one textbox page
        self.current_page = 0 #Current page of textboxx being viewed
        self.movelock = False
        self.ispaused = False #Status of whether or not the game is in the pause menu
        self.yesno = False #Toggle for if the player is in a yes or no option textbox
        self.pauselock = False #Toggles whether or not a pause is permitted
        self.show_pause_ui = False

        self.screenfill_show = False #Variable to toggle filling the screen (TEMP)
        self.gameinfotext_show = False #Variable to toggle showing game info (TEMP)
        self.interacttiles_show = False #Variable to toggle showing interact tiles (TEMP)
        self.grid_show = False #Variable to toggle showing grid (TEMP) 

        self.current_image = 0

        self.current_time = 0 #By default game time is 0
        self.timepoint = 0 #Point in time for an event default to 0
        self.timepassed = 0 #Time elapsed from timepoint to current time default 0
        self.timelock = False #lock used to instantaneously get a timepoint

        self.cooldown1 = 0 #Used as an alternative method for delay timers

        self.font35 = pg.font.SysFont("Aerial", 35)
        self.font25 = pg.font.SysFont("Aerial", 25)
        self.font15 = pg.font.SysFont("Aerial", 15)

        self.action = False #Toggle for when action key is pressed

        self.controller_right = False #Controller input variables
        self.controller_left = False
        self.controller_up = False
        self.controller_down = False

        self.is_playing_music = False #Checks if background music is being played

    def init_spritegroups(self): #Initialise sprite groups
        self.player_sg = pg.sprite.Group() #Player only
        self.enemy_sg = pg.sprite.Group()
        self.all_sg = pg.sprite.Group() #All sprites (used to update all sprites)
        self.playerbullets_sg = pg.sprite.Group()

        #Tile layers
        self.floor_sg = pg.sprite.Group() #Floor tile sprite group
        self.bgdeco_sg = pg.sprite.Group() #For background decoration that can be walked over
        self.fgdeco_sg = pg.sprite.Group() #For foreground decoration that will be above the player
        self.wall_sg = pg.sprite.Group() #Wall tile sprite group
        self.interacttile_sg = pg.sprite.Group() #Tiles that trigger something if player touches

        #UI
        self.border_sg = pg.sprite.Group() #Sprite group for border tiles
        self.textbox_sg = pg.sprite.Group() #Sprite group for all textbox components

        #Object sprite groups
        self.switch_sg = pg.sprite.Group() #Sprite group for all switches
        self.item_sg = pg.sprite.Group() #Sprite group for all items visible on screen

    def init_objects(self): #Initialise objects
        #Player
        self.player = Player(self,int(self.user_record[0][4]),int(self.user_record[0][5]))
        
        self.playerbullet = Bullet(self)

        #HP Bar
        self.hpbar = Hpbar(self)

        #Black screen for fading to black
        self.black_screen = pg.Surface((WIDTH, HEIGHT))
        self.black_screen.fill(BLACK)
        self.black_screen_alpha = 0
        self.black_screen_midpoint = False

        #############TEST CONTROLLER SUPPORT
        self.joysticks = []
        for i in range(pg.joystick.get_count()):
            self.joysticks.append(pg.joystick.Joystick(i))
            print(self.joysticks)
            self.joysticks[-1].init()
        
    def init_object_status(self): #Initialise the default status of objects
        self.toggledoor_status = [0,0,0,0,0,0,0,0,0] #List to hold status of all doors, starting with default
        #self.switch_status =     [0,0,0,0,0] #List to hold status of all buttons, starting with default   
        #self.switch_status = self.user_record[0][6]
        self.item_collected =    [0,0,0] #List to hold boolean values whether an in game item has been collected
        self.keydoor_status =    [0] #List to hold the status of all keydoors
        
    def load_media(self): #Loads all images that will be used in the program
        #BORDER IMAGES:
        self.border_image = pg.image.load("Tiles/tile0.png")

        #PLAYER IMAGES:
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
        self.p_shooting_images = []
        self.p_shooting_images.append(pg.image.load("Player/PlayerShooting/p_u_shoot.png"))
        self.p_shooting_images.append(pg.image.load("Player/PlayerShooting/p_d_shoot.png"))
        self.p_shooting_images.append(pg.image.load("Player/PlayerShooting/p_l_shoot.png"))
        self.p_shooting_images.append(pg.image.load("Player/PlayerShooting/p_r_shoot.png"))

        #NPC IMAGES:
        #Janitor
        self.npc1_u_animate = [] #Packet of frames for down animation
        self.npc1_u_animate.append(pg.image.load("Npc/npc1_janitor/npc1_u_1.png")) # 2 frame repeated twice as each frame "packet"
        self.npc1_u_animate.append(pg.image.load("Npc/npc1_janitor/npc1_u_1.png")) # should have 4 frames to stay consistent for the
        self.npc1_u_animate.append(pg.image.load("Npc/npc1_janitor/npc1_u_2.png")) # player and npc movement animations. Janitor wont
        self.npc1_u_animate.append(pg.image.load("Npc/npc1_janitor/npc1_u_2.png")) # ever move up so these 2 frames are for idling animation
        self.npc1_d_animate = [] #Packet of frames for down animation              # (bobbing up and down while stationary)
        self.npc1_d_animate.append(pg.image.load("Npc/npc1_janitor/npc1_d_1.png"))
        self.npc1_d_animate.append(pg.image.load("Npc/npc1_janitor/npc1_d_2.png"))
        self.npc1_d_animate.append(pg.image.load("Npc/npc1_janitor/npc1_d_3.png"))
        self.npc1_d_animate.append(pg.image.load("Npc/npc1_janitor/npc1_d_4.png"))
        self.npc1_r_animate = [] #Packet of frames for down animation
        self.npc1_r_animate.append(pg.image.load("Npc/npc1_janitor/npc1_r_1.png"))
        self.npc1_r_animate.append(pg.image.load("Npc/npc1_janitor/npc1_r_2.png"))
        self.npc1_r_animate.append(pg.image.load("Npc/npc1_janitor/npc1_r_3.png"))
        self.npc1_r_animate.append(pg.image.load("Npc/npc1_janitor/npc1_r_4.png"))

        #OBJECTS:
        #Door images
        self.door_images = [] #Array that holds all the door images
        self.door_images.append("2stateTiles/doors/tile0.png") 
        self.door_images.append("2stateTiles/doors/tile1.png")
        self.door_images.append("2stateTiles/doors/tile2.png") 
        self.door_images.append("2stateTiles/doors/tile3.png")
        self.door_images.append("2stateTiles/doors/tile4.png")
        self.door_images.append("2stateTiles/doors/tile5.png")
        #Button images
        self.switch_images = []
        self.switch_images.append("2stateTiles/switches/tile0.png")
        self.switch_images.append("2stateTiles/switches/tile1.png")
        self.switch_images.append("2stateTiles/switches/tile2.png")
        self.switch_images.append("2stateTiles/switches/tile3.png")
        self.switch_images.append("2stateTiles/switches/tile4.png")
        self.switch_images.append("2stateTiles/switches/tile5.png")
        self.switch_images.append("2stateTiles/switches/tile6.png")
        self.switch_images.append("2stateTiles/switches/tile7.png")
        
        #ENEMIES:
        #Slime
        self.slime_move_images = ["Enemies/slime/slime_move/tile0.png", "Enemies/slime/slime_move/tile1.png"] #Array that holds all the door images
        self.slime_hit_image = "Enemies/slime/slime_hit.png"
        self.slime_death_image = "Enemies/slime/slime_death.png"
        #Laser
        self.laser1_images = ["Enemies/lasers/laser1/tile0.png", "Enemies/lasers/laser1/tile1.png","Enemies/lasers/laser1/tile2.png"] #1 tile high laser

        #UI IMAGES:
        self.textbox_img = pg.image.load("UI/textbox.png") #Textbox
        self.pause_ui_bg_img = pg.image.load("UI/pause_ui_bg.png") #Pause screen bg
        #Pause arrow
        self.pause_arrow_img = pg.image.load("UI/pause_arrow.png")
        self.pause_arrow_img.set_colorkey(WHITE)
        self.pause_arrow_show = False
        self.pause_arrow_x, self.pause_arrow_y = 0, 0 #Placeholder start pos (gets set later)
        self.pause_arrow_defaultx, self.pause_arrow_defaulty = TILESIZE*5.8, TILESIZE*3.9 #Default position
        self.pause_arrow_item = 0 #Placeholder
        #Textbox arrow
        self.arrow = pg.image.load("UI/arrow.png")
        self.arrow.set_colorkey(WHITE)
        self.arrowx = TILESIZE*13.5
        self.arrowy = TILESIZE*10
        #Query icon
        self.qicon = pg.image.load("UI/query_icon.png")
        self.qicon_show = False
        self.qicon.set_colorkey(WHITE)
        self.qiconx = TILESIZE*1.2
        self.qicony = TILESIZE*1.2
        #Hpbar border
        self.hpbar_border_image = pg.image.load("UI/hpbar_border.png")

        #BACKGROUNDS:
        self.menubg_animate = []
        self.menubg_animate.append(pg.image.load("Backgrounds/bg1.png"))
        self.menubg_animate.append(pg.image.load("Backgrounds/bg2.png"))
        
        #ITEMS:
        self.item_images = []
        self.item_images.append(pg.image.load("Items/icon/screwdriver.png"))

        #SOUND:
        self.switch_sound = mixer.Sound("switch.wav")
        self.spooky_sound = mixer.Sound("spooky.wav")
        self.click_sound = mixer.Sound("click.wav")
        self.bg1_sound = mixer.Sound("bg1.wav")
        self.item_obtain_sound = mixer.Sound("item_obtain.wav")

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

    def spawn_tiles(self, roomx, roomy): #Initialise the static tiles in a given room
        #Clear old tiles
        self.floor_sg.empty()
        self.wall_sg.empty()
        self.fgdeco_sg.empty()
        self.bgdeco_sg.empty()
        self.interacttile_sg.empty()

        #Add tiles to sprite groups
        self.layers = ["MAP_Floors.csv", "MAP_InteractTiles.csv", "MAP_Walls.csv", "MAP_ForegroundDecoration.csv", "MAP_BackgroundDecoration.csv"] #Layers of the tilemap
        
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

                                if layer == self.layers[0]: #If on floor layer:
                                    if tile == "129":
                                        self.atile = Tile(self, "animatedfloor", roomx, roomy, x, y, 0, 5, 0, 1, 0.01, BLACK)
                                    else:
                                        new_tile = Tile(self, "static", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                        self.floor_sg.add(new_tile) #Classify this new tile as a floor tile
                                if layer == self.layers[1]: #If on interact tile layer:                     
                                    if tile == "72": #Down interact tile:
                                        new_tile = Tile(self, "interactdown", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    elif tile == "73": #Left interact tile:
                                        new_tile = Tile(self, "interactleft", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    elif tile == "74": #Up interact tile:
                                        new_tile = Tile(self, "interactup", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    elif tile == "75": #Right interact tile:
                                        new_tile = Tile(self, "interactright", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    self.interacttile_sg.add(new_tile)
                                if layer == self.layers[2]: #If on wall layer:
                                    #Animated Tiles:
                                    if tile == "89": #Gel lamp
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 4, 0, 1, 0.05, BLACK)
                                    elif tile == "100": #Pump
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 1, 0, 4, 0.05, BLACK)
                                    elif tile == "101": #NPC Janitor
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 3, 0, 1, 0.05, WHITE) 
                                    elif tile == "102": #Terminal
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 0, 0, 1, 0.035, WHITE)
                                    elif tile == "103": #Medbay monitor
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 2, 0, 1, 0.05, WHITE)
                                    elif tile == "126": #Top half of vending machine
                                        self.atile = Tile(self, "animatedwall", roomx, roomy, x, y, 0, 3, 0, 1, 0.05, WHITE)
                                    else:
                                        new_tile = Tile(self, "static", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                        self.wall_sg.add(new_tile) #Classify this new tile as a wall tile
                                if layer == self.layers[3]: #If on fg deco layer:
                                    new_tile = Tile(self, "static", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    self.fgdeco_sg.add(new_tile) #Classify this new tile as a fg deco tile
                                if layer == self.layers[4]: #If on bg deco layer:
                                    new_tile = Tile(self, "static", self.roomx, self.roomy, x, y, image, 0, 0, 0, 0, WHITE)
                                    self.bgdeco_sg.add(new_tile) #Classify this new tile as a bg deco tile
                               
    def new_room(self, roomx, roomy): #Initalise the animated tiles and objects for all rooms
        self.music()
        self.all_sg.empty() #Clear the all sprite group
        self.all_sg.add(self.player) #Re add the player
        self.spawn_tiles(roomx,roomy) #Spawn all the static tiles needed for the current room
        if roomx == 0 and roomy == 0: #ROOM 0 0
            self.switch = Switch(self, roomx, roomy, 1, 0, 1, TILESIZE*4, TILESIZE*7, "up") 
            self.door = Door(self, "toggle", roomx, roomy, 1, 1, TILESIZE*3, TILESIZE*11) 
        if roomx == 0 and roomy == 1: #ROOM 0 1
            self.door = Door(self, "key", roomx, roomy, 0, 2, TILESIZE*5, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, 1, 1, TILESIZE*3, TILESIZE*1) 
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*9, TILESIZE*10, "up")
            if self.phase < 3:
                self.janitor = Npc(self, "janitor", 0, roomx, roomy, TILESIZE*3, TILESIZE*6) 
        if roomx == 0 and roomy == 2: #ROOM 0 2
            if self.phase == 3:
                self.janitor = Npc(self, "janitor", 1, roomx, roomy, TILESIZE*10, TILESIZE*10)
            elif self.phase == 4:
                self.janitor = Npc(self, "janitor", 2, roomx, roomy, TILESIZE*11, TILESIZE*10)
        if roomx == 1 and roomy == 0: #ROOM 1 0
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*4, TILESIZE*2, "up") 
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*13, TILESIZE*6)
        if roomx == 1 and roomy == 1: #ROOM 1 1
            self.switch = Switch(self, roomx, roomy, 2, 6, 7, TILESIZE*13, TILESIZE*2, "up") 
            self.door = Door(self, "toggle", roomx, roomy, 2, 5, TILESIZE*12, TILESIZE*3) 
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*3, TILESIZE*5) 
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*10, TILESIZE*5)
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*10, TILESIZE*9) 
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*3, TILESIZE*9) 
        if roomx == 1 and roomy == 2: #ROOM 1 2 ----------------------------PUZZLE ROOM 1--------------------------------------------------------
            #Orange doors:
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*9, TILESIZE*2)
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*8, TILESIZE*4)
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*12, TILESIZE*6)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*6, TILESIZE*8)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*3, TILESIZE*5) 
            #Orange switches:
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*11, TILESIZE*4, "up")
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*3, TILESIZE*2, "up")
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*8, TILESIZE*8, "up")
            #Green doors:
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*10, TILESIZE*3) 
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*3, TILESIZE*3) 
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*6, TILESIZE*4) 
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*11, TILESIZE*6)
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*10, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*6, TILESIZE*9) 
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*3, TILESIZE*9) 
            #Green switches:
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*12, TILESIZE*2, "up")
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*8, TILESIZE*6, "up")
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*9, TILESIZE*10, "up")
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*2, TILESIZE*10, "up")
            #Red doors:
            self.door = Door(self, "toggle", roomx, roomy, 2, 5, TILESIZE*14, TILESIZE*9)
            self.door = Door(self, "toggle", roomx, roomy, -2, 5, TILESIZE*3, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, -2, 5, TILESIZE*9, TILESIZE*4)
            #Red switches:
            self.switch = Switch(self, roomx, roomy, 2, 6, 7, TILESIZE*4, TILESIZE*10, "up")
        if roomx == 1 and roomy == 3: #ROOM 1 3
            self.slime = Enemy(self, "slime", roomx, roomy, TILESIZE*10, TILESIZE*7, 1, 0.005, 0.05)  
        if roomx == 2 and roomy == 0: #ROOM 2 0
            self.door = Door(self, "toggle", roomx, roomy, 2, 5, TILESIZE*7, TILESIZE*8)
            self.screwdriver = Item(self, 0, roomx, roomy, TILESIZE*10.25, TILESIZE*3.8) #Screwdriver 
        if roomx == 2 and roomy == 1: #ROOM 2 1
            self.door = Door(self, "toggle", roomx, roomy, -2, 5, TILESIZE*3, TILESIZE*5)
            self.switch = Switch(self, roomx, roomy, 2, 6, 7, TILESIZE*2, TILESIZE*6, "up")
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*3, TILESIZE*7)
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*2, TILESIZE*8, "up")
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*3, TILESIZE*9)
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*2, TILESIZE*10, "up")
        if roomx == 2 and roomy == 2: #ROOM 2 2 ----------------------------PUZZLE ROOM 2--------------------------------------------------------
            #Orange doors:
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*2, TILESIZE*2)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*4, TILESIZE*3)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*9, TILESIZE*5)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*13, TILESIZE*6)
            self.door = Door(self, "toggle", roomx, roomy, 4, 4, TILESIZE*7, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*10, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, -4, 4, TILESIZE*9, TILESIZE*9)
            #Orange switches:
            self.switch = Switch(self, roomx, roomy, 4, 4, 5, TILESIZE*12, TILESIZE*10, "up")
            #Green doors:
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*2, TILESIZE*3)
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*9, TILESIZE*3)
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*13, TILESIZE*3)
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*9, TILESIZE*6)
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*3, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, -3, 3, TILESIZE*8, TILESIZE*7)
            self.door = Door(self, "toggle", roomx, roomy, 3, 3, TILESIZE*12, TILESIZE*7)
            #Green switches:
            self.switch = Switch(self, roomx, roomy, 3, 2, 3, TILESIZE*10, TILESIZE*4, "up")
            #Red doors:
            self.door = Door(self, "toggle", roomx, roomy, 2, 5, TILESIZE*2, TILESIZE*4)
            self.door = Door(self, "toggle", roomx, roomy, 2, 5, TILESIZE*1, TILESIZE*9)
            self.door = Door(self, "toggle", roomx, roomy, -2, 5, TILESIZE*11, TILESIZE*10)
            #Red switches:
            self.switch = Switch(self, roomx, roomy, 2, 6, 7, TILESIZE*6, TILESIZE*5, "up")
            self.switch = Switch(self, roomx, roomy, 2, 6, 7, TILESIZE*11, TILESIZE*7, "up")
        
    def game_text(self): #Loads text used in textboxes
        #Game text:
        self.gametext1 = ["Use WASD keys to move and the O key"]
       
        #Sign text:
        self.signtext1 = ["Holding Chamber (^)", "Supply Room (V)      Tunnel A (>)"]
        self.signtext2 = ["Test Labrynth A (V)"]
        self.signtext3 = ["Tunnel A (^)"]
        self.signtext4 = ["Subject 48 Convert Station (^)"]
        self.signtext5 = ["<Holding Chamber>"]

        #NPC text:
        self.npc1text1 = []
        self.npc1text2 = []
        self.npc1text3 = []
        self.npc1text1.append("You're awake from your coma!")
        self.npc1text1.append("I must notify the head scientist at once")
        self.npc1text1.append("but the path is blocked by a faulty door")
        self.npc1text1.append("I'd fix it easily if i had my screwdriver,")
        self.npc1text1.append("but I can't find it anywhere.")
        self.npc1text1.append("Let me know if you find it")
        self.npc1text2.append("You found my screwdriver?")
        self.npc1text2.append("<You give screwdriver>")
        self.npc1text3.append("It's dangerous out there!")
        self.npc1text3.append("You need a weapon to defend yourself")

        #Object text:
        self.objecttext1 = ["Looks like a pump of some sort", "It emits an ominous green glow"]
        self.objecttext2 = ["The monitors look broken and stuck in a", "looping pattern yet they seem somewhat", "familiar"]
        self.objecttext3 = ["These hospital beds are hooked up to IVs","full of a green liquid"]
        self.objecttext4 = ["< TERMINAL LOCKED >"]
        self.objecttext5 = ["These servers look abandoned and dusty"]
        self.objecttext6 = ["< NORTH WEST PLANT A>"]
        self.objecttext7 = ["The buttons look slimy"]
        self.objecttext8 = ["The hinge is slightly broken", "theres $17 inside!"]
        self.objecttext9 = ["Not enough money"]
        self.objecttext10 = ["Already purchased"]
        self.objecttext11 = ["Smells like metal and decaying flesh"]

        #Yes no text
        self.yesnotext1 = ["PP-19 Bizon <$15>  [Y]       [N]"]

        #Item text:
        self.itemtext1 = ["<You obtained screwdriver>"]

    def timer(self, delay): #Used to allow a delay (NEEDS FIXING)
        if self.timelock == False:
            self.timepoint = pg.time.get_ticks()
            self.timelock = True
        if self.timepassed > delay:
            self.timelock = False
            return True

    def ui_update(self): #Updates to the query icon, textbox arrow etc
        #Update bottom right textbox arrow movement 
        if self.arrowy < TILESIZE*10.5:
            self.arrowy += 0.3
        else:
            self.arrowy = TILESIZE*10
        
        if self.yesno == False: #Move pause arrow like such if not in the yesno textbox page (if in the pause menu)
            if self.pause_arrow_y == self.pause_arrow_defaulty:
                self.pause_arrow_item = "resume"
            elif self.pause_arrow_y == self.pause_arrow_defaulty + TILESIZE*0.75:
                self.pause_arrow_item = "save"
            elif self.pause_arrow_y == self.pause_arrow_defaulty + TILESIZE*1.5:
                self.pause_arrow_item = "items"

            #Update pause arrow movement 
            if self.pause_arrow_x > TILESIZE*5.8:
                self.pause_arrow_x -= 0.15
            else:
                self.pause_arrow_x = TILESIZE*6
            
        self.pause_arrow_y = round(self.pause_arrow_y, 1) #Always round to one dp (helps with checks in draw function)

        #Update query icon movement
        if self.qicony < TILESIZE*1.4:
            self.qicony += 0.1
        else:
            self.qicony = TILESIZE*1.2

    def setup_textbox(self, textboxtype, colour1, title, colour2, text_array): #Configures a new textbox with given parameters
        #Parameters: textboxtype: Is the textbox manually action spawned or auto spawned?
        #            colour1, colour2 : Colours for the title and text
        #            title, text_array: The text that will be displayed as the title and text respectively

        self.movelock = True #Lock movement while the textbox is true
        self.pauselock = True #Lock ability to pause game
        self.current_page = 1 #Default current page being viewed 
        self.textboxtype = textboxtype
        self.textcolour1, self.textcolour2 = colour1, colour2
        self.titletext, self.text_array = title, text_array
        self.titletext_x, self.titletext_y = TILESIZE*2, TILESIZE*7
        self.text_x, self.text_y = TILESIZE*2.5, TILESIZE*9
        self.showtextbox = True #Will update all textbox components in gameloop update section
    
    def draw_textbox(self): #Draws all components of the textbox onto the screen
        self.titletext_surface = self.font35.render(self.titletext,True,self.textcolour1) #Create the text surface with the parameters
        self.text_surface = self.font25.render(self.text_array[self.textcount-1],True,self.textcolour2) 

        self.screen.blit(self.textbox_img,(TILESIZE*1.5,TILESIZE*6.5)) #Draw box
        self.screen.blit(self.titletext_surface,(self.titletext_x, self.titletext_y)) #Draw title
        self.screen.blit(self.text_surface,(self.text_x, self.text_y)) #Draw text
        if not self.yesno: #Dont draw bottom right arrow if in yes no textbox page since that will already have an arrow to choose option
            self.screen.blit(self.arrow,(self.arrowx,self.arrowy))
        
        
        if self.action:
            self.click_sound.play()
            if self.yesno == True: #Is the current textbox page a yes no choice?
                self.pause_arrow_show = True
                self.pause_arrow_x, self.pause_arrow_y = TILESIZE*8.4, TILESIZE*9
                self.pause_arrow_item = "yes" #As default pos is on the yes option
            
            else:
                self.pause_arrow_show = False
                #The case where the textbox has more than one page:
                if len(self.text_array) > 1:
                    if self.textcount < len(self.text_array): 
                        self.textcount += 1 #Increment count
                    else:
                        self.textcount = 0 #Reset count
                        self.clear_textbox()
                
                #The case where the textbox has only one page
                else:            
                    if self.textcount2 < 1:
                        self.textcount2 += 1 #Increment count2
                    else:
                        self.clear_textbox()
                        self.textcount2 = 0 #Reset count2
    
    def clear_textbox(self): #Removes the textbox
        self.showtextbox = False
        self.pauselock = False
        self.arrow_show = False
        self.textcolour1, self.textcolour2 = BLACK, BLACK
        self.titletext_x, self.titletext_y = -100, -100
        self.text_x, self.text_y = -100, -100
        self.movelock = False
        self.yesno = False
        self.pause_arrow_show = False
    
    def room_event(self,x,y): #All events in each specific room

        def inspect(type, sprite, alternate_command, textboxtype, c1, title, c2, text_array):
            #Type parameter specifies what type of interaction has occured
            #If type = switch, the target sprite specified will be affected
            #If type = textbox, the last 5 parameters will be used to call a textbox
            #Alternate command is what occurs when the textbox has ended
            self.qicon_show = True #Show the query icon in the top left
            if self.action == True and self.ispaused == False: #If action key pressed and game not paused:
                if type == "switch":
                    sprite.switch()
                    self.switch_sound.play()
                if type == "textbox":
                    if self.showtextbox == False:
                        self.setup_textbox(textboxtype, c1, title, c2, text_array)
                if type == "yesnotextbox":
                    if self.showtextbox == False:
                        self.setup_textbox(textboxtype, c1, title, c2, text_array)
                        if text_array != x and self.current_page == len(text_array):
                            self.yesno = True
                    else:
                        if self.pause_arrow_item == "yes": #Yes option picked
                            if self.roomx == 2 and self.roomy == 1: #Vending machine --------------------------------------------
                                if not self.item_collected[2]:
                                    if self.player.coins >= 15:
                                        self.player.coins -= 15
                                        self.item_collected[2] = True
                                        self.clear_textbox()
                                    else:
                                        self.yesno = False
                                        self.setup_textbox("textbox", BLACK, "Machine", BLACK, self.objecttext9)
                                else:
                                    self.yesno = False
                                    self.setup_textbox("textbox", BLACK, "Machine", BLACK, self.objecttext10)
                                    
                        else: #No option picked
                            self.clear_textbox()

                    
                if text_array != x and self.current_page > len(text_array): #If page that user is viewing of the textbox equals the number of pages (if all pages scrolled through)
                    if alternate_command != x: #If command isnt a placeholder x value
                        if alternate_command == "increment_phase":
                            self.phase += 1
                        if alternate_command[0] == "$": #Payment command (give player money)        #Payment parameter passed as:   "$117"
                            digit1 = alternate_command[2]                                           #The "$" indicates that coins will be given to the player
                            try:                                                                    #The second character is the id of the item_collected array so that it can be toggled off
                                digit2 = alternate_command[3]                                       #to ensure one time payment only
                                try:                                                                #The following 1 to 3 characters correspond to the payment amount
                                    digit3 = alternate_command[4]
                                    self.player.coins += int(digit1 + digit2 + digit3)
                                except:
                                    self.player.coins += int(digit1 + digit2)
                            except:
                                self.player.coins += int(digit1)
                            
                            if alternate_command[1] != "x":
                                self.item_collected[int(alternate_command[1])] = True
                                     
        self.qicon_show = False #Hide query icon by default

        #Switch Inspections:
        for switch in self.switch_sg:   
            if pg.sprite.collide_rect(self.player, switch):
                inspect("switch", switch, x, x, x, x, x, x)
        
        #Interact Tile Inspections:
        for itile in self.interacttile_sg:
            if pg.sprite.collide_rect(self.player, itile):
                if self.roomx == 0 and self.roomy == 0: #--------------------------------------------------------
                    if self.player.x > TILESIZE*8:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext1) #xs are placeholders as textbox parameters not needed in this case
                    else:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.signtext5)
                if self.roomx == 0 and self.roomy == 1: #--------------------------------------------------------
                    if self.player.x > TILESIZE*4: #Sign
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.signtext1) 
                    elif self.phase < 3:  #NPC1
                        if not self.item_collected[0]: #If screwdriver not obtained           
                            inspect("textbox", x, x, "manual", BLACK, "Janitor", BLACK, self.npc1text1)
                        elif self.item_collected[0]: #If screwdriver obtained
                            inspect("textbox", x, "increment_phase", "manual", BLACK, "Janitor", BLACK, self.npc1text2)                      
                if self.roomx == 0 and self.roomy == 2: #--------------------------------------------------------
                    if self.player.x < 3*TILESIZE:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext11)
                    elif self.player.x > 3*TILESIZE and self.player.x < TILESIZE*9: #Coin locker
                        if not self.item_collected[1]: #Makes sure money can only be taken once
                            inspect("textbox", x, "$117", "manual", BLACK, "---", BLACK, self.objecttext8)
                    elif self.player.x > TILESIZE*9.5 and self.player.x < TILESIZE*10.5 and self.phase == 3: #Janitor in position 2
                        if not self.item_collected[2]:
                            inspect("textbox", x, x, "manual", BLACK, "Janitor", BLACK, self.npc1text3)
                        else:
                            self.janitor.phase = 2
                            self.phase += 1
                    elif self.player.x > TILESIZE*11:
                        if self.player.y < TILESIZE*6: #Right side objects
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext6)
                        else:
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext7)
                if self.roomx == 1 and self.roomy == 0: #--------------------------------------------------------
                    if self.player.y > TILESIZE*4:
                        if (self.player.x < TILESIZE*4) or (self.player.x > TILESIZE*8):
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext2) #Medbay monitors
                        else:
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext3) #Medbay beds
                    else:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext4) #Terminal
                if self.roomx == 1 and self.roomy == 1: #--------------------------------------------------------
                    if self.player.y < TILESIZE*4:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.signtext4) #Top sign
                    else:
                        if self.player.x > TILESIZE*7:
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.signtext2) #Right sign
                        else:
                            inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.signtext3) #Left sign
                if self.roomx == 2 and self.roomy == 0: #--------------------------------------------------------
                    if self.player.x < TILESIZE*7:
                        inspect("textbox", x, x, "manual", BLACK, "---", BLACK, self.objecttext5) #Server
                    else:
                        if self.item_collected[0] == False:
                            self.qicon_show = True
                        if self.action and not self.item_collected[0] and self.player.x > TILESIZE*7:
                            self.item_collected[0] = True
                            self.screwdriver.remove = True
                            inspect("textbox", x, "increment_phase", "manual", BLACK, "---", BLACK, self.itemtext1) #Screwdriver
                if self.roomx == 2 and self.roomy == 1: #--------------------------------------------------------
                    inspect("yesnotextbox", x, x, "manual", BLACK, "Machine", BLACK, self.yesnotext1)

        #Looped Room Events:
        if x == 0 and y == 0: #--------------------------------------------------------
            if self.phase == 0:
                if self.timer(2000):
                    self.phase = 1
            if self.phase == 1:
                #Textbox appears explaining controls
                self.setup_textbox("auto", BLACK, "???", BLACK, self.gametext1)
                self.phase += 1
        if x == 0 and y == 1:#---------------------------------------------------------
            pass
        
    def pause_ui(self, command):
        if command == "on":
            self.ispaused = True
            self.pause_arrow_show = True
            self.pause_items_show = False
            self.movelock = True
            self.show_pause_ui = True
            self.pause_arrow_x, self.pause_arrow_y = self.pause_arrow_defaultx, self.pause_arrow_defaulty #Default pause arrow position
            self.pause_arrow_item = "resume"
        elif command == "off":
            self.ispaused = False
            self.pause_arrow_show = False
            self.movelock = False
            self.show_pause_ui = False
            self.pause_arrow_x, self.pause_arrow_y = TILESIZE*-1, TILESIZE*-1 #Default pause arrow position

    def gameloop(self): #Main loop that will run while running program
        
        def events(): #Controls all boolean inputs
            for event in pg.event.get(): ####################FIX THIS BY SETTING A VARIABLE FOR ALL KEY/CONTROLLER INPUTS THEN MERGING REPEATING CODE BLOCKS##############################################################
                if event.type == pg.QUIT: #Quit game if X of window pressed
                    self.running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE: #Quit game if esc key pressed
                        self.running = False
                        pg.quit()
                        sys.exit()
                   
                    if event.key == pg.K_o: #If event key pressed, toggle action variable on
                        self.action = True
                    
                    if event.key == pg.K_p:
                        if not self.player.shooting and not self.movelock and self.item_collected[2]: #If not already shooting, not movement locked and item 3 (gun) owned:
                            self.player.shooting = True

                    if event.key == pg.K_q: 
                        if not self.ispaused and not self.pauselock: #If not paused and pause is permitted:
                            self.pause_ui("on") #Pause game

                    if self.ispaused: #If paused:
                        if event.key == pg.K_w: 
                            if self.pause_arrow_y >= self.pause_arrow_defaulty + TILESIZE*0.75: #Move arrow up and down within limits
                                self.pause_arrow_y -= TILESIZE*0.75
                        if event.key == pg.K_s:
                            if self.pause_arrow_y <= self.pause_arrow_defaulty + TILESIZE*0.75:
                                self.pause_arrow_y += TILESIZE*0.75

                    if self.yesno:
                        if event.key == pg.K_a or self.controller_right: 
                            if self.pause_arrow_x >= TILESIZE*8.7: #Move arrow up and down within limits
                                self.pause_arrow_x -= TILESIZE*1.7
                                self.pause_arrow_item = "yes"
                        if event.key == pg.K_d or self.controller_left:
                            if self.pause_arrow_x <= TILESIZE*8.4:
                                self.pause_arrow_x += TILESIZE*1.7
                                self.pause_arrow_item = "no"
                    
                    ####################################### TEMP DEV CODE
                    if event.key == pg.K_1:
                        if self.screenfill_show:
                            self.screenfill_show = False
                        else:
                            self.screenfill_show = True
                    if event.key == pg.K_2:
                        if self.gameinfotext_show:
                            self.gameinfotext_show = False
                        else:
                            self.gameinfotext_show = True
                    if event.key == pg.K_3:
                        if self.interacttiles_show:
                            self.interacttiles_show = False
                        else:
                            self.interacttiles_show = True
                    if event.key == pg.K_4:
                        if self.grid_show:
                            self.grid_show = False
                        else:
                            self.grid_show = True
                    
                    if event.key == pg.K_n:
                        self.player.newhealth = self.player.health - 3
                        self.player.dhealth = -0.01
                    ########################################

                if event.type == pg.JOYAXISMOTION: #Joystick input
                    if event.axis == 0: #Horizontal
                        if abs(event.value) >= 0.4: #Allow for joystick deadzone
                            if event.value > 0:
                                self.controller_right = True
                            else:
                                self.controller_left = True
                        else:
                            self.controller_right = False
                            self.controller_left = False
                    if event.axis == 1: #Vertical
                        if abs(event.value) >= 0.4:
                            if event.value > 0:
                                self.controller_down = True
                            else:
                                self.controller_up = True
                        else:
                            self.controller_down = False
                            self.controller_up = False
 
                if event.type == pg.JOYBUTTONDOWN: #Controller  button input
                    if event.button == 0: #A Button
                        self.action = True
                    if event.button == 2: #X Button
                        if not self.player.shooting and not self.movelock and self.item_collected[2]: #If not already shooting, not movement locked and item 3 (gun) owned:
                            self.player.shooting = True
                   
            if self.action:
                self.current_page += 1
                if not self.yesno:
                    if self.gamemode == "MENU":
                        self.gamemode = "GAME"
                    if self.pause_arrow_item == "resume":
                        self.pause_ui("off")
                    if self.pause_arrow_item == "save":
                        self.save_gamedata()
                    if self.pause_arrow_item == "items":
                        self.pause_items_show = True
    
            if self.yesno:
                if self.controller_left: 
                    if self.pause_arrow_x >= TILESIZE*8.7: #Move arrow up and down within limits
                        self.pause_arrow_x -= TILESIZE*1.7
                        self.pause_arrow_item = "yes"
                if self.controller_right:
                    if self.pause_arrow_x <= TILESIZE*8.4:
                        self.pause_arrow_x += TILESIZE*1.7
                        self.pause_arrow_item = "no"

        def draw_all(): #Draws all components onto the screen    
            #Draw sprites
            self.floor_sg.draw(self.screen)
            self.bgdeco_sg.draw(self.screen)
            self.enemy_sg.draw(self.screen)
            self.player_sg.draw(self.screen)
            self.wall_sg.draw(self.screen)
            self.fgdeco_sg.draw(self.screen)

            #Draw items
            self.item_sg.draw(self.screen)

            #Draw textbox
            if self.showtextbox == True:
                self.draw_textbox()
    
            ############################################################################################################################
            #Draw interact tiles (TEMP)
            if self.interacttiles_show:
                self.interacttile_sg.draw(self.screen)
            
            #Draw grid (TEMP)
            if self.grid_show:
                for i in range (0, WIDTH, TILESIZE):
                    pg.draw.line(self.screen,(RED), (i,0), (i,HEIGHT))
                for i in range (0, HEIGHT, TILESIZE):
                    pg.draw.line(self.screen,(RED), (0,i), (WIDTH,i))
            
            #Fill screen (TEMP)
            if self.screenfill_show:
                self.screen.fill(BLACK)
            
            #Draw player pos text (TEMP)
            #Show player pos TEMP
            a1 = ("PLAYER ["+str(self.player.x)+"]["+str(self.player.y)+"]["+str(int(self.player.x/TILESIZE))+"]["+str(int(self.player.y/TILESIZE))+"]")
            a2 = self.font25.render(a1, True, (WHITE))
            b1 = ("ROOM ["+str(self.roomx)+"]["+str(self.roomy)+"] PHASE ["+str(self.phase)+"]")
            b2 = self.font25.render(b1, True, (WHITE))
            c1 = ("DOOR "+str(self.toggledoor_status))
            c2 = self.font15.render(c1, True, (WHITE))
            d1 = ("Switch "+str(self.switch_status))
            d2 = self.font15.render(d1, True, (WHITE))

            
            if self.gameinfotext_show:
                self.screen.blit(a2,(TILESIZE*1, TILESIZE*1))
                self.screen.blit(b2,(TILESIZE*1, TILESIZE*1.5))
                self.screen.blit(c2,(TILESIZE*1, TILESIZE*2))
                self.screen.blit(d2,(TILESIZE*1, TILESIZE*2.3))
            ############################################################################################################################

            #Border
            self.border_sg.draw(self.screen)

            #Border edge lines
            pg.draw.line(self.screen, self.border_colour, (TILESIZE,TILESIZE), (TILESIZE,HEIGHT-TILESIZE))
            pg.draw.line(self.screen, self.border_colour, (TILESIZE,HEIGHT-TILESIZE), (WIDTH-TILESIZE,HEIGHT-TILESIZE))
            pg.draw.line(self.screen, self.border_colour, (WIDTH-TILESIZE,TILESIZE), (WIDTH-TILESIZE,HEIGHT-TILESIZE))
            pg.draw.line(self.screen, self.border_colour, (TILESIZE,TILESIZE), (WIDTH-TILESIZE, TILESIZE))

            #Hpbar
            self.screen.blit(self.hpbar_border_image, (TILESIZE - 2, TILESIZE/2 - 7)) #Hpbar border
            self.screen.blit(self.hpbar.surface,(self.hpbar.x, self.hpbar.y)) #Hpbar surface

            #Extra top left border tile
            self.screen.blit(self.border_image, (0, 0))

            #Coin count
            coins = ("[$"+ str(self.player.coins) + "]")
            coins_surface = self.font25.render(coins, True, (RED))
            self.screen.blit(coins_surface,(TILESIZE*7.5, TILESIZE*0.2))

            #Query icon
            if self.qicon_show == True:
                self.screen.blit(self.qicon,(self.qiconx,self.qicony))

            #Pause UI
            if self.show_pause_ui == True:
                pause_ui_text1 = self.font25.render("MENU", True, (BLACK))
                pause_ui_text2 = self.font25.render("   Resume", True, (BLACK))
                pause_ui_text3 = self.font25.render("   Save", True, (BLACK))
                pause_ui_text4 = self.font25.render("   Items", True, (BLACK))

                #pause_ui_text5 = self.font25.render("   Time played: " + str(int(self.current_time/600)), True, (BLACK))
                #self.screen.blit(pause_ui_text5, (TILESIZE*3, TILESIZE*6.6))

                self.screen.blit(self.pause_ui_bg_img, (TILESIZE*2, TILESIZE*2))
                self.screen.blit(pause_ui_text1, (TILESIZE*3, TILESIZE*3))
                self.screen.blit(pause_ui_text2, (TILESIZE*3, TILESIZE*4))
                self.screen.blit(pause_ui_text3, (TILESIZE*3, TILESIZE*4.75))
                self.screen.blit(pause_ui_text4, (TILESIZE*3, TILESIZE*5.5))

                if self.pause_items_show == True:
                    try:
                        for item in range(0,1):
                            if self.item_collected[item]:
                                self.item_images[item].set_colorkey(WHITE)
                                self.screen.blit(self.item_images[item], (TILESIZE*3, TILESIZE*7))
                    except:
                        pass

            if self.pause_arrow_show == True:
                #Draw arrow
                self.screen.blit(self.pause_arrow_img, (self.pause_arrow_x, self.pause_arrow_y))
                  
                #print(self.item_collected, self.pause_items_show)

            #Bullets
            if self.playerbullet.show:
                self.playerbullets_sg.draw(self.screen)
    
        def update(): #Updates screen, player and all objects
            if self.gamemode == "GAME": #Run these methods only if the program is running the game
                self.room_event(self.roomx,self.roomy)
                self.all_sg.update() #Run every sprite's update function
                self.ui_update()
                self.hpbar.update() #Update Hp bar
                self.playerbullets_sg.update()
                
            #Run this regardless of gamemode
            self.clock.tick(FPS) 
            pg.display.update()
        
        while self.running == True: #GAME LOOP---------------------------------------------------------------------------------------
            events()
            update()

            if self.gamemode == "MENU": #If in mode: Menu
                self.main_menu()
                
            elif self.gamemode == "GAME": #If in mode: Game
                #Methods to call continuously:
                draw_all() 

                #Time in frames of the game
                self.current_time = pg.time.get_ticks()
                self.timepassed = self.current_time - self.timepoint

                self.cooldown1 += 1

                #Set action status to false by default
                if self.action == True:
                    self.action = False
                
                #print(self.button_status)
                #print(self.current_time,self.timepoint,self.timepassed,self.timelock,self.action)
                #print("wall count ",len(self.wall_sg)," ","all count ",len(self.all_sg)," ","deco count ",len(self.bgdeco_sg)," ", "floor count ",len(self.floor_sg))

    def main_menu(self):
        self.image = self.menubg_animate[int(self.current_image)]
        self.screen.blit(self.image, (0,0))
        self.current_image += 0.05
        if self.current_image >= len(self.menubg_animate):
            self.current_image = 0

    def music(self):
        #Play background music
        if not self.is_playing_music:
            self.is_playing_music = True
            mixer.music.load("bg1.wav") 
            mixer.music.set_volume(0.1)
            mixer.music.play(-1)

class Player(pg.sprite.Sprite): #The player object
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Gives a copy of the game to this class
        self.rect = pg.Rect(0, 0, TILESIZE-2, TILESIZE-2) #-8 old 
        self.rect.x = x #Hitbox x pos
        self.rect.y = y #Hitbox y pos
        self.x = x #Player x pos
        self.y = y #Player y pos
        self.dy = 0 #Current yspeed
        self.dx = 0 #Current xspeed 
        self.speed = 2 #Speed increment ######################################## normally 2
        self.direction = "down" #Will change indicating axis of movement 
        self.uplock, self.rightlock, self.downlock, self.leftlock = False, False, False, False #Direction locks to fix screen swap wall clips
        
        self.health = 5 #How much current health the player has
        self.maxhealth = 5 #Maximum possible health the player can have
        self.dhealth = 0 #Refers to the change in health (speed at which health will change)
        self.newhealth = 0 #Refers to the new amount of health the player will have after a change
        self.immunity = 0 #Frames where damage will not be taken
        
        self.shooting = False
        self.damage = 1

        self.coins = 0
        
        self.current_image = 0 #Will be used to time animations
        self.image = self.game.p_d_animate[1] #Start with player frame (down2)
        self.image.set_colorkey(WHITE) #Define transparent background colour of png image

        #Add to sprite groups
        self.game.all_sg.add(self)
        self.game.player_sg.add(self)

        #Create a bullet for the player
        #self.bullet = Bullet(self.game)

    def check_collision(self, axis):
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
        
        elif self.x < TILESIZE - 5:
            self.uplock, self.rightlock, self.downlock, self.leftlock = True, False, True, False
            if self.x < 5: #If offscreen left:
                self.game.roomx -= 1
                self.game.new_room(self.game.roomx, self.game.roomy) #New room with y coordinate +1
                self.x = WIDTH - TILESIZE - 6 #Mirror player position on opposite edge of screen
        else:
            self.uplock, self.rightlock, self.downlock, self.leftlock = False, False, False, False 

    def animate(self, direction):
        if not self.shooting: #If moving while not shooting
            self.current_image += 0.1 #Constantly increment this count
            if self.current_image >= len(self.game.p_u_animate): #If count surpasses length of image array
                self.current_image = 0 #Reset count to 0 which loops the animation from the start
            if direction == "up":
                self.image = self.game.p_u_animate[int(self.current_image)] #Set image to the (integer value of the current image count) index of the 
            if direction == "down":                                         #player animation image arrays, in this case its the "up" array consisting of 4 up movement frames
                self.image = self.game.p_d_animate[int(self.current_image)]
            if direction == "left":
                self.image = self.game.p_l_animate[int(self.current_image)]
            if direction == "right":
                self.image = self.game.p_r_animate[int(self.current_image)]
            #Defines transparent bg colour for player image
            self.image.set_colorkey(WHITE)
        
    def basic_movement(self):
        keys = pg.key.get_pressed()

        ############################################ TEMP CODE 
        if keys[pg.K_z]:
            self.health -= 0.1
        if keys[pg.K_x]:
            self.health += 0.1
        if keys[pg.K_c]:
            if self.maxhealth > 0.1:
                self.maxhealth -= 0.1
        if keys[pg.K_v]:
            self.maxhealth += 0.1
        ############################################

        #Basic movement
        self.dy, self.dx = 0, 0 #Current x and y speed change = 0 by default
        if self.game.movelock == False:
            if keys[pg.K_w] or self.game.controller_up: #UP
                if self.uplock == False:
                    self.dy = -self.speed #Set delta y to - player speed 
                    self.animate("up")
            if keys[pg.K_a] or self.game.controller_left: #LEFT
                if self.leftlock == False:
                    self.dx = -self.speed #Set delta x to - player speed
                    self.animate("left")
            if keys[pg.K_s] or self.game.controller_down: #DOWN
                if self.downlock == False:
                    self.dy = self.speed #Set delta y to  player speed 
                    self.animate("down")
            if keys[pg.K_d] or self.game.controller_right: #RIGHT
                if self.rightlock == False:
                    self.dx = self.speed #Set delta x to  player speed
                    self.animate("right")
            
            #Direction determination
            if self.dy < 0: #If moving up:
                if self.dx == 0:
                    self.direction = "up"
                elif self.dx < 0:
                    self.direction = "upleft"
                elif self.dx > 0:
                    self.direction = "upright"
            elif self.dy > 0: #If moving down:
                if self.dx == 0:
                    self.direction = "down"
                elif self.dx < 0:
                    self.direction = "downleft"
                elif self.dx > 0:
                    self.direction = "downright"
            elif self.dx < 0: #If moving right:
                self.direction = "left"
            elif self.dx > 0:
                self.direction = "right"
        
        #Player image while shooting
        if self.shooting:
            if self.game.playerbullet.direction == "up":
                self.image = self.game.p_shooting_images[0]
            elif self.game.playerbullet.direction == "down":
                self.image = self.game.p_shooting_images[1]
            elif self.game.playerbullet.direction == "left" or self.game.playerbullet.direction == "upleft" or self.game.playerbullet.direction == "downleft":
                self.image = self.game.p_shooting_images[2]
            elif self.game.playerbullet.direction == "right" or self.game.playerbullet.direction == "upright" or self.game.playerbullet.direction == "downright":
                self.image = self.game.p_shooting_images[3]
            self.image.set_colorkey(WHITE)
        else:
            if self.dx == 0 and self.dy == 0: #If stationary
                if self.direction == "up":
                    self.image = self.game.p_u_animate[1] #Set image to player looking down (neutral look)
                elif self.direction == "down":
                    self.image = self.game.p_d_animate[1]
                elif self.direction == "left":
                    self.image = self.game.p_l_animate[0]
                elif self.direction == "right":
                    self.image = self.game.p_r_animate[0]
                self.image.set_colorkey(WHITE)

        self.x += self.dx #Change player x position by delta x per frame
        self.y += self.dy #Change player y position by delta y per frame
    
    def update_health(self):
        #Player health should never be greater than their max health
        if self.game.player.health > self.maxhealth:
            self.health = self.maxhealth
        
        #Change health 
        if self.dhealth != 0: #If change in health is positive:
            if int(self.health) + 1 != int(self.newhealth): #If current health not equal to new health: (ints to truncate decimals and +1 used to avoid a rounding error)
                self.health += self.dhealth #Add change in health to current health
            else:
                self.dhealth = 0
        
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
        
        #Update health
        self.update_health()
        
        #print(self.uplock, self.rightlock, self.downlock, self.leftlock)

class Hpbar(pg.sprite.Sprite): #The red hp bar in the top left
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.colour = (200,0,0) #Slightly dark red
        self.surface = pg.Surface((TILESIZE*6, 5))
        self.surface.fill(self.colour)
        self.x, self.y = TILESIZE, TILESIZE/2 - self.surface.get_height()
       
    def update(self):
        #xpos of hp bar is the origin point plus the width of the hp bar divided by the maxhealth * current player health
        self.x = (TILESIZE - self.surface.get_width()) + ((self.surface.get_width()/self.game.player.maxhealth)*self.game.player.health)
        #Never exceed max x position
        if self.x > TILESIZE:
            self.x = TILESIZE
        
        #Change colour
        self.surface.fill(self.colour)
        if self.game.player.dhealth < 0:
            self.colour = (150,0,0) #Darker red
        elif self.game.player.dhealth > 0:
            self.colour = (250,0,0)
        else:
            self.colour = (200,0,0)



        #print(round(self.game.player.health, 1), "      ", round(self.game.player.maxhealth, 1), "       ", round(self.game.player.dhealth, 1), "      ", round(self.game.player.newhealth, 1))

class Door(pg.sprite.Sprite): #Two state door object 
    def __init__(self, game, type, roomx, roomy, id, closedimageid, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game to this class
        self.type = type
        self.id = id #Used to identify which specific door this is
        if self.type == "toggle":
            self.status_array = self.game.toggledoor_status
        elif self.type == "key":
            self.status_array = self.game.keydoor_status

        self.game.all_sg.add(self) #Add self to all sprites group
        self.game.bgdeco_sg.add(self) #Add self to all sprites group
        
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x,y
        self.openimageid, self.closedimageid = 0, closedimageid #Open doors have the same door image id = 0

        self.image = pg.image.load(self.game.door_images[0]) #Set default image to open (Stops door flashing glitch when entering new room)

        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.rect.topleft = (x,y)

    def update(self): 
        if self.type == "toggle": #If door type is toggle - manipulated by switch presses
                #Take positive value of id
            if not self.game.switch_status[abs(self.id)]: #If switch not pressed:
                self.game.toggledoor_status[self.id] = False #Door with matching id as button is set to false or closed
                self.game.toggledoor_status[-1*self.id] = True #Door with matching negative type id as button is set to true or open
            else: #If switch pressed:
                self.game.toggledoor_status[self.id] = True 
                self.game.toggledoor_status[-1*self.id] = False 

        if self.status_array[abs(self.id)] == False: #If door closed:
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

        #print(len(self.game.bgdeco_sg))
        #print(self.game.door_status)
        #print(self.game.roomx,self.game.roomy,self.roomx,self.roomy)

    def switch(self):
        if self.game.toggledoor_status[abs(self.id)] == True: #If door is closed:
            self.game.toggledoor_status[abs(self.id)] = False
        else: #If door is open:
            self.game.toggledoor_status[abs(self.id)] = True

class Switch(pg.sprite.Sprite): #Two state switch object
    def __init__(self, game, roomx, roomy, id, closedimageid, openimageid, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.game.bgdeco_sg.add(self)
        self.game.all_sg.add(self)
        self.game.switch_sg.add(self)

        self.closedimageid, self.openimageid = closedimageid, openimageid #The id of the graphics for the open and closed door
        self.image = pg.image.load(self.game.switch_images[self.closedimageid])
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #self.rect.x, self.rect.y = x, y
        
        self.roomx, self.roomy = roomx, roomy
        self.id = id #Used to identify which specific switch this is
    
    def update(self):
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the switch's chunk doesnt match player chunk:
            self.game.bgdeco_sg.remove(self)
            self.game.all_sg.remove(self)
            self.game.switch_sg.remove(self)

        if self.game.switch_status[self.id] == True: #If switch pressed:
            self.image = pg.image.load(self.game.switch_images[self.closedimageid])
            self.image.set_colorkey(WHITE)
        else: #If switch unpressed:
            self.image = pg.image.load(self.game.switch_images[self.openimageid])
            self.image.set_colorkey(WHITE)
        
    def switch(self):
        if self.game.switch_status[self.id]: #If switch is pressed:
            self.game.switch_status[self.id] = False
        else: #If switch is unpressed:
            self.game.switch_status[self.id] = True

class Tile(pg.sprite.Sprite): #Square graphics that make up the game
    def __init__(self, game, type, roomx, roomy, x ,y, image, folderid, frameA, frameB, animationspeed, colourkey):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game class
        self.type = type
        self.x, self.y = x, y #Initialise x and y positions
        self.image = image
        self.colourkey = colourkey

        #STATIC TILE
        if self.type == "static":
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.image.set_colorkey(self.colourkey)
        
        #INTERACT TILE
        elif self.type == "interactdown":
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y - 1)
        elif self.type == "interactleft":
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x + 1, self.y)
        elif self.type == "interactup":
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y + 1)
        elif self.type == "interactright":
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x - 1, self.y)

        #ANIMATED TILE
        elif self.type == "animatedwall" or self.type == "animatedfloor": 
            self.roomx, self.roomy = roomx, roomy #Set the local room position
            self.colourkey = colourkey 
            self.game.all_sg.add(self) #Add self to all sprites group
            self.image = pg.image.load("ATiles/folder" + str(folderid) + "/Atile0.png") #Default image
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.image.set_colorkey(self.colourkey)
            self.current_image = 0
            self.setup_animation(folderid,frameA,frameB)
            self.animation_speed = animationspeed
            if self.type == "animatedwall":
                self.game.wall_sg.add(self) #Add self to wall sprite group
            else:
                self.game.floor_sg.add(self) #Add self to floor sprite group

    def setup_animation(self, folderid, frameA, frameB):
        self.image_animation = [] #Array to store all frames of animation
        for i in range(frameA, frameB+1): #From frameA to frameB (Indicates which animated tiles to load)
            #Add this image to the array: image with file path that matches this below:
            self.image_animation.append(pg.image.load("ATiles/folder" + str(folderid) + "/Atile"+ str(i) +".png"))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.type == "animatedwall" or self.type == "animatedfloor":
            if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If the Atile's chunk doesnt match player chunk:
                self.game.wall_sg.remove(self)
                self.game.floor_sg.remove(self)
                self.game.fgdeco_sg.remove(self)
                self.game.bgdeco_sg.remove(self)
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
        self.immunity = 0 #Timer for how long the enemy will be invisible for after being hit
        self.knockback_timer = 0 #Timer for how long the enemy will be knocked back after being hit
        self.death_timer = 0 #Timer for how long to show corpse of enemy on screen for after killed
        self.dead = False #Is dead?

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
    
    def init_type(self, type): #Initialisation specific to the type of enemy
        if type == "slime":
            self.health = 3
            self.default_image = self.game.slime_move_images[0] 
            self.hit_image = self.game.slime_hit_image
            self.image_array = self.game.slime_move_images
            
    def animate(self): #Animation
        if self.immunity > 0:
            self.current_image += self.animation_speed
            if self.current_image >= len(self.image_array):
                self.current_image = 0
            self.image = pg.image.load(self.image_array[int(self.current_image)])
        else:
            self.image = pg.image.load(self.game.slime_hit_image)
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
        self.immunity += 1 
        self.knockback_timer += 1
        self.death_timer += 1

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

        if not self.dead: #If enemy is alive
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
        
        #Bullet collision:
        #if (self.x < self.game.player.x or self.x > self.game.player.x + TILESIZE) and (self.y < self.game.player.y or self.y > self.game.player.y + TILESIZE):
        if pg.sprite.spritecollide(self, self.game.playerbullets_sg, False): #If colliding with the player's bullet
            if self.immunity >= 0: 
                self.immunity = -20 #Create a 20 frame immunity window
                self.knockback_timer = -10 #Create a 20 frame knockback window
                self.health -= self.game.player.damage #Enemy health decreases by the damage dealt by the player
        
        if self.knockback_timer < 0:
            if self.knockback_direction == "up":
                self.dx, self.dy = 0, -2     
            if self.knockback_direction == "down":
                self.dx, self.dy = 0, 2
            if self.knockback_direction == "left":
                self.dx, self.dy = -2, 0
            if self.knockback_direction == "right":
                self.dx, self.dy = 2, 0
            if self.knockback_direction == "upright":
                self.dx, self.dy = 2, -2
            if self.knockback_direction == "upleft":
                self.dx, self.dy = -2, -2
            if self.knockback_direction == "downright":
                self.dx, self.dy = 2, 2
            if self.knockback_direction == "downleft":
                self.dx, self.dy = -2, 2
        else:
            self.knockback_direction = self.game.playerbullet.direction

        #If health less than 0, call death method
        if self.health <= 0:
            self.dead = True
            self.image = pg.image.load(self.game.slime_death_image)
            self.image.set_colorkey(WHITE)
            if self.death_timer > 1: #Set death timer to a negative number just once
                self.death_timer = -255
            
            if self.death_timer < 0: #If enemy is dead and corpse showing:
                self.image.set_alpha(-self.death_timer) #Fade the corpse out until invisible

            if self.death_timer > 0: #When death timer surpassed (becomes positive):
                self.game.all_sg.remove(self) #Remove from following sprite groups:
                self.game.enemy_sg.remove(self)
        
        #print(self.health, self.game.player.damage, self.immunity, self.death_timer, self.game.playerbullet.direction)
        #print(self.x < self.game.player.x or self.x > self.game.player.x + TILESIZE) and (self.y < self.game.player.y or self.y > self.game.player.y + TILESIZE)
                
class Item(pg.sprite.Sprite): #All items on screen
    def __init__(self, game, id, roomx, roomy, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.id = id
        self.x, self.y = x, y
        self.roomx, self.roomy = roomx, roomy
        self.remove = False
        self.show = True
        self.game.item_sg.add(self)
        self.game.all_sg.add(self)

        if self.id == 0:
            self.image = pg.image.load("Items/ingame/screwdriver.png")
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.collected = False

    def update(self):
        #Check if offscreen
        if ((self.roomx != self.game.roomx) or (self.roomy != self.game.roomy) or self.game.item_collected[0] == True): #If current room x and y not equal to the sprite's local room x and y or remove variable is trues:
            self.game.item_sg.remove(self) #Remove from item sprite group
            self.game.all_sg.remove(self) #Remove from all sprtie group
        
        self.rect.x, self.rect.y = self.x, self.y
        if self.show == True:
            self.game.all_sg.add(self)
        else:
            self.game.all_sg.remove(self)

    def present(self): #Present item
        self.hide = True

class Npc(pg.sprite.Sprite): #Non player characters
    def __init__(self, game, type, phase, roomx, roomy, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game structure class to this object
        self.type = type
        self.phase = phase #Refers to the sequence the npc is currently in
        self.roomx, self.roomy = roomx, roomy
        self.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
        self.x, self.y = x, y
        self.rect.x, self.rect.y = self.x, self.y
        self.dx, self.dy = 0, 0
        self.direction = "up"

        self.current_image = 0 #Will be used to time animations
        self.image = self.game.npc1_u_animate[1] #Start with up frame
        self.image.set_colorkey(WHITE) #Define transparent background colour of png image
        
        self.game.wall_sg.add(self)
        self.game.all_sg.add(self)

        if self.type == "janitor":
            self.direction = "up"

    def animate(self, direction):
        self.current_image += 0.1
        if self.current_image >= len(self.game.p_u_animate):
            self.current_image = 0
        if direction == "up":
            self.image = self.game.npc1_u_animate[int(self.current_image)]
        if direction == "down":
            self.image = self.game.npc1_d_animate[int(self.current_image)]
        if direction == "left":
            self.image = self.game.npc1_l_animate[int(self.current_image)]
        if direction == "right":
            self.image = self.game.npc1_r_animate[int(self.current_image)]
        self.image.set_colorkey(WHITE)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x, self.rect.y = self.x, self.y
        if self.direction != "x":
            self.animate(self.direction)
        if self.dx > 0:
            self.direction = "right"
        if self.dx < 0:
            self.direction = "left"
        if self.dy > 0:
            self.direction = "down"
        if self.dy < 0:
            self.direction = "up"
        if self.dx == 0 and self.dy == 0:
            self.direction = "x"
        if (self.roomx != self.game.roomx) or (self.roomy != self.game.roomy): #If offscreen:
            self.game.wall_sg.remove(self)     
            self.game.all_sg.remove(self) 

        if self.type == "janitor": #---------------------------------------------------
            if self.phase == 0: 
                if int(self.x/TILESIZE) < 5:
                    if self.game.phase == 3: #If screwdriver given
                        self.game.movelock = True
                        self.dx = 2 #Move right
                elif self.y < HEIGHT:
                    self.game.keydoor_status[0] = True                 
                    self.dx, self.dy = 0, 2 #Move down
                else:
                    self.dx, self.dy = 0,0
                    self.phase += 1
                    self.game.movelock = False
            
            if self.phase == 2: #When caused to move after gun obtained
                if int(self.x/TILESIZE) < 11:
                    self.game.movelock = True
                    self.dx = 1 #Move right
                else:
                    self.dx = 0
                    self.direction = "up"
                    self.image = self.game.npc1_u_animate[2] #Look upwards
                    self.image.set_colorkey(WHITE)
                    self.game.movelock = False                
                    self.phase += 1
            
            if self.phase == 3:
                pass
                
        #print(self.dx, self.x, self.direction, int(self.x/TILESIZE), self.phase)

class Bullet(pg.sprite.Sprite): #Bullet 
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("Player/PlayerBullets/bullet1.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0
        self.rect.x, self.y = 0, 0
        self.speed = 5
        self.direction = ""
        self.show = True

        self.game.playerbullets_sg.add(self)
    
    def check_collision(self): #Checks if the bullet has hit anything or offscreen
        if self.game.player.shooting:
            if pg.sprite.spritecollide(self, self.game.wall_sg, False):
                self.game.player.shooting = False
            if self.x > WIDTH - TILESIZE*1.2 or self.x < TILESIZE*1.2 or self.y > HEIGHT - TILESIZE*1.2 or self.y < TILESIZE*1.2:
                self.game.player.shooting = False
            if pg.sprite.spritecollide(self, self.game.enemy_sg, False):
                self.game.player.shooting = False
        
    def update(self):
        self.x += self.dx #Increment x by the x change
        self.y += self.dy #Increment y by the y change
        self.rect.x, self.rect.y = self.x, self.y #Set the collider box equal to the x and y pos

        if self.game.player.shooting: #If bullet has been fired
            self.show = True #Show bullet
            self.dx, self.dy = 0, 0 #By default bullet isnt moving
            #Movement of bullet in 8 directions depending on player's direction
            if self.direction == "up":
                self.dy = -self.speed
            if self.direction == "down":
                self.dy = self.speed
            if self.direction == "left":
                self.dx = -self.speed
            if self.direction == "right":
                self.dx = self.speed
            if self.direction == "upright":
                self.dx = self.speed
                self.dy = -self.speed
            if self.direction == "upleft":
                self.dx = -self.speed
                self.dy = -self.speed
            if self.direction == "downright":
                self.dx = self.speed
                self.dy = self.speed
            if self.direction == "downleft":
                self.dx = -self.speed
                self.dy = self.speed
            
            self.check_collision()
            
        else: #If bullet has not been fired
            self.show = False #Hide bullet
            self.x, self.y = self.game.player.x + TILESIZE/2, self.game.player.y + TILESIZE/2 #Set position to the middle of the player
            self.direction = self.game.player.direction #Check the direction that the player is facing in
        
        #print(self.game.player.shooting, self.dx, self.dy)
        #print(self.game.player.direction)

#CONSTANTS:
FPS = 60
TILESIZE = 32
#Screen size (16x13 Tiles, 512x416 Pixels)
WIDTH = TILESIZE*16  
HEIGHT = TILESIZE*13 
#Colours (R,G,B)
BLACK =  (0,0,0)
WHITE =  (255,255,255)
GREY  =  (100,100,100)
RED   =  (255,0,0)
GREEN =  (0,255,0)
BLUE  =  (0,0,255)

gui = GUI() 

#ERROR CHECKING: Button() is a class of tkinter but it is also a class i have defined in my program which is why it crashes when i try running the
#program since the lines that instantiate Button() get mixed up. Had to go change my Button() class to Switch().