from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from process_image import *

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin (pour React)




UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    print('upload_image running')
    
    # Vérifier si un fichier est présent
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "Nom de fichier invalide"}), 400

    # Sauvegarder l'image
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Traiter l'image avec process_image.py
    try:
        result = process_image(file_path)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)  # Supprimer l'image après traitement

if __name__ == '__main__':
    app.run(debug=True)
