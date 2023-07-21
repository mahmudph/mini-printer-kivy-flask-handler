import kivy

kivy.require('2.1.0')

import json
import threading
import usb.core
import socket
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from service import app

Window.clearcolor = (255, 255, 255, 1.0)
Window.size = (600, 400)

class MainScreen(MDBoxLayout):
    data_file = "data.json"
    dialog = None
    process = None

    status_id_text  = StringProperty('Tidak Aktif')
    local_server    = StringProperty('http://localhost:5000')
    server_port     = StringProperty('5000')
    vendor_id_text  = StringProperty('')
    product_id_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_data()
        self.get_local_ip()

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.local_server = "http://{0}:{1}".format(s.getsockname()[0], self.server_port)
        s.close()

    def on_save_value(self):
        vendor_id   = self.ids.vendor_id.text
        product_id  = self.ids.product_id.text
        server_port = self.ids.server_port.text

        if vendor_id == '' or product_id == '' or server_port == '':
            return self.show_snack_bar('Mohon Untuk mengisi seluruh field')

        has_correct_vendor_and_product = self.checck_device()

        if not has_correct_vendor_and_product:
            return self.show_snack_bar('Mohon Untuk mengisi vendor id dan produk id dengan benar')

        data = {
            'server_port': server_port,
            'vendor_id': vendor_id,
            'product_id': product_id,
        }

        with open(self.data_file, 'w') as file:
            json.dump(data, file)

        self.status_id_text = "Aktif"
        self.stop_event     = threading.Event()
        self.process        = threading.Thread(target=self.start_service, args=(self.ids.server_port.text, ))

        self.process.setDaemon(True)
        self.process.start()

        self.show_snack_bar("Plugin server berhasil di hidupkan")

    def show_snack_bar(self, message):
        snackbar = Snackbar(text= message,snackbar_x="10dp",snackbar_y="10dp")
        snackbar.open()

    def checck_device(self):
        try:
            vendor_id   = self.ids.vendor_id.text
            product_id  = self.ids.product_id.text

            device = usb.core.find(idVendor=int(vendor_id, 16), idProduct=int(product_id, 16))
            return device != None

        except Exception:
            return False

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.vendor_id_text  = data.get('vendor_id', '')
                self.product_id_text = data.get('product_id', '')
                self.server_port     = data.get('server_port', '5000')
        except FileNotFoundError:
            pass

    def start_service(self, *args):
        port = int(args[0])
        app.run("0.0.0.0", port=port, use_reloader=False)

    def stop_service(self):
        self.process.join()

class RmpPluginApp(MDApp):

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    RmpPluginApp().run()