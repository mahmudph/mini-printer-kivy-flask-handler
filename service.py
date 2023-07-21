from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json



app = Flask(__name__)
CORS(app, resources={r'/*': {"origins": '*'}})

@app.route('/print', methods=['POST'])
def print_handler():
    vendor_id       = request.form.get('printer_vendor_id', type=str),
    product_id      = request.form.get('printer_product_id', type=str),
    qr_code_no      = request.form.get('qr_code_no', type=str),
    qr_code_size    = request.form.get('qr_code_size', 16, str),


    if request.method == 'POST':
        try:
            with open("data.json", 'r') as file:
                data = json.load(file)
                vendor_id = data.get('vendor_id', '')
                product_id = data.get('product_id', '')

                if vendor_id[0] == None or product_id[0] == None:
                    return jsonify({"status": 'Error', 'message': 'Mohon atur terlebih dahulu konfigurasi printer'}), 500

                result = subprocess.run(['python3', 'print_handler.py', vendor_id[0], product_id[0], qr_code_no[0], qr_code_size[0]], capture_output=True)
                if result.returncode == 0:
                    return jsonify({"status": 'OK', 'message': 'Cetak kode QR berhasil'}), 200

                return jsonify({"status": 'OK', 'message': 'Cetak kode QR gagal'}), 500

        except Exception:
            pass
        except FileNotFoundError:
            pass

    return jsonify({"status": 'ERROR'}), 403