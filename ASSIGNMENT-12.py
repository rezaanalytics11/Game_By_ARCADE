

import arcade
import math
import os
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Bullets Enemy Aims Example"
BULLET_SPEED = 4


PARTICLE_GRAVITY = 0.05
PARTICLE_FADE_RATE = 8
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 20
PARTICLE_RADIUS = 3

PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.COQUELICOT,
                   arcade.color.LAVA,
                   arcade.color.KU_CRIMSON,
                   arcade.color.DARK_TANGERINE]
PARTICLE_SPARKLE_CHANCE = 0.02


SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5
SMOKE_CHANCE = 0.25


class Smoke(arcade.SpriteCircle):
    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        if self.alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE


class Particle(arcade.SpriteCircle):
    def __init__(self, my_list):
        color = random.choice(PARTICLE_COLORS)
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture
        self.my_list = my_list

        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        self.my_alpha = 255
        self.my_list = my_list

    def update(self):
        if self.my_alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)


class MyGame(arcade.Window):
  def __init__(self, width, height, title):
     super().__init__(width, height, title)


     file_path = os.path.dirname(os.path.abspath(__file__))
     os.chdir(file_path)

     arcade.set_background_color(arcade.color.BLACK)


     self.mainplayer_list =[]
     self.bullet_list = []
     self.enemy_list = []
     self.coin_list= []
     self.divar_list=[]
     self.explosions_list=[]
     self.player_sprite = None
     self.enemy = None
     self.score = 0



  def setup(self):
       self.mainplayer_list = arcade.SpriteList()
       self.bullet_list = arcade.SpriteList()
       self.enemy_list = arcade.SpriteList()
       self.coin_list = arcade.SpriteList()
       self.smoke_list = arcade.SpriteList()
       self.explosions_list=arcade.SpriteList()
       self.divar_list=arcade.SpriteList()


       self.set_mouse_visible(False)
       self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser2.wav")
       self.hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")


       self.coin = arcade.Sprite(":resources:images/items/star.png", 0.5)
       self.coin.center_y = 50
       self.coin.center_x = 50
       self.coin_list.append(self.coin)

       self.coin = arcade.Sprite(":resources:images/items/star.png", 0.5)
       self.coin.center_y = 50
       self.coin.center_x = 100
       self.coin_list.append(self.coin)

       self.coin = arcade.Sprite(":resources:images/items/star.png",0.5)
       self.coin.center_y = 50
       self.coin.center_x = 150
       self.coin_list.append(self.coin)


       self.divar = arcade.Sprite(":resources:images/tiles/brickBrown.png")
       self.divar.center_x = SCREEN_WIDTH//2
       self.divar.width = SCREEN_WIDTH
       self.divar.height=20
       self.divar.center_y =10
       self.divar_list.append(self.divar)



       self.mainplayer = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
       self.mainplayer.center_x = SCREEN_WIDTH//2
       self.mainplayer.height=40
       self.mainplayer.center_y = 100
       self.mainplayer.angle = 0
       self.mainplayer.speed = 10
       self.mainplayer_list.append(self.mainplayer)
       self.mainplayer.change_angle=self.mainplayer.change_angle * self.mainplayer.speed

  def on_draw(self):


       arcade.start_render()
       self.mainplayer.draw()
       self.bullet_list.draw()
       self.enemy_list.draw()
       self.divar_list.draw()
       self.coin_list.draw()
       self.explosions_list.draw()

       arcade.draw_text(f"Score: {self.score}", SCREEN_WIDTH-150, 30, arcade.color.WHITE, 20)
       arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, arcade.color.WHITE, 28)

  def on_update(self, delta_time):

    for  self.bullet in self.bullet_list:
         self.bullet_list.update()


    odds = 200


    adj_odds = int(odds * (1 / 60) / delta_time)

    if random.randrange(adj_odds) == 0:

        self.enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.enemy.center_y = random.randint(500, SCREEN_HEIGHT)
        self.enemy.center_x = random.randint(100, SCREEN_WIDTH-100)
        self.enemy.angle = 180
        self.enemy.speed = 4
        self.enemy.change_y -= self.enemy.speed
        self.enemy_list.append(self.enemy)

    self.enemy_list.update()

  def on_mouse_press(self, x, y, button, modifiers):
       arcade.sound.play_sound(self.gun_sound)
        # Loop through each enemy that we have
       for mainplayer in self.mainplayer_list:
            start_x = mainplayer.center_x
            start_y = mainplayer.center_y

            dest_x = self.enemy.center_x
            dest_y = self.enemy.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            mainplayer.angle = math.degrees(angle)-90

            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
            bullet.center_x = start_x
            bullet.center_y = start_y

            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            self.bullet_list.append(bullet)

       for bullet in self.bullet_list:
           if bullet.top < 0:
               bullet.remove_from_sprite_lists()

  def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        #self.mainplayer.angle = y
        self.mainplayer.center_x = x
        self.mainplayer.center_y = y

        k=[]
        for self.enemy in self.enemy_list:
            if self.enemy.top < self.divar.center_y:
                k.append(self.enemy)


        print(len(k))

        if len(k)>=5 :
              self.coin.remove_from_sprite_lists()

        for bullet in self.bullet_list:

         hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)


         if len(hit_list) > 0:

                bullet.remove_from_sprite_lists()


         for self.enemy in hit_list:
                for i in range(PARTICLE_COUNT):
                    particle = Particle(self.explosions_list)
                    particle.position = self.enemy.position
                    self.explosions_list.append(particle)

                smoke = Smoke(50)
                smoke.position = self.enemy.position
                self.explosions_list.append(smoke)

                self.enemy.remove_from_sprite_lists()
                self.score += 1

                arcade.sound.play_sound(self.hit_sound)


         if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()




def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()