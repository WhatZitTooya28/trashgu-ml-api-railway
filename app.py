    # app.py (File ini akan diunggah ke Railway.app untuk ML API)
    from flask import Flask, request, jsonify
    from PIL import Image
    import numpy as np
    import io
    import os
    import tensorflow as tf # Import tensorflow di sini karena model ML akan dijalankan di sini

    app = Flask(__name__)

    # PATH MODEL ANDA DI RAILWAY.APP
    # Asumsikan 'best_model.keras' berada di root direktori proyek Anda di Railway
    MODEL_PATH = "best_model.keras" 

    # Inisialisasi model di luar endpoint untuk efisiensi
    model = None

    # Muat model saat aplikasi Flask ini dimulai
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print(f"Model '{MODEL_PATH}' berhasil dimuat!")
        else:
            print(f"ERROR: File model tidak ditemukan di '{MODEL_PATH}'. API tidak akan berfungsi.")
            model = None 
    except Exception as e:
        print(f"ERROR: Gagal memuat model dari '{MODEL_PATH}': {e}. API tidak akan berfungsi.")
        model = None

    # Konfigurasi Label dan Ukuran Gambar (HARUS SAMA DENGAN SAAT PELATIHAN MODEL)
    CLASS_LABELS = ['battery', 'biological', 'cardboard', 'clothes', 'glass', 'metal', 'paper', 'plastic', 'shoes', 'trash']
    IMG_SIZE = (150, 150) # Ukuran gambar yang diharapkan oleh model Anda

    # Fungsi untuk preprocessing gambar
    def preprocess_image(image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0 # Normalisasi
        return np.expand_dims(img_array, axis=0) # Tambah dimensi batch

    # Endpoint utama untuk mengecek API status
    @app.route("/", methods=["GET"])
    def home():
        return "TrashGu ML API on Railway is running!"

    # Endpoint untuk klasifikasi gambar
    @app.route("/classify", methods=["POST"])
    def classify_image():
        if model is None:
            return jsonify({"error": "Model ML belum dimuat. Mohon cek log Railway."}), 500

        if 'image' not in request.files:
            return jsonify({"error": "Tidak ada file gambar yang disediakan."}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()

        try:
            processed_image = preprocess_image(image_bytes)
        except Exception as e:
            app.logger.error(f"Gagal melakukan preprocessing gambar: {e}")
            return jsonify({"error": f"Gagal melakukan preprocessing gambar: {e}"}), 400

        # --- Bagian Deteksi Anomali (Opsional, jika ada Autoencoder) ---
        is_anomaly = False
        anomaly_score = 0.0
        # Jika terdeteksi anomali (kode anomali diimplementasikan), berikan respons anomali
        if is_anomaly:
            return jsonify({
                "prediction": "TIDAK_DIKETAHUI",
                "confidence": 0.0,
                "is_anomaly": True,
                "anomaly_score": anomaly_score
            }), 200

        # --- Klasifikasi Sampah Menggunakan Model ---
        try:
            predictions = model.predict(processed_image)
            pred_array = predictions[0] if isinstance(predictions, np.ndarray) and predictions.ndim > 1 else predictions 
            
            predicted_class_index = np.argmax(pred_array)
            predicted_label = CLASS_LABELS[predicted_class_index]
            confidence = float(pred_array[predicted_class_index])

            return jsonify({
                "prediction": predicted_label,
                "confidence": confidence,
                "is_anomaly": False,
                "anomaly_score": 0.0
            }), 200

        except Exception as e:
            app.logger.error(f"Gagal melakukan inferensi model: {e}")
            return jsonify({"error": f"Gagal melakukan inferensi model: {e}"}), 500

    # Tidak perlu blok if __name__ == "__main__": saat menggunakan Gunicorn/CMD di Dockerfile
    