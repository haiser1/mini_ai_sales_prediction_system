# Mini AI Sales Prediction System

## 📖 Deskripsi Singkat
Proyek ini adalah sistem prediksi penjualan berbasis web yang menggunakan Artificial Intelligence (Machine Learning) untuk memprediksi apakah suatu produk akan "Laris" atau "Tidak Laris" berdasarkan input jumlah penjualan, harga produk, dan persentase diskon. 

Sistem ini bersifat Full-Stack dan terdiri dari aplikasi frontend modern, API backend yang efisien, dan model prediktif yang terlatih.

---

## 🏗️ System Design & Architecture

```mermaid
graph TD
    %% Entities
    User((User))
    
    %% Frontend Components
    subgraph Frontend [React Frontend - Vite]
        UI[UI Components\nTailwind + DaisyUI]
        Zustand[State Management\nZustand]
        Axios[API Client\nAxios]
        
        UI <--> Zustand
        Zustand <--> Axios
    end
    
    %% Backend Components
    subgraph Backend [FastAPI Backend]
        Router[API Routers]
        Auth[Auth Service\nJWT]
        SalesSvc[Sales Service]
        PredSvc[Prediction Service]
        
        Router --> Auth
        Router --> SalesSvc
        Router --> PredSvc
    end
    
    %% ML & Database
    subgraph ML [Machine Learning Model]
        Model[(Random Forest Model\nScikit-learn)]
        Scaler[MinMaxScaler]
    end
    
    subgraph Database [PostgreSQL Database]
        DB[(PostgreSQL)]
    end
    
    %% Connections
    User -->|Interacts with| UI
    Axios -->|HTTP/REST| Router
    Auth -->|Queries/Validates| DB
    SalesSvc -->|Async Queries| DB
    PredSvc -->|Loads & Predicts| Model
    PredSvc -->|Scales Input| Scaler
```

---

## 💻 Tech Stack
- **Frontend**: React.js (Vite), Zustand (State Management), Tailwind CSS v4, DaisyUI v5, React Router DOM, Axios.
- **Backend**: FastAPI, SQLAlchemy (Async Queries), PostgreSQL (asyncpg), Pydantic, Passlib (bcrypt), PyJWT, Uvicorn.
- **Machine Learning**: Python, Scikit-Learn (RandomForestClassifier), Pandas, Joblib.
- **Infrastruktur / Environment**: Node.js (Frontend), Python 3.x+ (Backend & ML).

---

## 🚀 Cara Setup dan Menjalankan Proyek

Proyek ini terdiri dari lingkungan Backend dan Frontend. Pastikan Anda sudah menginstal **Python 3.10+**, **Node.js 20+**, dan instance **PostgreSQL** yang berjalan.

### 1. Clone Repository

```bash
git clone https://github.com/haiser1/mini_ai_sales_prediction_system.git
```

### 2. Setup Backend

Buka terminal dan masuk ke folder `backend`:
```bash
cd backend
```

**a. Buat dan aktifkan Virtual Environment:**
```bash
python -m venv venv
# Untuk Linux / macOS
source venv/bin/activate
# Untuk Windows
venv\Scripts\activate
```

**b. Buat Database:**
```bash
CREATE DATABASE sales_db;
```

**c. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**d. Konfigurasi Environment Variable:**
Pastikan file `.env` di folder `backend` sudah disesuaikan dengan koneksi database PostgreSQL Anda:
```env
LOG_LEVEL=INFO
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sales_db
SECRET_KEY=super-rahasia
```

**e. Jalankan Migrasi Database (Alembic):**
```bash
alembic upgrade head
```

**f. Seed Data Penjualan (Opsional):**
Anda bisa memasukkan sampel data penjualan awal ke dalam database.
```bash
python scripts/seed_sales_data.py
```

**g. Jalankan Server FastAPI:**
```bash
uvicorn app.main:app --reload
```
Backend akan berjalan di: `http://localhost:8000`.
Anda dapat melihat dokumentasi API (Swagger UI) di: `http://localhost:8000/docs`.


---

### 2. Setup Frontend

Buka tab terminal baru dan masuk ke folder `frontend`:
```bash
cd frontend
```

**a. Install Node Dependencies:**
```bash
npm install
```
*(Atau Anda bisa menggunakan manajer paket lain seperti `yarn` atau `pnpm`)*

**b. Konfigurasi Environment Frontend:**
Pastikan file `.env` (jika ada) terkonfigurasi ke API backend. Secara bawaan (default), Axios merujuk ke endpoint `http://localhost:8000/api`.

**c. Jalankan Development Server Vite:**
```bash
npm run dev
```
Frontend akan berjalan dan dapat diakses di browser pada: `http://localhost:5173`.

---

 ### 3. Train Model (Opsional)

 ```bash
cd ml

python -m venv venv

# Untuk Linux / macOS
source venv/bin/activate
# Untuk Windows
venv\Scripts\activate

python train_model.py
 ```

---

## 🎯 Fitur
1. **Autentikasi Pengguna**: Login & Register secara aman menggunakan JWT.
2. **Dashboard Data Penjualan**: Menampilkan data dengan fitur pagination, search, dan filter status (Laris / Tidak Laris).
3. **Prediksi Penjualan AI**: Memungkinkan staf / pengguna memprediksi status barang ("Laris" atau "Tidak Laris") melalui pengisian form dinamis yang di-hit langsung ke model ML.
4. **Manajemen Profil**: Pengguna dapat memperbarui nama lengkap akun mereka.
