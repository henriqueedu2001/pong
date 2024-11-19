class Screen():
    def __init__(self, pygame_screen, images) -> None:
        self.pygame_screen = pygame_screen
        self.screen_width, self.screen_height = pygame_screen.get_size()
        self.images = images
        self.top = 0
        self.bottom = self.screen_height
        self.left = 0
        self.right = self.screen_width
        self.inner_grid_offset_y = self.ru_size(5)
        self.inner_grid_x_margin = self.ru_x(10)
        self.inner_grid_y_margin = self.ru_y(10)
        
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
    
    
    def grid_x(self, x_index):
        new_x = 0
        width = self.screen_width
        horizontal_margin = self.inner_grid_x_margin
        w, hm  = width, horizontal_margin
        
        new_x = int(hm + ((w - 2*hm)/14)*x_index)
        
        return new_x
    
    
    def grid_y(self, y_index):
        new_y = 0
        height = self.screen_height
        vertical_margin = self.inner_grid_y_margin
        h, vm = height, vertical_margin
        
        new_y = int(vm + ((h - 2*vm)/14)*(14-y_index))
        
        new_y += self.inner_grid_offset_y
        
        return new_y
    