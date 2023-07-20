from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/print', methods=['POST'])
def print_handler():
    vendor_id       = request.form.get('printer_vendor_id', type=str),
    product_id      = request.form.get('printer_product_id', type=str),
    qr_code_no      = request.form.get('qr_code_no', type=str),
    qr_code_size    = request.form.get('qr_code_size', 16, str),

    if request.method == 'POST':

        if vendor_id[0] == None or product_id[0] == None:
            return jsonify({"status": 'Error', 'message': 'Mohon atur terlebih dahulu konfigurasi printer'}), 500

        result = subprocess.run(['python3', 'print_handler.py', vendor_id[0], product_id[0], qr_code_no[0], qr_code_size[0]], capture_output=True)
        if result.returncode == 0:
            return jsonify({"status": 'OK', 'message': 'Cetak kode QR berhasil'}), 200

        return jsonify({"status": 'OK', 'message': 'Cetak kode QR gagal'}), 500

    return jsonify({"status": 'ERROR'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)