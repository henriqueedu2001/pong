from typing import List
from typing import Union

class BinaryHandler():
    hex_digits_chars = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
    
    def get_byte(byte: Union[bytes, int]) -> bytes:
        real_byte = byte
        
        if type(byte) == int:
            real_byte = bytes([byte])
        
        return real_byte
    
    
    def get_bytes_from_str(str_content: str) -> List[bytes]:
        content_bytes = []
        hex_digits = []
        
        for character in str_content:
            if character in BinaryHandler.hex_digits_chars:
                hex_digits.append(character)
        
        if len(hex_digits) % 2 == 0:
            bytes_quantity = len(hex_digits)//2
            
            for i in range(bytes_quantity):
                hex_str = f'{hex_digits[2*i]}{hex_digits[2*i+1]}'
                decimal_int = int(hex_str, 16)
                byte = BinaryHandler.get_byte(decimal_int)
                content_bytes.append(byte)
        
        return content_bytes
    
    
    def get_int(byte: bytes) -> int:
        int_value = int.from_bytes(byte, byteorder='big')
        
        return int_value
    
    
    def cast_bool(bit: int) -> bool:
        bool_value = True if bit == 1 else False
        
        return bool_value
    
    
    def get_int_from_bits(bits: List[int]):
        binary_str = ''.join(map(str, bits))
        number = int(binary_str, 2)
        
        return number
    
    
    def get_byte_str(byte: Union[bytes, int], str_format='hex') -> str:
        byte_str = 'XX'
        byte_int = byte
        
        if type(byte) == bytes:
            byte_int = BinaryHandler.get_int(byte)
        
        if str_format == 'hex':
            byte_hex = '{:02x}'.format(byte_int)
            byte_str = byte_hex
        elif str_format == 'bin':
            bits = BinaryHandler.get_bits(byte_int)
            byte_str = ''.join(map(str, bits))
            
        return byte_str
    
    
    def get_bits(byte: Union[bytes, int]) -> List[int]:
        bits = [0] * 8
        
        byte_int = byte
        
        # converte byte para int
        if type(byte) == bytes:
            byte_int = BinaryHandler.get_int(byte)
                  
        for i in range(8):
            bit = BinaryHandler.get_bit(byte=byte_int, index=i)
            bits[7-i] = bit
            
        return bits


    def get_bit(byte: Union[bytes, int], index: int) -> int:
        """Retorna o valor do bit na posição index do byte"""
        byte_int = byte
        bit = 0
        
        # converte para int, se necessário
        if type(byte_int) == bytes:
            byte_int = BinaryHandler.get_int(byte)
        
        bit = (byte_int >> index) & 1
        
        return bit
    
    
    def print_byte(byte: Union[bytes, int], str_format: str = 'hex') -> None:
        if byte is None:
            return
        
        byte_str = BinaryHandler.get_byte_str(byte, str_format=str_format)
        
        print(byte_str)
        
        return
    
    
    def print_byte_data(data: Union[bytes, List[int]] , bytes_per_line: int = 16, str_format: str = 'hex') -> None:
        byte_data_str = BinaryHandler.get_byte_data_str(data, bytes_per_line=bytes_per_line, str_format=str_format)
        print(byte_data_str)
        
        return
    
    
    def get_byte_data_str(data: Union[bytes, List[int]] , bytes_per_line: int = 16, str_format: str = 'hex') -> str:
        if data == None:
            return 'empty'
        
        block_size = len(data)
        lines = (block_size // bytes_per_line)
        tail_size = block_size % bytes_per_line
        spacing_char = ' '
        byte_data_str = ''

        # imprimir bloco, com exceção da cauda
        for i in range(lines):
            for j in range(bytes_per_line):
                index = i*bytes_per_line + j
                byte = data[index]
                byte_char = BinaryHandler.get_byte_str(byte=byte, str_format=str_format)
                byte_data_str = byte_data_str + byte_char + spacing_char
            
            byte_data_str = byte_data_str + '\n'
        
        # imprimir cauda
        if tail_size != 0:
            for j in range(tail_size):
                index = lines*bytes_per_line + j
                byte = data[index]
                byte_char = BinaryHandler.get_byte_str(byte=byte, str_format=str_format)
                byte_data_str = byte_data_str + byte_char + spacing_char

        
        return byte_data_str

def test():
    byte_tape = b'\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03'
    byte_tape_str = '00 01 02 03 00 01 02 03 00 01 02 03 00 01 02 03 \n00 01 02 03 '
    
    ggg = BinaryHandler.get_bytes_from_str(byte_tape_str)
    
    # BinaryHandler.print_byte_data(data=byte_tape, str_format='hex')
    
    return

# test()