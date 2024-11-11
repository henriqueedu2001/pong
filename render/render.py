import pygame
import os


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

T_largura, T_altura = 900, 600
M_largura, M_altura = 900, 600
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

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
        self.jog1 = Player(0, 0, 10, 100)
        self.jog2 = Player(M_largura - 10, 0, 10, 100)
        self.bola = Bola(M_largura//2, M_altura//2, 10, 7, 7)

        self.cor = WHITE

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
        
        self.render_gameplay()
        
        return
    
    
    def render_gameplay(self):
        # RenderGameplay.render(self.screen_class, self.data)

        deltaX = 2
        deltaY = 1

        #Definicao dos objetos
        jog1 = self.jog1
        jog2 = self.jog2
        bola = self.bola

        nex_jog_1_pos, nex_jog_2_pos = 0, 0

        try:
            nex_jog_1_pos = self.get_pos(self.data['US1_dist'])
            nex_jog_2_pos = self.get_pos(self.data['US2_dist'])

            self.jog1.update(0, T_altura - nex_jog_1_pos)
            self.jog2.update(M_largura - 20, T_altura - nex_jog_2_pos)

        except Exception as e:
            print(f'error: {e}')

        self.jog1.posy = nex_jog_1_pos
        self.jog2.posy = nex_jog_2_pos

        # print(f'{self.data} {nex_jog_1_pos} {nex_jog_2_pos}')

        if checaColisaoBolaMapa(bola):
            if bola.dirY == -1:
                bola.updateVel(bola.velX, bola.velY, bola.dirX, 1)
            else:
                if bola.dirY == 1:
                    bola.updateVel(bola.velX, bola.velY, bola.dirX, -1)

        if checaColisaoJogadorBola(jog1, bola):
            bola.updateVel(bola.velX + deltaX, bola.velY + deltaY, 1 , bola.dirY)

        if checaColisaoJogadorBola(jog2, bola):
            bola.updateVel(bola.velX + deltaX, bola.velY + deltaY, -1 , bola.dirY)
        
        pygame.draw.circle(self.screen, self.cor, (self.bola.posx, self.bola.posy), self.bola.raio)
        pygame.draw.rect(self.screen, self.cor, self.jog1.geekRect)
        pygame.draw.rect(self.screen, self.cor, self.jog2.geekRect)

        return
    

    def get_pos(self, US_dist):

        return int(US_dist*20)
    

    def render_debug(self):
        # RenderDebug.render(self.screen_class, self.data)    
        return
    

    def clear_screen(self):
        self.screen.fill(BLACK)
    
    
    def log_message(self, log_message):
        if self.log_messages:
            print(log_message)
            
        return


class Player:
    def __init__(self, posx, posy, largura, altura):
        self.posx = posx
        self.posy = posy
        self.largura = largura
        self.altura = altura

        #Retangulo generico do pygame:
        self.geekRect= pygame.Rect(self.posx, self.posy, self.largura, self.altura)        


    def update(self, newx, newy):
        
        #Atualiza com os valores recebidos
        self.posx, self.posy = newx, newy

        #Update do retangulo
        self.geekRect= pygame.Rect(self.posx, self.posy, self.largura, self.altura)        


class Bola:
    def __init__(self, posx, posy, raio, velX, velY):
        self.posx = posx
        self.posy = posy
        self.raio = raio
        self.velX = velX
        self.velY = velY
        self.dirX = 0
        self.dirY = 0
        self.primeiraVez = 1


    def update(self):
        self.posx += self.velX*self.dirX
        self.posy += self.velY*self.dirY


    def updateVel(self, velX, velY, dirX, dirY):
        self.velX = velX
        self.velY = velY 
        self.dirX = dirX
        self.dirY = dirY


def checaColisaoJogadorBola(jogador, bola):
    limX = jogador.posx + jogador.largura
    limY1 = jogador.posy
    limY2 = jogador.posy + jogador.altura

    colisaoX = False
    colisaoY = False

    #bola na posicao X do jogador
    if bola.posx + bola.raio <= limX:
        colisaoX = True
    else:
        colisaoX = False

    #bola na posicao Y do Jogador
    if limY1 <= bola.posy + bola.raio <= limY2:
        colisaoY = True
    else:
        colisaoY = False 

    return (colisaoY and colisaoX)


def checaColisaoBolaMapa(bola):
    if bola.posx + bola.raio >= M_altura:
        return True
    else:
        return False 


def checaPonto(bola):
    if bola.posx <= 0:
        return -1
    else:
        if bola.posx >= M_largura:
            return 1
        else: 
            return 0