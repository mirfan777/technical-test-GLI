
# Technical Test Backend - FastAPI

Aplikasi backend berbasis FastAPI dan SQLModel.

## Prasyarat
- Python 3.14+
- PostgreSQL (Sudah membuat database bernama `GLI`)

## Cara Menjalankan Proyek

Sebelum memilih salah satu opsi di bawah, pastikan terminal sudah masuk ke folder backend:

```
cd backend
```
### Install Requirements
```
pip install -r requirements.txt
```
### Jalankan Aplikasi Lokal
```
python -m uvicorn app.main:app --reload
```

### Akses Aplikasi
- Base URL: http://127.0.0.1:8000
- Dokumentasi Swagger API: http://127.0.0.1:8000/docs

