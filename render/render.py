import pygame
import os

from typing import *

from . screen import Screen
from . artist import Artist

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

size_factor = 1 

DEFAULT_CONFIG = {
    'render_mode': 'gameplay'
}
    
class RenderEngine:
    def __init__(self, pygame_screen, config=DEFAULT_CONFIG) -> None:
        self.config = config
        self.render_mode = config['render_mode']
        self.data = None
        self.loaded_data = False
        self.pygame_screen = pygame_screen
        self.screen_width, self.screen_height = pygame_screen.get_size()
        self.min_size = self.screen_width
        self.default_text_font = pygame.font.SysFont(None, 24)
        self.log_messages = False
        
        self.screen = Screen(pygame_screen, None)
        self.debug_mode = False

        self.player_a_score = 0
        self.player_b_score = 0
        
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
        self.images = {
            'ball': None,
            'player': None,
            'player_a': None,
            'player_b': None,
            'asteroid': None,
        }
        
        self.images_paths = {
            'ball': '../art/ball.png',
            'player': '../art/player.png',
            'player_a': '../art/player.png',
            'player_b': '../art/player.png',
        }
        
        self.db_index = 0
        
        # carregamento de imagens
        self.load_assets()
        
        return
    
    
    def load_assets(self):
        """Carrega todas as imagens no jogo
        """
        self.log_message('loading images...')
        
        # getting the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # loading all images
        for img_key, img_path in self.images_paths.items():
            try:
                self.log_message(f'loading image {img_key}')
                
                # loading image
                path = os.path.join(script_dir, img_path)
                self.images[img_key] = pygame.image.load(path)
                
                self.screen.images = self.images
                
                self.log_message(f'sucess in loading image {img_key}!')
                pass
            except Exception as exeption:
                self.log_message(f'failed to load image {img_key}')
                self.log_message(f'\texeption {exeption}')
                pass
            pass
        
        return
    
    
    def load_data(self, data):
        if data != None:
            self.data = data
            self.loaded_data = True
        else:
            self.loaded_data = False
            
        return
    
    
    def render(self):
        self.clear_screen()

        if self.loaded_data:
            self.render_gameplay(screen=self.screen)
        
        return
    
    
    def render_gameplay(self, screen):
        self.draw_ball(screen)
        self.draw_player_a(screen)
        self.draw_player_b(screen)

        return
    

    def draw_ball(self, screen: Screen):
        x_pos, y_pos = self.data['ball_x_pos'], self.data['ball_y_pos']
        x_pos, y_pos = self.get_ball_pos(screen, x_pos, y_pos)
        ball_size = screen.ru_size(5)
        Artist.draw_image(screen, self.images['ball'], x_pos, y_pos, ball_size, ball_size, border=False, alignment='center')
        return
    

    def draw_player_a(self, screen: Screen):
        player_width, player_height = screen.ru_x(1), screen.ru_y(16)

        # position
        x_pos = player_width//2
        cursor = self.data['player_a_y_pos']
        y_pos = self.get_player_pos(screen, cursor)
        
        Artist.draw_image(screen, self.images['player'], x_pos, y_pos, player_width, player_height, alignment='top left')
        
        return
    

    def draw_player_b(self, screen: Screen):
        player_width, player_height = screen.ru_x(1), screen.ru_y(16)

        # position
        x_pos = screen.screen_width - (player_width//2)
        cursor = self.data['player_b_y_pos']
        y_pos = self.get_player_pos(screen, cursor)
        
        Artist.draw_image(screen, self.images['player'], x_pos, y_pos, player_width, player_height, alignment='top left')
        
        return
    

    def get_player_pos(self, screen: Screen, cursor: float) -> int:
        return screen.bottom - screen.ru_y(int(cursor))
    

    def get_ball_pos(self, screen: Screen, x_pos: float, y_pos) -> Tuple[int, int]:
        x_coordinate = screen.ru_x(x_pos/2)
        y_coordinate = screen.bottom - screen.ru_y(y_pos)
        
        return x_coordinate, y_coordinate
    

    def clear_screen(self):
        self.pygame_screen.fill(BLACK)
    
    
    def log_message(self, log_message):
        if self.log_messages:
            print(log_message)
            
        return