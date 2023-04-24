# Main
from kivy.app import App
# Sub
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
# Add-ons
from obstacle import Obstacle
# RNG
from random import randint

class Background(Widget):
    floor_texture = ObjectProperty(None)
    bgvine_texture = ObjectProperty(None)
    bgtrees_texture = ObjectProperty(None)
    forest_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.floor_texture = Image(source="assets/floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

        self.bgvine_texture = Image(source="assets/bgvine.png").texture
        self.bgvine_texture.wrap = 'repeat'
        self.bgvine_texture.uvsize = (Window.width / self.bgvine_texture.width, -1)

        self.bgtrees_texture = Image(source="assets/bgtrees.png").texture
        self.bgtrees_texture.wrap = 'repeat'
        self.bgtrees_texture.uvsize = (Window.width / self.bgtrees_texture.width, -1)

        self.forest_texture = Image(source="assets/bgtrees.png").texture
        self.forest_texture.wrap = 'repeat'
        self.forest_texture.uvsize = (Window.width / self.forest_texture.width, -1)

    def scroll_textures(self, time_passed):
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0] + time_passed/1.4)%Window.width,
                                    self.floor_texture.uvpos[1])
        self.bgvine_texture.uvpos = ((self.bgvine_texture.uvpos[0] + time_passed/5.0)%Window.width,
                                     self.bgvine_texture.uvpos[1])
        self.bgtrees_texture.uvpos = ((self.bgtrees_texture.uvpos[0] + time_passed/50.0)%Window.width,
                                     self.bgtrees_texture.uvpos[1])
        self.forest_texture.uvpos = ((self.forest_texture.uvpos[0] + time_passed/50.0)%Window.width,
                                     self.forest_texture.uvpos[1])

        texture = self.property('floor_texture')
        texture.dispatch(self)

        texture = self.property('bgvine_texture')
        texture.dispatch(self)

        texture = self.property('bgtrees_texture')
        texture.dispatch(self)
        
        texture = self.property('forest_texture')
        texture.dispatch(self)

class Birdy(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "assets/bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "assets/bird1.png"
        super().on_touch_up(touch)

class MainApp(App):
    title = "Fappy Burd"
    gravity = 400
    obstacles = []
    collided = False

    def starto(self):
        self.root.ids.score.text = "0"
        self.was_collided = False
        self.obstacles = []
        self.frame = Clock.schedule_interval(self.next_frame, 1/60.)
        # obstacles spawn
        num_obstacles = 5
        distance_between_obstacles = Window.width / (num_obstacles - 1)
        for i in range(num_obstacles):
            obstacle = Obstacle()
            obstacle.obstacle_center = randint(96 + 100, self.root.height - 100)
            obstacle.size_hint = (None, None)
            obstacle.pos = (Window.width + i*distance_between_obstacles, 96)
            obstacle.size = (64, self.root.height - 96)

            self.obstacles.append(obstacle)
            self.root.add_widget(obstacle)

    def asobi_owarida(self):
        self.root.ids.birdy.pos = (20, (self.root.height - 96) / 2.0)
        for obstacle in self.obstacles:
            self.root.remove_widget(obstacle)
        self.frame.cancel()
        self.root.ids.starto.disabled = False
        self.root.ids.starto.opacity = 1

    def birdy_movement(self, time_passed):
        birdy = self.root.ids.birdy
        birdy.y = birdy.y + birdy.velocity * time_passed
        birdy.velocity = birdy.velocity - self.gravity * time_passed
        self.collision()

    def next_frame(self, time_passed):
        self.birdy_movement(time_passed)
        self.move_obstacles(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    def move_obstacles(self, time_passed):
        for obstacle in self.obstacles:
            obstacle.x -= time_passed * 100
        # repo obstacles to right
        num_obstacles = 5
        distance_between_obstacles = Window.width / (num_obstacles - 1)
        obstacle_xs = list(map(lambda obstacle: obstacle.x, self.obstacles))
        right_most_x = max(obstacle_xs)
        if right_most_x <= Window.width - distance_between_obstacles:
            most_left_obstacle = self.obstacles[obstacle_xs.index(min(obstacle_xs))]
            most_left_obstacle.x = Window.width

    def collision(self):
        birdy = self.root.ids.birdy
        colliding = False

        for obstacle in self.obstacles:
            if obstacle.collide_widget(birdy):
                colliding = True
                if birdy.y < (obstacle.obstacle_center - obstacle.GAP_SIZE/2.0):
                    self.asobi_owarida()
                if birdy.top > (obstacle.obstacle_center + obstacle.GAP_SIZE/2.0):
                    self.asobi_owarida()
        if birdy.y < 96:
            self.asobi_owarida()
        if birdy.top > Window.height:
            self.asobi_owarida()
        if self.collided and not colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.collided = colliding

if __name__ == "__main__":
    MainApp().run()