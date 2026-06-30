import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.api.deps import get_db
from app.core.database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

class BaseTestCase(unittest.TestCase):
    client: TestClient

    @classmethod
    def setUpClass(cls):
        # Setup DB & Override dijalankan sekali untuk kelas yang mewarisinya
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Bersihkan DB setelah semua test di dalam kelas selesai
        Base.metadata.drop_all(bind=engine)
        app.dependency_overrides.clear()