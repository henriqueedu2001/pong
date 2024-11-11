from . binary_handler import BinaryHandler
from . chunk import Chunk as Chunk

EMPTY_DATA_BYTE = b'\x00'

class Buffer():
    def __init__(self, buffer_size, chunk_size, break_point_str) -> None:
        self.index = 0
        self.buffer_size = buffer_size
        self.buffer = [EMPTY_DATA_BYTE] * self.buffer_size # inicialização do buffer
        self.chunk_size = chunk_size
        self.break_point_str = break_point_str
        self.last_break_point = -1
        self.chunk:Chunk = Chunk(chunk_size)
        self.chunk_loaded = False
        self.chunk_loading = False
    
    
    def write_buffer(self, byte: bytes, detect_break_point=True, load=True):
        """Escreve um byte no buffer

        Args:
            byte (str): byte a ser escrito
        """
        # índice módulo n = buffer_size que retorna para o início, depois de atingir o limite
        real_byte = BinaryHandler.get_byte(byte)
        index = self.index % self.buffer_size
        self.buffer[index] = real_byte
        
        if detect_break_point:
            if self.is_break_point(real_byte):
                if self.complete_chunk():
                    if load: self.load_chunk()
                else:
                    self.chunk_loading = False
                    pass
                
                self.last_break_point = index
        
        # atualiza índice
        self.index = index + 1
    
        return
    
    
    def load_chunk(self):
        """Carrega um chunk, percorrendo os últimos n = chunk_size bytes do buffer
        """
        self.chunk_loading = True
        
        chunk = []
        
        # percorre o buffer, coletando os bytes do chunk
        for i in range(self.chunk_size):
            buffer_index = self.index
            buffer_index = self.get_absolute_index(buffer_index, i - self.chunk_size + 1)
            byte = BinaryHandler.get_byte(self.buffer[buffer_index])
            chunk.append(byte)
        
        self.chunk.load_chunk(chunk)
        
        self.chunk_loaded = True
        
        return
    
    
    def complete_chunk(self):
        """Verifica se o buffer acabou de receber um buffer completo

        Returns:
            bool: verdadeiro, se houve recepção de um chunk completo e falso caso contrário
        """
        first_chunk_byte_index = self.get_absolute_index(pivot_index=self.index,relative_index=1-self.chunk_size)
        first_chunk_byte = self.buffer[first_chunk_byte_index]
        
        if first_chunk_byte != self.break_point_str[-1]:
            return True
        
        return False
    
    
    def is_break_point(self, last_byte: bytes):
        """Verifica se o buffer acabou de receber um break_point

        Args:
            last_byte (bytes): último byte recebido

        Returns:
            bool: verdadeiro se o buffer recebeu um break point
        """
        last_break_point_str_byte = BinaryHandler.get_byte(self.break_point_str[-1])
        # print("last_break_point_str_byte: ", last_break_point_str_byte)
        break_point_str_size = len(self.break_point_str)
              
        # detecção de byte final de parada
        if last_byte == last_break_point_str_byte:
            # caso o último byte do buffer seja o último byte da str do breakpoint
            # percorra o buffer para trás e verifique se a string é de fato de um breakpoint

            for i in range(break_point_str_size):
                # cálculo dos índices
                break_point_str_index = break_point_str_size - i - 1
                buffer_index = self.get_absolute_index(self.index, -i) 
                
                # obtenção dos caracteres
                break_point_char = BinaryHandler.get_byte(self.break_point_str[break_point_str_index])
                buffer_char = self.buffer[buffer_index]
                
                if buffer_char != break_point_char:
                    return False
                
            return True
        
        return False
    
    
    def get_absolute_index(self, pivot_index, relative_index):
        """Obtém um índice absoluto no buffer, a partir de um índice pivô e um índice relativo.
        por exemplo, num buffer de tamanho 8, para o índice pivô pivot_index = 3, temos:\n
        rel_index = -6 => abs_index = 5\n
        rel_index = -5 => abs_index = 6\n
        rel_index = -4 => abs_index = 7\n
        rel_index = -3 => abs_index = 0\n
        rel_index = -2 => abs_index = 1\n
        rel_index = -1 => abs_index = 2\n
        rel_index = 0 => abs_index = 3 (mesmo do pivô)\n
        rel_index = 1 => abs_index = 4\n
        rel_index = 2 => abs_index = 5\n
        rel_index = 3 => abs_index = 6\n
        rel_index = 4 => abs_index = 7\n
        rel_index = 5 => abs_index = 0\n
        rel_index = 6 => abs_index = 1\n

        Args:
            pivot_index (_type_): _description_
            relative_index (_type_): _description_

        Returns:
            Int: índice no buffer
        """
        if relative_index == 0:
            # retornar mesmo endereço, módulo n = buffer_size
            abs_index = pivot_index % self.buffer_size
        elif relative_index > 0:
            # retornar pivot_index + relative_index, descontando a ultrapassagem à direita
            abs_index = (pivot_index + relative_index) % self.buffer_size
        elif relative_index < 0:
            # retornar pivot_index + relative_index, descontado a ultrapassagem à esquerda
            abs_index = pivot_index + relative_index
            
            if abs_index >= 0:
                # índice ainda positivo
                abs_index = abs_index % self.buffer_size
            elif abs_index < 0:
                # índice negativo, mover para fim do bloco
                abs_index = (abs_index + self.buffer_size) % self.buffer_size
            
        return abs_index
    
    
    def print_buffer(self, bytes_per_line: int = 16, str_format: str = 'hex'):
        """Exibe o conteúdo do buffer
        """
        data = self.buffer
        
        BinaryHandler.print_byte_data(data=data, bytes_per_line=bytes_per_line, str_format=str_format)
    
    
def test():
    buffer = Buffer(buffer_size = 180, chunk_size = 45, break_point_str=b'\x41\x41')
    
    data = b'\x02\xd8\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x41\x41'
    data = data + data + data
    
    for byte in data:
        buffer.write_buffer(byte)
    
    # buffer.print_buffer()
    chunk = buffer.chunk
    chunk.print_chunk()
    chunk.slice_chunk()
    chunk.decode_data()
    # chunk.print_chunk()

# test()