import serial
import time

import serial.tools
import serial.tools.list_ports

from . binary_handler import BinaryHandler

DEFAULT_PORT_NAME = 'COM15'

def show_ports():
    """Imprime as portas disponíveis
    """
    
    ports = serial.tools.list_ports.comports()
    
    if ports:
        print("Available serial ports:")
        for port in ports:
            print(port.device)
    else:
        print("No serial port founded!.")


def open_port(port_name: str):
    """_summary_

    Args:
        port_name (str): nome da porta serial

    Returns:
        serial.Serial: porta serial
    """
    # Configurar a porta serial (substitua '/dev/ttyUSB0' pelo seu dispositivo serial)
    serial_port = serial.Serial(port_name, baudrate=115200, timeout=1, parity=serial.PARITY_NONE)

    return serial_port


def receive_data(serial_port: serial.Serial, n=1, print_data=False):
    """recebe um byte de dados

    Args:
        serial_port (serial.Serial): _description_

    Returns:
        _type_: _description_
    """
    try:
        received_bytes = serial_port.read(n)
        if received_bytes:
            if print_data:
                BinaryHandler.print_byte_data(received_bytes)
                
            return received_bytes
        
    except:
        return None

    return None


def send_data(serial_port: serial.Serial, data: bytes):
    """Envia um byte de dados

    Args:
        serial_port (serial.Serial): _description_
        data (bytes): _description_
    """

    # Converta a entrada de string para bytes antes de enviar
    encoded_data = data.encode()
    serial_port.write(encoded_data)  

    return


def send_test():
    """teste do envio de dados
    """
    port_name = DEFAULT_PORT_NAME
    data_chunk = ['a', 'b', 'c']
    port = open_port(port_name)

    while True:
        for character in data_chunk:
            print(character)
            send_data(port, character)
            time.sleep(1)

    pass 


def receive_test():
    """teste do recebimento de dados
    """
    port_name = DEFAULT_PORT_NAME
    port = open_port(port_name)

    while True:
        received_data = receive_data(port)
        print(received_data)

    return


def data_transmission_test():
    port_name = DEFAULT_PORT_NAME
    port = open_port(port_name)

    i = 0
    data_chunk = ['a', 'b', 'c']

    while True:
        for data_byte in data_chunk:
            send_data(port, data_byte)
            print(f'dado enviado: {data_byte}')
            time.sleep(1)

        received_data = receive_data(port)
        print(f'dado recebido: {received_data}')

        time.sleep(1)

    pass