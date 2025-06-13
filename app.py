# app.py (VERSI SANGAT MINIMAL UNTUK DEBUGGING DI RAILWAY.APP)
# Tujuan: Hanya untuk memastikan Flask itu sendiri bisa running di Railway

from flask import Flask, jsonify # Pastikan tidak ada indentasi di sini

app = Flask(__name__) # Pastikan tidak ada indentasi di sini, dan __name__ benar

@app.route("/", methods=["GET"])
def home():
    # Ini adalah endpoint dummy paling sederhana.
    return "Hello from Railway Flask API! (Minimal Version)"

# Tidak ada endpoint /classify di versi ini dulu
# Tidak ada import numpy, Pillow, tensorflow, io, os
# Tidak ada blok if __name__ == "__main__":
