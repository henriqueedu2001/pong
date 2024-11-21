class Screen():
    def __init__(self, pygame_screen, images) -> None:
        self.pygame_screen = pygame_screen
        self.screen_width, self.screen_height = pygame_screen.get_size()
        self.images = images
        self.top = 0
        self.bottom = self.screen_height
        self.left = 0
        self.right = self.screen_width
        self.center_x = self.screen_width//2
        self.center_y = self.screen_height//2
        
        pass
    
    
    def print_info(self):
        print(f'width = {self.screen_width} height = {self.screen_height}')
        
        return
    
        
    def ru_x(self, x):
        ru_x = int(x*self.screen_width/100)
        
        return ru_x
    
    
    def ru_y(self, y):
        ru_y = int(y*self.screen_height/100)
        
        return ru_y
    
    
    def ru_size(self, size):
        ru_s = self.ru_y(size)
        
        return ru_s
    
    def relative_units_x(self, x):
        return self.ru_x(x)
    
    
    def relative_units_y(self, y):
        return self.ru_x(y)
    