# Frontend - Mini AI Sales Prediction System

Bagian ini berisi aplikasi antarmuka pengguna (Frontend) yang dibangun menggunakan **React**, **Vite**, **Tailwind CSS v4**, dan **DaisyUI v5**. Aplikasi web ini memungkinkan pengguna untuk melakukan login, melihat dan memfilter data penjualan, serta mencoba untuk memprediksi hasil penjualan berbasis model Machine Learning yang telah ditambahkan.

## 📁 Struktur Direktori Frontend

```text
frontend/
├── public                  # Aset publik statis
│   ├── favicon.svg         # Ikon tab aplikasi
│   └── icons.svg           # File SVG untuk asset visual tambahan
├── src                     # Direktori utama kode sumber React
│   ├── api                 # Konfigurasi komunikasi ke API backend
│   │   └── axios.js        # Konfigurasi instansiasi Axios (Custom Headers & Base URL)
│   ├── components          # Komponen React yang dapat digunakan ulang (Re-usable UX)
│   │   ├── Layout.jsx      # Navigation Bar, Struktur Layout Umum, dan Sidebar
│   │   └── ProtectedRoute.jsx  # Router Guard (Proteksi Halaman berdasarkan status Auth)
│   ├── pages               # Halaman utama aplikasi (Views)
│   │   ├── LoginPage.jsx   # Form Login Pengguna
│   │   ├── RegisterPage.jsx# Form Registrasi Pengguna
│   │   ├── PredictPage.jsx # Halaman Prediksi Status Barang menggunakan model AI ML
│   │   ├── SalesPage.jsx   # Landing page Dashboard Penjualan (Tabel dan Filter)
│   │   └── ProfilePage.jsx # Halaman Detail dan Update Profile Pengguna
│   ├── store               # Global State Management menggunakan Zustand
│   │   └── authStore.js    # Menyimpan status Autentikasi dan Identitas User
│   ├── assets              # Gambar, ilustrasi, media internal aplikasi
│   ├── index.css           # Styling utama CSS (Konfigurasi Tailwind)
│   ├── App.jsx             # Entry Point Router dan Komponen Utama Aplikasi
│   └── main.jsx            # Rendering root React ke DOM index.html
├── .env                    # Environment variables frontend (local)
├── index.html              # Template HTML dasar dari SPA React Vite
├── package.json            # Manifest file yang menyimpan daftar Library Frontend
└── vite.config.js          # Konfigurasi module bundler (Vite) beserta Tailwind Plugin
```

## 🚀 Instalasi & Menjalankan

Lihat dokumentasi instalasi lengkap di [README.md utama](../README.md).
