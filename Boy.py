from pico2d import load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_a
from transitions import Machine

GROUND_Y = 90
FRAME_COUNT = 8
RUN_SPEED = 5


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


class Run:
    @staticmethod
    def enter(boy):
        boy.face_dir = boy.dir
        boy.action = 1 if boy.face_dir == 1 else 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.face_dir = boy.dir
        boy.action = 1 if boy.face_dir == 1 else 0
        boy.frame = (boy.frame + 1) % FRAME_COUNT
        boy.x = clamp(50, boy.x + boy.dir * RUN_SPEED, 750)

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, GROUND_Y)


class AutoRun:
    @staticmethod
    def enter(boy):
        boy.auto_dir = boy.face_dir
        boy.action = 1 if boy.auto_dir == 1 else 0

    @staticmethod
    def exit(boy):
        boy.face_dir = boy.auto_dir

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % FRAME_COUNT
        boy.x += boy.auto_dir * RUN_SPEED
        if boy.x <= 50 or boy.x >= 750:
            boy.x = clamp(50, boy.x, 750)
            boy.auto_dir *= -1
            boy.action = 1 if boy.auto_dir == 1 else 0

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, GROUND_Y)


STATES = {'Idle': Idle, 'Run': Run, 'AutoRun': AutoRun}

TRANSITIONS = [
    {'trigger': 'run', 'source': 'Idle', 'dest': 'Run'},
    {'trigger': 'stop', 'source': 'Run', 'dest': 'Idle'},
    {'trigger': 'auto_run', 'source': ['Idle', 'Run'], 'dest': 'AutoRun'},
]


class Boy:
    def __init__(self):
        self.x = 400
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.auto_dir = 1
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
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.auto_run()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_RIGHT, SDLK_LEFT):
            self.dir += 1 if event.key == SDLK_RIGHT else -1
            if self.dir != 0:
                self.run()
            else:
                self.stop()
        elif event.type == SDL_KEYUP and event.key in (SDLK_RIGHT, SDLK_LEFT):
            self.dir -= 1 if event.key == SDLK_RIGHT else -1
            # 키를 뗀 것으로는 AutoRun이 풀리지 않는다
            if self.dir == 0:
                self.stop()
            elif self.state != 'AutoRun':
                self.run()

    def update(self):
        STATES[self.state].do(self)

    def draw(self):
        STATES[self.state].draw(self)
