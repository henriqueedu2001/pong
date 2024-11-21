import pygame
import os

class SoundEngine:
    def __init__(self) -> None:
        self.log_messages = False
        self.sounds = {
            'click': None
        }
        
        self.sounds_paths = {
            'click': '../sound/click.wav'
        }

        # carregamento dos sons
        self.load_sounds()

        return
    

    def load_sounds(self):
        """Carrega todos os sons do jogo
        """
        self.log_message('loading sounds...')
        
        # getting the absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # loading all the sounds
        for sound_key, sound_path in self.sounds_paths.items():
            try:
                self.log_message(f'loading sound {sound_key}')
                
                # loading image
                path = os.path.join(script_dir, sound_path)
                self.sounds[sound_key] = pygame.mixer.Sound(path)
                
                self.log_message(f'sucess in loading sound {sound_key}!')
                pass
            except Exception as exeption:
                self.log_message(f'failed to load sound {sound_key}')
                self.log_message(f'\texeption {exeption}')
                pass
            pass
        
        return
    

    def play_sound(self, sound_name):
        try:
            self.sounds[sound_name].play()
        except Exception as error:
            self.log_message(f'error while playing sound {sound_name}\ndetails: {error}')
        return
    

    def log_message(self, log_message):
        if self.log_messages:
            print(log_message)
            
        return