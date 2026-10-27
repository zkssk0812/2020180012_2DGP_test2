from pico2d import load_image
from transitions import Machine

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


STATES = {'Idle': Idle}

TRANSITIONS = []


class Boy:
    def __init__(self):
        self.x = 400
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=[{'name': name,
                     'on_enter': lambda n=name: STATES[n].enter(self),
                     'on_exit': lambda n=name: STATES[n].exit(self)}
                    for name in STATES],
            transitions=TRANSITIONS,
            initial='Idle',
            ignore_invalid_triggers=True,
        )
        Idle.enter(self)  # 초기 상태는 on_enter가 호출되지 않으므로 직접 호출

    def handle_event(self, event):
        pass

    def update(self):
        STATES[self.state].do(self)

    def draw(self):
        STATES[self.state].draw(self)
