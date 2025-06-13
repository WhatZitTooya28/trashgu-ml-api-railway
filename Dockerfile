    # Menggunakan base image Python
    FROM python:3.9-slim-buster

    # Mengatur working directory di dalam container
    WORKDIR /app

    # Menyalin requirements.txt
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Menyalin seluruh aplikasi (termasuk app.py dan best_model.keras)
    COPY . .

    # Mengekspos port 5000
    EXPOSE 5000

    # Perintah untuk menjalankan aplikasi Flask menggunakan Gunicorn
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
    