import sys
from escpos.printer import Usb

def main_handler():
    if len(sys.argv) < 3:
        sys.exit(1)

    vendor_id = sys.argv[1]
    product_id = sys.argv[2]

    qr_code = sys.argv[3]
    qr_code_size = sys.argv[4]

    printer = Usb(int(vendor_id,16), int(product_id, 16))


    printer.qr(qr_code, size=int(qr_code_size))
    printer.set(font='b', align='center', width= 3, height=3)
    printer.text(qr_code)

    printer.cut()
    printer.close();

if __name__ == '__main__':
    main_handler()