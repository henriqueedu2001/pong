import random
import math

from sound.sound_engine import SoundEngine

class GameEngine:
    def __init__(self) -> None:
        self.game_state = None
        self.received_game_data = None
        self.user_keys = None
        self.loaded_data = False

        self.ball = Ball()
        self.player_a = Player(x_position=Player.LEFT, y_position=Player.Y_CENTER)
        self.player_b = Player(x_position=Player.RIGHT, y_position=Player.Y_CENTER)

        self.sound_engine = SoundEngine()

        self.colision_detector = ColisionDetector(self.ball, self.player_a, self.player_b, self.sound_engine)

        pass


    def load_data(self, received_game_data, user_keys):
        if received_game_data != None:
            self.received_game_data = received_game_data
            self.user_keys = user_keys
            self.loaded_data = True
        else:
            self.loaded_data = False
            
        return


    def update(self):
        self.ball.update_position()

        if self.loaded_data:
            player_a_y_pos = self.received_game_data['cursor_1']
            player_b_y_pos = self.received_game_data['cursor_2']
            self.player_a.update_position(player_a_y_pos)
            self.player_b.update_position(player_b_y_pos)
            self.colision_detector.detect()
        
        return
    

    def get_game_data(self):
        data = None

        if self.received_game_data:
            data = {
                'ball_x_pos': self.ball.x_pos,
                'ball_y_pos': self.ball.y_pos,
                'ball_x_vel': self.ball.x_vel,
                'ball_y_vel': self.ball.y_vel,
                'player_a_y_pos': self.player_a.y_pos,
                'player_b_y_pos': self.player_b.y_pos,
                'player_a_score': self.player_a.score,
                'player_b_score': self.player_b.score,
            }

        return data
    

    def print_game_data(self):
        data = self.get_game_data()
        if data:
            print(f'{data['ball_x_vel']: .2f} {data['ball_y_vel']: .2f}')


class Ball:
    SPAWN_X_POS = 100.0
    SPAWN_Y_POS = 50.0
    DEFAULT_SPEED = 4.5

    def __init__(self) -> None:
        self.speed = Ball.DEFAULT_SPEED
        self.x_pos = Ball.SPAWN_X_POS
        self.y_pos = Ball.SPAWN_Y_POS
        self.x_vel, self.y_vel = self.random_vel()
        self.resitance = 1e-5
        pass
    

    def restart(self):
        self.x_pos = Ball.SPAWN_X_POS
        self.y_pos = Ball.SPAWN_Y_POS

        self.x_vel, self.y_vel = self.random_vel()
        
        return
    

    def random_vel(self):
        magnitude = self.speed
        angle_lim = math.pi*70/180 # 70º graus

        angle = random.uniform(0, angle_lim)
        signal = random.choice([1, -1])
        vel_x = signal*magnitude*math.cos(angle)
        vel_y = signal*magnitude*math.sin(angle)
        
        return vel_x, vel_y


    def update_position(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.x_vel = self.x_vel*(1 - self.resitance)
        self.y_vel = self.y_vel*(1 - self.resitance)

    
    def print_info(self):
        print(f'x = {self.x_pos: .2f} y = {self.y_pos: .2f} x_vel = {self.x_vel: .2f} y_vel = {self.y_vel: .2f}')
    

class Player:
    LEFT = 0
    RIGHT = 200
    TOP = 100
    BOTTOM = 0
    X_CENTER = 100
    Y_CENTER = 50
    HEIGHT = 16

    def __init__(self, x_position, y_position) -> None:
        self.x_pos = x_position
        self.y_pos = y_position
        self.vel = 0.0
        self.vel_magnitude = 0.8
        self.score = 0
        self.n_means = 8
        self.position_buffer = self.n_means * [0.0]
        pass


    def update_position(self, new_y_pos):
        self.position_buffer.insert(0, new_y_pos)
        self.position_buffer.pop()

        self.y_pos = self.get_mean_position()
        self.vel = self.get_velocity()
    

    def get_mean_position(self):
        avg = 0
        for pos in self.position_buffer: avg += pos/self.n_means
        
        return avg
    

    def get_velocity(self):
        y_0 = self.position_buffer[-1]
        y_t = self.position_buffer[0]
        delta_y = self.vel_magnitude*(y_t - y_0)/self.n_means
        
        return delta_y


    def increase_score(self):
        self.score += 1


    def reset_score(self):
        self.score = 0


class ColisionDetector:
    def __init__(self, ball, player_a, player_b, sound_engine) -> None:
        self.ball: Ball = ball
        self.player_a: Player = player_a
        self.player_b: Player = player_b
        self.sound_engine: SoundEngine = sound_engine
        
        self.colision = False
        self.left_wall_colision = False
        self.right_wall_colision = False
        self.top_wall_colision = False
        self.bottom_wall_colision = False
        self.player_a_colision = False
        self.player_b_colision = False
        pass


    def detect(self):
        # left and right wall colisions
        self.left_wall_colision = self.ball.x_pos < 0
        self.right_wall_colision = self.ball.x_pos > 200
        
        # top and bottom wall colisions
        self.top_wall_colision = self.ball.y_pos > 100
        self.bottom_wall_colision = self.ball.y_pos < 0

        # colision with player a
        self.player_a_colision = (self.ball.y_pos > self.player_a.y_pos - self.player_a.HEIGHT/2) and (self.ball.y_pos < self.player_a.y_pos + self.player_a.HEIGHT/2) and self.left_wall_colision
        self.player_b_colision = (self.ball.y_pos > self.player_b.y_pos - self.player_b.HEIGHT/2) and (self.ball.y_pos < self.player_b.y_pos + self.player_b.HEIGHT/2) and self.right_wall_colision

        self.colision = self.left_wall_colision or self.right_wall_colision or self.top_wall_colision or self.bottom_wall_colision or self.player_a_colision or self.player_b_colision

        if self.colision: self.handle_colision()

        print(f'{self.player_a.y_pos: .2f},{self.player_a.vel: .2f}')

        return
    

    def handle_colision(self):
        self.sound_engine.play_sound('click')
        if self.top_wall_colision:
            self.ball.y_pos = 100.0
            self.ball.y_vel *= -1

        if self.bottom_wall_colision:
            self.ball.y_pos = 0.0
            self.ball.y_vel *= -1
        
        if self.player_a_colision:
            self.ball.x_pos = 0.0
            self.ball.x_vel *= -1
            self.ball.x_vel += self.player_a.vel
        
        if self.player_b_colision:
            self.ball.x_pos = 200.0
            self.ball.x_vel *= -1
            self.ball.x_vel += self.player_b.vel
        
        if self.left_wall_colision and not self.player_a_colision:
            self.player_b.increase_score()
            self.ball.restart()
        
        if self.right_wall_colision and not self.player_b_colision:
            self.player_a.increase_score()
            self.ball.restart()

        return