from . binary_handler import BinaryHandler
from . chunk_decoder import ChunkDecoder

EMPTY_DATA_BYTE = b'\x00'

class Chunk():
    def __init__(self, chunk_size) -> None:
        self.chunk_size = chunk_size
        self.content = [EMPTY_DATA_BYTE] * self.chunk_size
        self.loaded = False
        self.encoded_data = None
        self.decoded_data = None
    
    
    def load_chunk(self, chunk: str):
        """Carrega um chunk de dados na memória

        Args:
            chunk (str): string do chunk de dados
        """
        
        self.content = chunk
        self.loaded = True
        
        return
    
    
    def slice_chunk(self):
        """Divide o chunk de dados em segmentos de informação
        """

        chunk = self.content

        self.print_chunk()

        US1 = chunk[5:8]
        US2 = chunk[8:11]
        
        # pedaços de informação
        
        sliced_chunk = {
            'US1': US1,
            'US2': US2
        }
        
        self.encoded_data = sliced_chunk
        
        return
    
    
    def decode_data(self) -> dict:
        """Obtém os dados a partir dos dados codificados no chunk

        Returns:
            dict: dicionário com as variáveis decodificadas
        """
        if self.loaded:
            # fatiamento dos dados
            self.slice_chunk()
            
            # decodificando dados
            encoded_data = self.encoded_data
            data = ChunkDecoder.decode_data(encoded_data)
            self.decoded_data = data
        
        return
    
        
    def print_chunk(self, bytes_per_line: int = 16, str_format: str = 'hex'):
        """Exibe o conteúdo do chunk
        """
        data = self.content
        
        BinaryHandler.print_byte_data(data=data, bytes_per_line=bytes_per_line, str_format=str_format)
    
    
    
    def print_decoded_data(self):
        data = self.decoded_data
        max_key_length = max(len(str(key)) for key in data.keys())
        
        for key, value in data.items():
            print(f"{str(key):<{max_key_length}} : {value}")


def test():
    chunk = Chunk(chunk_size=64)
    chunk.load_chunk('pç1111222233334444qwer9999888877776666asdfè$&')
    chunk.print_chunk()
    
    # chunk.slice_chunk()
    data = chunk.decode_data()
    
    print(data)
    pass


# test()