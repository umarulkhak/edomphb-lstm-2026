# EDOM PHB

Portal evaluasi dosen Politeknik Harapan Bersama dengan klasifikasi sentimen berbasis LSTM.

**Versi aplikasi: 2026.1.0**

## Fitur

- Autentikasi mahasiswa dan administrator.
- Pengiriman evaluasi dosen dan klasifikasi sentimen.
- Dashboard ringkasan serta pengelolaan akun dan data EDOM.
- Rekap evaluasi yang dapat difilter per dosen dan diekspor.

## Pratinjau aplikasi

<p align="center">
  <img src="ss/2026-dashboard.png" alt="Dashboard administrator EDOM dengan ringkasan empat sentimen" width="49%">
  <img src="ss/2026-analytics.png" alt="Analitik evaluasi EDOM dengan grafik distribusi sentimen" width="49%">
</p>

Screenshot memakai database demo terisolasi dengan 48 evaluasi simulasi: 12 untuk setiap kategori sentimen. Data tersebut hanya untuk pratinjau dan tidak mengubah database lokal aplikasi.

## Menjalankan aplikasi

Proyek ini memakai Python 3.11 dan TensorFlow 2.15 agar dependensi memiliki wheel yang sesuai untuk Mac Apple Silicon. `requirements.txt` memilih paket `tensorflow-macos` pada Mac ARM, `tensorflow` pada Mac Intel, dan `tensorflow-cpu` pada sistem lain.

```bash
uv python install 3.11
uv venv --python 3.11 .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Aktifkan environment yang sudah dibuat dengan perintah sesuai shell Anda sebelum menjalankan aplikasi.

Untuk pengembangan lokal:

```bash
python run.py
```

Buka `http://127.0.0.1:5000/`. Database SQLite dibuat pada penggunaan pertama.

Untuk membuat akun administrator, jalankan perintah berikut dari folder proyek. Username, email, dan kata sandi akan diminta secara interaktif; kata sandi tidak disimpan di source code:

```bash
.venv/bin/flask --app run.py create-admin
```

Di Windows, gunakan `.venv\Scripts\flask --app run.py create-admin`. Masuk melalui halaman `/login` dengan username dan kata sandi admin yang dibuat. Pendaftaran publik tetap hanya membuat akun mahasiswa.

## Konfigurasi produksi

Jangan gunakan konfigurasi pengembangan di internet publik. Produksi memerlukan secret key sendiri dan database PostgreSQL:

```bash
export APPSEED_CONFIG_MODE=Production
export SECRET_KEY='gunakan-secret-random-yang-panjang'
export DATABASE_URL='postgresql://user:password@host:5432/edomphb'
# Alternatif: APPSEED_DATABASE_USER/PASSWORD/HOST/PORT/NAME
export APPSEED_DATABASE_USER='...'
export APPSEED_DATABASE_PASSWORD='...'
export APPSEED_DATABASE_HOST='...'
export APPSEED_DATABASE_PORT='5432'
export APPSEED_DATABASE_NAME='...'
```

`SECRET_KEY` wajib diatur untuk mode produksi. Gunakan pengelola rahasia deployment; jangan menyimpan nilai rahasia di repository.

## Struktur aplikasi

```text
app/
  base/
    auth_routes.py          # autentikasi dan pendaftaran
    admin_routes.py         # pengelolaan data dan rekap
    evaluation_routes.py    # alur pengiriman dan analisis ulasan
    services/edom.py        # aturan dosen dan inferensi LSTM
    models.py               # model SQLAlchemy
  home/
    routes.py               # dashboard dan halaman aplikasi
  extensions.py             # ekstensi Flask bersama
```

Artefak tokenizer dan model tersimpan di `app/base/tokenizer1.pickle` dan `app/base/best_model.h5`. Dataset pelatihan dan notebook penelitian tersedia di folder `dataset/` dan `model/`.
