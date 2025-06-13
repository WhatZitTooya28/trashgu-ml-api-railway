# app.py (File ini akan diunggah ke Railway.app untuk ML API - VERSI DUMMY)
from flask import Flask, request, jsonify
# from PIL import Image # Tidak perlu lagi jika tidak memproses gambar
import numpy as np # Masih bisa digunakan untuk random choice
# import io # Tidak perlu lagi
# import os # Tidak perlu lagi
# import tensorflow as tf # PENTING: Ini dihapus!

app = Flask(__name__)

# Model loading dan konfigurasi lainnya Dihapus untuk versi dummy
# MODEL_PATH = "best_model.keras" 
# model = None
# try:
#     if os.path.exists(MODEL_PATH):
#         model = tf.keras.models.load_model(MODEL_PATH, compile=False)
#         print(f"Model '{MODEL_PATH}' berhasil dimuat!")
#     else:
#         print(f"ERROR: File model tidak ditemukan di '{MODEL_PATH}'. API akan menggunakan dummy logic.")
#         model = None 
# except Exception as e:
#     print(f"ERROR: Gagal memuat model dari '{MODEL_PATH}': {e}. API akan menggunakan dummy logic.")
#     model = None

# Konfigurasi Label dan Saran Penanganan Sampah (Tetap digunakan untuk output dummy yang konsisten)
CLASS_LABELS = ['battery', 'biological', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic', 'shoes', 'trash']
# IMG_SIZE = (150, 150) # Tidak perlu lagi

# Endpoint utama untuk mengecek API status
@app.route("/", methods=["GET"])
def home():
    return "TrashGu ML API on Railway is running! (Dummy Mode)"

# Endpoint untuk klasifikasi gambar (mengembalikan hasil dummy)
@app.route("/classify", methods=["POST"])
def classify_image():
    # Tidak perlu memproses gambar atau memuat model
    # Cukup kembalikan respons dummy
    
    # Anda bisa membuat logika dummy yang lebih kompleks jika mau,
    # misalnya mengembalikan hasil random dari CLASS_LABELS
    predicted_label = np.random.choice(CLASS_LABELS) # Pilih random dari kelas yang ada
    # Atau bisa juga hardcode satu jenis sampah saja:
    # predicted_label = "plastic" 
    
    confidence = np.random.uniform(0.5, 0.99) # Confidence random
    is_anomaly = False # Selalu False untuk dummy
    anomaly_score = 0.0

    print(f"DEBUG: Returning dummy prediction: {predicted_label}") # Cetak di log Railway

    return jsonify({
        "prediction": predicted_label,
        "confidence": float(confidence),
        "is_anomaly": is_anomaly,
        "anomaly_score": float(anomaly_score)
    }), 200
