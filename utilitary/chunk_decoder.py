from . binary_handler import BinaryHandler
from typing import List

class ChunkDecoder():
    def decode_data(encoded_data):

        US1 = encoded_data['US1']
        US2 = encoded_data['US2']
        
        US1_dist = ChunkDecoder.get_US_dist(US1)
        US2_dist = ChunkDecoder.get_US_dist(US2)
        cursor_1 = ChunkDecoder.get_cursor(US1_dist)
        cursor_2 = ChunkDecoder.get_cursor(US2_dist)

        data = {
            'US1_dist': US1_dist,
            'US2_dist': US2_dist,
            'cursor_1': cursor_1,
            'cursor_2': cursor_2,
        }

        return data
        
        
    def get_US_dist(US_slice: bytes):
        US_dist = 0

        US_D0 = BinaryHandler.get_bits(US_slice[2]) 
        US_D1 = BinaryHandler.get_bits(US_slice[1])
        US_D2 = BinaryHandler.get_bits(US_slice[0])

        US_D0[0] = 0
        US_D1[0] = 0
        US_D2[0] = 0

        US_D0 = BinaryHandler.get_int_from_bits(US_D0)
        US_D1 = BinaryHandler.get_int_from_bits(US_D1)
        US_D2 = BinaryHandler.get_int_from_bits(US_D2)

        US_dist = US_D0 + 10*US_D1 + 100*US_D2

        return US_dist
    
    
    def get_cursor(US_dist, dead_zone=50, capture_zone=250) -> float:
        if US_dist < dead_zone:
            return 0.0
        
        if US_dist > dead_zone + capture_zone:
            return 100.0
        
        cursor = 100.0*(US_dist - dead_zone)/capture_zone

        return cursor
