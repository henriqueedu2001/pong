
import time # for debbuging
from utilitary import uart as uart
from utilitary.binary_handler import BinaryHandler

def main():
    uart.show_ports()
    port = uart.open_port('/dev/ttyUSB1', 115200)

    while True:
        x = uart.receive_data(port, n=9*4)
        BinaryHandler.print_byte_data(x, 9, 'hex')
        time.sleep(0.5)
    return

main()