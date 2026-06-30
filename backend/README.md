
# Technical Test Backend - FastAPI

Aplikasi backend berbasis FastAPI dan SQLAlchemy.

## Prasyarat
- Python 3.14+
- PostgreSQL (Sudah membuat database bernama `GLI`)

## Library

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest

## Cara Menjalankan Proyek

Sebelum memilih salah satu opsi di bawah, pastikan terminal sudah masuk ke folder backend:

```
cd backend
```
### Install Requirements
```
pip install -r requirments.txt
```
## Migrasi Database (Alembic)

### 1. Menjalankan Migrasi ke Database
```bash
python -m alembic upgrade head
```

### 2. Membuat Migrasi Baru Refresh
```bash
python -m alembic revision --autogenerate -m "Deskripsi perubahan"
```

### 3. Menghapus Migrasi
```bash
python -m alembic downgrade -1
```

### Jalankan Aplikasi Lokal
```
python -m uvicorn app.main:app --reload
```

### menjalankan test
```
python -m pytest
```

### Akses Aplikasi
- Base URL: http://127.0.0.1:8000
- Dokumentasi Swagger API: http://127.0.0.1:8000/docs


