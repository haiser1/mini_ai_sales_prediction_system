"""
=============================================================
  ML Sales Prediction - Load & Predict Script
  Memuat model yang sudah disimpan dan melakukan prediksi
=============================================================
"""

import os
import joblib


def load_model(model_dir=None):
    """Load model dan scaler dari file .pkl"""
    if model_dir is None:
        model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

    model_path = os.path.join(model_dir, "sales_model.pkl")
    scaler_path = os.path.join(model_dir, "scaler.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model tidak ditemukan di: {model_path}\n"
            "Jalankan train_model.py terlebih dahulu!"
        )

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    print(f"Model berhasil dimuat dari: {model_path}")
    print(f"Scaler berhasil dimuat dari: {scaler_path}")

    return model, scaler


def predict(model, scaler, jumlah_penjualan, harga, diskon):
    """
    Prediksi status produk (Laris / Tidak).

    Parameters:
        model: model ML yang sudah dilatih
        scaler: StandardScaler yang sudah di-fit
        jumlah_penjualan (int): jumlah unit terjual
        harga (int): harga produk
        diskon (int): persentase diskon (0-30)

    Returns:
        str: 'Laris' atau 'Tidak'
    """
    # Siapkan input
    import pandas as pd

    input_data = pd.DataFrame(
        [[jumlah_penjualan, harga, diskon]],
        columns=["jumlah_penjualan", "harga", "diskon"],
    )

    # Scaling
    input_scaled = scaler.transform(input_data)

    # Prediksi
    prediction = model.predict(input_scaled)

    # Decode: model di-train dengan LabelEncoder (Laris=0, Tidak=1) atau sebaliknya
    # Berdasarkan alphabetical order: Laris=0, Tidak=1
    label_map = {0: "Laris", 1: "Tidak"}
    result = label_map[prediction[0]]

    return result
