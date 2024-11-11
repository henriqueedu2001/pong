import pygame
import os


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NOT_LOADED_ASTEROID_POSITION = (0, 0)
NOT_LOADED_SHOOT_POSITION = (0, 0)

GRID_SIZE = 15 # em unidades relativas
size_factor = 1 

DEFAULT_CONFIG = {
    'render_mode': 'gameplay'
}
    
class RenderEngine():
    def __init__(self, pygame_screen, actual_screen='gameplay', config=DEFAULT_CONFIG) -> None:
        self.config = config
        self.render_mode = config['render_mode']
        self.data = None
        self.loaded_data = False
        self.screen = pygame_screen
        self.actual_screen = actual_screen
        self.screen_width, self.screen_height = pygame_screen.get_size()
        self.min_size = self.screen_width
        self.default_text_font = pygame.font.SysFont(None, 24)
        self.log_messages = False
        
        # self.screen_class = Screen(pygame_screen, None)
        
        self.debug_mode = False
        
        # state variables
        self.score = None
        self.player_direction = None
        self.lifes_quantity = None
        self.game_difficulty = None
        self.asteroids = None
        self.asteroids_positions = None
        self.asteroids_directions = None
        self.shots = None
        self.shots_positions = None
        self.shots_directions = None
        self.played_special_shooting = None
        self.available_special_shooting = None
        self.played_shooting = None
        self.end_of_lifes = None
        self.players_scores = [
            {'name': 'player_01', 'score': 201},
            {'name': 'player_02', 'score': 168},
            {'name': 'player_03', 'score': 95},
            {'name': 'player_04', 'score': 85},
            ]
        
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
        self.images = {
            'life': None,
            'space_ship': None,
            'shot': None,
            'asteroid': None,
            'asteroid_01': None,
            'asteroid_02': None,
            'asteroid_03': None,
            'asteroid_04': None
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
                
                self.screen_class.images = self.images
                
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
    
    
    def render(self, screen):
        self.clear_screen()
        
        # telas possíveis: initial_menu, gameplay, gameover e players_scores
        if self.render_mode == 'debug':
            self.actual_screen = 'debug'
        
        actual_screen = screen
        
        render_engines = {
            'initial_menu': self.render_initial_menu,  
            'gameplay': self.render_gameplay,  
            'gameover': self.render_gameover,  
            'players_scores': self.render_players_scores,
            'register_score': self.render_players_scores,
            'debug': self.render_debug,
            'loading': self.render_loading
        }
        
        render_engines[actual_screen]()
        
        return
    
    
    def render_gameplay(self):
        # RenderGameplay.render(self.screen_class, self.data)
        
        return
    
    
    def render_gameover(self):
        # RenderGameOver.render(self.screen_class, self.data)
        
        return
    
    
    def render_initial_menu(self):
        # RenderInitialMenu.render(self.screen_class, self.data)
        
        return
    
    
    def render_players_scores(self):
        # RenderPlayersScores.render(self.screen_class, self.data)
        
        return
    
    
    def render_loading(self):
        # RenderLoading.render(self.screen_class, self.data)
        
        return
    
    
    def render_debug(self):
        # RenderDebug.render(self.screen_class, self.data)    
        return
    
    
    def clear_screen(self):
        self.screen.fill(BLACK)
    
    
    def log_message(self, log_message):
        if self.log_messages:
            print(log_message)
            
        return