import pygame
import random
import time # for debbuging
from utilitary import uart as uart
from utilitary.byte_tape import ByteTape
from utilitary.buffer import Buffer as Buffer
from utilitary.chunk import Chunk
from utilitary.binary_handler import BinaryHandler
from render.render import RenderEngine
from engine.game_engine import GameEngine
from sound.sound_engine import SoundEngine

BUFFER_SIZE = 9*5
CHUNK_SIZE = 9
BREAK_POINT_STR = b'\xff\xff\xff'
DEFAULT_PORT_NAME = '/dev/ttyUSB1'

DEFAULT_GAME_CONFIG = {
  'screen_widht': 1200,
  'screen_heigth': 600,
  'serial_port': '/dev/ttyUSB1',
  'mode': 'debug',
  'byte_tape': 'vertical_slide',
  'delay': 0.001,
  'print_buffer': False,
  'print_chunk': False,
  'print_uart': False,
  'print_received_data': False,
  'print_actual_screen': False
}

DEFAULT_RENDER_CONFIG = {
    'render_mode': 'gameplay'
}

class Game():
  def __init__(self, game_config=DEFAULT_GAME_CONFIG, render_config=DEFAULT_RENDER_CONFIG) -> None:
    self.game_config = game_config
    
    # delay
    self.delay = self.game_config['delay']
    
    # debugging
    self.debug_mode = True if self.game_config['mode'] == 'debug' else False
    self.debug_byte_tape_name = self.game_config['byte_tape']
    self.debug_byte_tape = ByteTape()
    self.log_messages = True
    self.degug_count = 0
    self.degug_count_max = 0
    
    # prints de depuração
    self.print_buffer = self.game_config['print_buffer']
    self.print_chunk = self.game_config['print_chunk']
    self.print_uart = self.game_config['print_uart']
    self.print_received_data = self.game_config['print_received_data']
    self.print_actual_screen = self.game_config['print_actual_screen']
    
    # pygame parameters
    self.screen = None
    self.clock = None

    # game engine
    self.game_engine = None
    self.game_data = None
    self.keys = None
    
    # buffer
    self.buffer = Buffer(buffer_size=BUFFER_SIZE, chunk_size=CHUNK_SIZE, break_point_str=BREAK_POINT_STR)
    self.received_game_data = None
    self.menu_byte = None
    self.last_byte = None
    
    # render
    self.render_config = render_config
    self.render_engine = None
    self.text_font = None
    
    # uart
    self.port = None
    self.port_opened = False
    self.port_name = game_config['serial_port']
    

  def start_game(self):
    """Inicia o jogo pong
    """
    
    # Mensagens de log
    self.log_message('starting game...')
    self.log_message(f'game config: {self.game_config}')
    self.log_message(f'render config: {self.render_config}')
    
    # abertura do canal de recepção de dados (UART ou FITA BINÁRIA)
    if self.debug_mode:
      self.log_messages = True
      self.log_message('debug mode activated')
      self.load_byte_tape()
    else:
      self.log_message('gameplay mode activated')
      self.open_uart_port()

    self.init_pygame()
    
    self.render_engine = RenderEngine(pygame_screen=self.screen, config=self.render_config)
    self.game_engine = GameEngine()

    # roda o jogo
    self.run_game()
    

  def init_pygame(self):
    try:
      pygame.init()
      pygame.mixer.init()
      self.log_message('starting pygame...')
      
      width = self.game_config['screen_widht']
      heigth = self.game_config['screen_heigth']
      self.screen = pygame.display.set_mode((width, heigth))
      self.clock = pygame.time.Clock()
      
      self.log_message('pygame started with sucess!')
    
    except Exception as exeption:
      self.log_message('failed to start the pygame')
      
    return
  

  def load_byte_tape(self):
    try:
      self.log_message('loading byte tape...')
      self.debug_byte_tape.load_tape(self.debug_byte_tape_name)
      self.log_message('byte tape loaded')
    
    except Exception as execption:
      self.log_message(f'failed to load byte tape\n error: {execption}')
    
    return
  
  
  def open_uart_port(self):
    self.log_message('opening uart')

    while self.port_opened == False:
        try:
          self.port = uart.open_port(port_name=self.port_name)
          self.port_opened = True
          self.log_message('uart port started with sucess!')
        
        except Exception as exeption:
          self.log_message(f'failed to start the uart.\ndetails: {exeption}')
          time.sleep(2)
          
    return


  def run_game(self):
    """Roda o jogo poli-asteroids
    """
    self.log_message('running game...')
    
    run = True
    
    while run:
      self.receive_data(delay=self.delay)
      self.update_game()
      self.render()
      
      for event in pygame.event.get():
        # lógica de fim do jogo
        if event.type == pygame.QUIT:
          self.log_message('player left the game')
          run = False
      
      pygame.display.flip()

    # sair do jogo
    pygame.quit()
  
  
  def receive_data(self, delay=0):
    """Recebe os dados da placa FPGA via transmissão serial
    """
    time.sleep(delay)
    
    buffer = self.buffer
    
    n_bytes = self.buffer.buffer_size
    received_bytes = None
    
    # escolhe entre a UART e a fita binária
    if self.debug_mode:
      received_bytes = self.receive_byte_tape()
    else:
      received_bytes = self.receive_uart_bytes(self.port, n=n_bytes, print_data=self.print_uart)  

    if received_bytes!= None and received_bytes != []:   
      self.last_byte = received_bytes[-1] 
      for received_byte in received_bytes:
        buffer.write_buffer(received_byte)
    else:
      self.last_byte = None
      if self.print_received_data: self.log_message('No byte received')
    
    if received_bytes != None:
      if len(received_bytes) == 1:
        self.menu_byte = received_bytes[-1]
        self.actual_screen = self.decode_menu_byte()
    
    if self.last_byte == b'\xf2' or self.last_byte == 242:
      if self.actual_screen == 'gameplay':
        self.actual_screen = 'gameover'
      
    if self.print_received_data:
        BinaryHandler.print_byte_data(received_bytes)

    if buffer.chunk_loading:
      self.load_chunk()
      
    self.print_debug()
    
    return
  
  
  def load_chunk(self):
    try:
      self.buffer.chunk.slice_chunk()
      self.buffer.chunk.decode_data()
      
    except Exception as exception:
      self.log_message(f'error while loading chunk\n details:{exception}')
      
    self.received_game_data = self.buffer.chunk.decoded_data
    
    return
  
  def receive_byte_tape(self):
    try:
      bytes = self.debug_byte_tape.read_bytes()
      return bytes
    
    except:
      return None
  
  
  def decode_menu_byte(self):
    encoding = {
      b'\xf0': 'initial_menu',
      b'\xf1': 'players_scores',
      b'\xf2': 'gameover',
      b'\xf3': 'register_score',
      b'\xf4': 'gameplay',
      240: 'initial_menu',
      241: 'players_scores',
      242: 'gameover',
      243: 'register_score',
      244: 'gameplay',
      None: 'gameplay',
    }
    
    
    screen = encoding[self.menu_byte]
    
    return screen
  
  
  def receive_uart_bytes(self, port, n=24, print_data=False):
    try:
      byte = uart.receive_data(port, n=n, print_data=print_data)
      return byte
    
    except:
      return None
  
  
  def render(self):
    if self.print_actual_screen:
      print(self.actual_screen)
      
    data = self.game_data
    self.render_engine.load_data(data)
    self.render_engine.render()
    
    return
  

  def update_game(self):
    self.game_engine.load_data(received_game_data=self.received_game_data, user_keys=self.keys)
    self.game_engine.update()
    self.game_data = self.game_engine.get_game_data()
    
    return
  

  def log_message(self, log_message):
    if self.log_messages:
        print(f'[ LOG ] {log_message}')
    
    return
  
  
  def print_debug(self):
    if self.buffer.chunk_loading:
      try:
        self.buffer.chunk.slice_chunk()
        self.buffer.chunk.decode_data()
        
        if self.print_chunk:
          self.buffer.chunk.print_chunk()
          print()
        
        if self.print_buffer:
          self.buffer.print_buffer()
          print()
        
      except Exception as exeption:
        self.log_message(f'error while loading chunk\n{exeption}')
        
    return


if __name__ == '__main__':
  game = Game()
  game.start_game()