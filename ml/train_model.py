"""
=============================================================
  ML Sales Classification System - Training Script
  Klasifikasi produk: Laris / Tidak
  Input: jumlah_penjualan, harga, diskon
  Output: status (Laris=1 / Tidak=0)
=============================================================
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


# ============================================================
# 1. LOAD DATA
# ============================================================
def load_data(filepath):
    """Membaca dataset CSV."""
    print("=" * 60)
    print("1. LOAD DATA")
    print("=" * 60)

    df = pd.read_csv(filepath)

    print(f"   Dataset berhasil dimuat: {filepath}")
    print(f"   Jumlah baris : {df.shape[0]}")
    print(f"   Jumlah kolom : {df.shape[1]}")
    print(f"\n   Kolom: {list(df.columns)}")
    print(f"\n   5 data pertama:")
    print(df.head().to_string(index=False))

    return df


# ============================================================
# 2. PREPROCESSING
# ============================================================
def preprocess_data(df):
    """
    Preprocessing data:
    - Cek missing values
    - Pilih fitur input & target
    - Encode target label
    - Feature scaling
    - Split train/test
    """
    print("\n" + "=" * 60)
    print("2. PREPROCESSING")
    print("=" * 60)

    # --- Cek info dataset ---
    print("\n   [Info Dataset]")
    print(f"   Tipe data:")
    for col in df.columns:
        print(f"     - {col}: {df[col].dtype}")

    # --- Cek missing values ---
    missing = df.isnull().sum()
    print(f"\n   [Missing Values]")
    if missing.sum() == 0:
        print("   ✅ Tidak ada missing values")
    else:
        print(missing[missing > 0])

    # --- Cek duplikat ---
    duplicates = df.duplicated().sum()
    print(f"\n   [Duplikat]")
    print(f"   Jumlah baris duplikat: {duplicates}")

    # --- Distribusi target ---
    print(f"\n   [Distribusi Target (status)]")
    status_counts = df["status"].value_counts()
    for status, count in status_counts.items():
        pct = count / len(df) * 100
        print(f"     {status}: {count} ({pct:.1f}%)")

    # --- Statistik deskriptif fitur input ---
    features = ["jumlah_penjualan", "harga", "diskon"]
    print(f"\n   [Statistik Deskriptif]")
    print(df[features].describe().to_string())

    # --- Pilih fitur & target ---
    X = df[features].copy()
    y = df["status"].copy()

    # --- Encode target: Laris=0, Tidak=1 (alphabetical) ---
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    print(f"\n   [Label Encoding]")
    print(f"   Mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # --- Feature Scaling (StandardScaler) ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"\n   [Feature Scaling]")
    print(f"   StandardScaler diterapkan pada fitur: {features}")

    # --- Split data: 80% train, 20% test ---
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    print(f"\n   [Split Data]")
    print(f"   Training set : {X_train.shape[0]} sampel")
    print(f"   Testing set  : {X_test.shape[0]} sampel")

    return X_train, X_test, y_train, y_test, scaler, le, features


# ============================================================
# 3. TRAINING MODEL
# ============================================================
def train_model(X_train, y_train):
    """Melatih model Random Forest."""
    print("\n" + "=" * 60)
    print("3. TRAINING MODEL")
    print("=" * 60)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    print(f"\n   🔄 Training Random Forest...")
    model.fit(X_train, y_train)
    print(f"   ✅ Random Forest selesai dilatih")

    return model


# ============================================================
# 4. EVALUASI
# ============================================================
def evaluate_model(model, X_test, y_test, le, features):
    """Evaluasi model dengan accuracy, classification report, confusion matrix."""
    print("\n" + "=" * 60)
    print("4. EVALUASI MODEL")
    print("=" * 60)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\n   {'─' * 50}")
    print(f"   📊 Random Forest")
    print(f"   {'─' * 50}")
    print(f"   Accuracy: {acc:.4f} ({acc * 100:.2f}%)")

    print(f"\n   Classification Report:")
    report = classification_report(y_test, y_pred, target_names=le.classes_, digits=4)
    for line in report.split("\n"):
        print(f"   {line}")

    print(f"\n   Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                 Predicted")
    print(f"                 {'Laris':>8} {'Tidak':>8}")
    print(f"   Actual Laris  {cm[0][0]:>8} {cm[0][1]:>8}")
    print(f"   Actual Tidak  {cm[1][0]:>8} {cm[1][1]:>8}")

    # --- Feature Importance ---
    importances = model.feature_importances_
    print(f"\n   {'─' * 50}")
    print(f"   🌲 Feature Importance")
    print(f"   {'─' * 50}")
    for feat, imp in sorted(
        zip(features, importances), key=lambda x: x[1], reverse=True
    ):
        bar = "█" * int(imp * 40)
        print(f"   {feat:>20}: {imp:.4f} {bar}")

    return acc


# ============================================================
# 5. SIMPAN MODEL
# ============================================================
def save_model(model, scaler, output_dir):
    """Simpan model dan scaler menggunakan joblib."""
    print("\n" + "=" * 60)
    print("5. SIMPAN MODEL")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(output_dir, "sales_model.pkl")
    scaler_path = os.path.join(output_dir, "scaler.pkl")

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    print(f"\n   ✅ Model (Random Forest) disimpan ke: {model_path}")
    print(f"   ✅ Scaler disimpan ke: {scaler_path}")
    print(f"   📁 Ukuran model : {os.path.getsize(model_path) / 1024:.1f} KB")
    print(f"   📁 Ukuran scaler: {os.path.getsize(scaler_path) / 1024:.1f} KB")

    return model_path, scaler_path


# ============================================================
# MAIN
# ============================================================
def main():
    print("\n" + "🚀" * 30)
    print("  MINI AI SALES PREDICTION SYSTEM")
    print("  Klasifikasi: Laris / Tidak")
    print("🚀" * 30 + "\n")

    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "sales_data.csv")
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

    # Pipeline
    df = load_data(data_path)
    X_train, X_test, y_train, y_test, scaler, le, features = preprocess_data(df)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test, le, features)
    save_model(model, scaler, model_dir)

    print("\n" + "=" * 60)
    print("✅ SELESAI! Pipeline ML berhasil dijalankan.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
