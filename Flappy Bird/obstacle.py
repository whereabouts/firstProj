from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock

class Obstacle(Widget):
    # attr
    GAP_SIZE = NumericProperty(100)
    CAP_SIZE = NumericProperty(15)
    obstacle_center = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)
    # Texture
    upper_obstacle_body_texture = ObjectProperty(None)
    lower_obstacle_body_texture = ObjectProperty(None)
    lower_obstacle_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_obstacle_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upper_obstacle_body_texture = Image(source="assets/vine_body.png").texture
        self.upper_obstacle_body_texture.wrap = 'repeat'
        self.lower_obstacle_body_texture = Image(source="assets/log_body.png").texture
        self.lower_obstacle_body_texture.wrap = 'repeat'

    def on_size(self, *args):
        lower_body_size = self.bottom_cap_position - self.bottom_body_position
        self.lower_obstacle_tex_coords[5] =lower_body_size/20.
        self.lower_obstacle_tex_coords[7] =lower_body_size/20.

        top_body_size = self.top - self.top_body_position
        self.top_obstacle_tex_coords[5] = top_body_size/20.
        self.top_obstacle_tex_coords[7] = top_body_size/20.

    def on_obstacle_center(self, *args):
        Clock.schedule_once(self.on_size, 0)