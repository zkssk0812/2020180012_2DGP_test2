from pico2d import load_image

GROUND_Y = 90
FRAME_COUNT = 8


class Idle:
    @staticmethod
    def enter(boy):
        boy.action = 3 if boy.face_dir == 1 else 2
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % FRAME_COUNT

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, GROUND_Y)


class Boy:
    def __init__(self):
        self.x = 400
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.cur_state = Idle
        self.cur_state.enter(self)

    def handle_event(self, event):
        pass

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
