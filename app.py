from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from encryption import encrypt_image, decrypt_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directories exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'original'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted'), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original', file.filename)
            file.save(image_path)
            encrypted_path, key = encrypt_image(image_path)
            encrypted_file_name = os.path.basename(encrypted_path)
            return render_template('encrypt.html', encrypted_image=encrypted_file_name, key=key)
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files['encrypted_image']
        key = request.form['key']
        if file and key:
            encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted', file.filename)
            file.save(encrypted_path)
            decrypted_path = decrypt_image(encrypted_path, key)
            decrypted_file_name = os.path.basename(decrypted_path)
            return render_template('decrypt.html', decrypted_image=decrypted_file_name)
    return render_template('decrypt.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    folder = ''
    if 'original' in filename:
        folder = 'original'
    elif 'encrypted' in filename:
        folder = 'encrypted'
    elif 'decrypted' in filename:
        folder = 'decrypted'
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
