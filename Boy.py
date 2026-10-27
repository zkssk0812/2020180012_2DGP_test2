from pico2d import load_image

GROUND_Y = 90


class Boy:
    def __init__(self):
        self.x = 400
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, GROUND_Y)
