import os
os.environ['DATABASE_URL'] = 'sqlite+pysqlite:///./test.db'
os.environ['STORAGE_ROOT'] = './test_data'

from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app

Base.metadata.create_all(bind=engine)


def get_client():
    return TestClient(app)
