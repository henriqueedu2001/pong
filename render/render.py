import pygame
import os

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
    
class RenderEngine():
    def __init__(self, pygame_screen, config=DEFAULT_CONFIG) -> None:
        self.config = config
        self.render_mode = config['render_mode']
        self.data = None
        self.loaded_data = False
        self.pygame_screen = pygame_screen
        self.screen_width, self.screen_height = pygame_screen.get_size()
        self.min_size = self.screen_width
        self.default_text_font = pygame.font.SysFont(None, 24)
        self.log_messages = True
        
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
            'player_a': None,
            'player_b': None,
            'asteroid': None,
        }
        
        self.images_paths = {
            'life': 'heart.png',
            'space_ship': 'space_ship.png',
            'shot': 'shot.png',
            'asteroid_01': 'asteroid_01.png',
            'asteroid_02': 'asteroid_02.png',
            'asteroid_03': 'asteroid_03.png',
            'asteroid_04': 'asteroid_04.png',
            'asteroid_05': 'asteroid_05.png',
            'asteroid_06': 'asteroid_06.png',
            'asteroid_07': 'asteroid_07.png',
            'asteroid_08': 'asteroid_08.png'
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
                path = os.path.join(script_dir, "imgs", img_path)
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
        self.render_gameplay(screen=self.screen)
        
        return
    
    
    def render_gameplay(self, screen):
        self.draw_player_a(screen)
        self.draw_player_b(screen)

        return
    

    def draw_player_a(self, screen):
        x, y = screen.ru_x(50), screen.ru_y(50)
        Artist.draw_text(self.screen, 'test', x, y)
        
        return
    

    def draw_player_b(self, screen):
        return
    

    def clear_screen(self):
        self.pygame_screen.fill(BLACK)
    
    
    def log_message(self, log_message):
        if self.log_messages:
            print(log_message)
            
        return