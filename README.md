
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

---

## Menjalankan dengan Docker

Pastikan anda sudah menginstall docker dan docker compose di komputer anda.

1. **Jalankan Container**
   ```bash
   docker compose up --build -d
   ```

2. **Akses Aplikasi**
   - **Frontend:** [http://localhost](http://localhost) (Port 80)
   - **Backend API:** [http://localhost:8000](http://localhost:8000)
   - **Dokumentasi Swagger API:** [http://localhost:8000/docs](http://localhost:8000/docs)

3. **Menjalankan Unit Test di Container**
   Untuk menjalankan test suite backend di dalam container yang sedang berjalan:
   ```bash
   docker compose exec backend python -m pytest
   ```

4. **Menghentikan Aplikasi**
   Untuk menghentikan dan menghapus container serta network yang dibuat oleh docker compose:
   ```bash
   docker compose down
   ```

### Menjalankan dengan Podman

