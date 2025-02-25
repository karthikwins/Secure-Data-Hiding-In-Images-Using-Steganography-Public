from flask import Flask, render_template, request, send_file
import os
from backend_code import encrypt_image, decrypt_image  # Assuming the backend code is saved as backend_code.py
from waitress import serve

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created directory: {UPLOAD_FOLDER}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    print("Index route hit")
    return render_template('encrypt_decrypt.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    print("Encrypt route hit")
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(f"Saving uploaded file to: {filepath}")
        file.save(filepath)
        
        if os.path.exists(filepath):
            print(f"File successfully saved at: {filepath}")
        else:
            print("File not saved successfully.")
        
        msg = request.form['message']
        password = request.form['password']
        
        encrypted_filepath = encrypt_image(filepath, msg, password)
        return send_file(encrypted_filepath, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    print("Decrypt route hit")
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(f"Saving uploaded file to: {filepath}")
        file.save(filepath)
        
        if os.path.exists(filepath):
            print(f"File successfully saved at: {filepath}")
        else:
            print("File not saved successfully.")
        
        password = request.form['password']

        
        
        message = decrypt_image(filepath, password)
        print(message)
        return f'Decrypted message: {message}'

if __name__ == '__main__':
    #serve(app, host='127.0.0.1', port=6666)
    app.run(debug=True, port=5000)
