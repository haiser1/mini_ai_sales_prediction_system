# Backend - Mini AI Sales Prediction System

Bagian ini berisi kode REST API yang dibangun menggunakan **FastAPI**, **SQLAlchemy**, dan **PostgreSQL**. Service backend ini melayani autentikasi pengguna, manajemen data penjualan, serta menyediakan endpoint integrasi untuk model Machine Learning.

## 📁 Struktur Direktori Backend

```text
backend/
├── .env                    # Environment variables (local)
├── alembic                 # Konfigurasi tool navigasi migrasi database
│   ├── env.py              # Environment eksekusi alembic
│   └── versions/           # Script versi migrasi yang di-generate Alembic
├── alembic.ini             # Konfigurasi utilitas utama Alembic
├── app                     # Kode sumber aplikasi utama
│   ├── api                 # Routing API (Entry point Controller)
│   │   ├── main_router.py
│   │   └── routes/         # Endpoint per-domain (auth, predict, sales, user)
│   ├── core                # Konfigurasi (Database, App Config, Dependencies)
│   ├── helper              # Utility (Response builder, hashing, token, logger)
│   ├── models              # Model tabel SQLAlchemy (sales_data, user)
│   ├── schemas             # Pydantic schema (Validasi Request/Response payload)
│   └── services            # Layer Business Logic
├── main.py                 # File entry point untuk server FastAPI
├── requirements.txt        # Daftar dependency library Python (Pip)
└── scripts/
    └── seed_sales_data.py  # Script untuk membaca CSV & seeding data awal ke PostgreSQL
```

## 🚀 Instalasi & Menjalankan

Lihat dokumentasi instalasi lengkap di [README.md utama](../README.md).
