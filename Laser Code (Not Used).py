class Laser(pg.sprite.Sprite):
    def __init__(self, game, orientation, height, roomx, roomy, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game #Give a copy of the game structure class to this object
        self.roomx, self.roomy = roomx, roomy
        self.x, self.y = x, y
        self.current_image = 0
        self.animaion_speed = 0.01

        self.setup_animation(orientation, height) 

        self.game.wall_sg.add(self)
        self.game.all_sg.add(self)

    def setup_animation(self, orientation, height):
        if orientation == "horizontal":
            pass
        else: #If vertical:
            if height == 1:
                self.image_array = self.game.laser1_images

    def animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.image_array):
            self.current_image = 0
        self.image = pg.image.load(self.image_array[int(self.current_image)])
        self.image.set_colorkey(WHITE)

    def update(self):
        if self.game.roomx != self.roomx or self.game.roomy != self.roomy:
            self.game.fgdeco_sg.remove(self)
            self.game.all_sg.remove(self)
        
        self.animate()