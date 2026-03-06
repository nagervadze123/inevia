from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from app.core.config import settings


class StorageService(ABC):
    @abstractmethod
    def write_text(self, project_id: int, asset_type: str, ext: str, content: str) -> str:
        raise NotImplementedError


class LocalStorage(StorageService):
    def __init__(self, root: str | None = None):
        self.root = Path(root or settings.storage_root)

    def write_text(self, project_id: int, asset_type: str, ext: str, content: str) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        folder = self.root / str(project_id) / asset_type
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / f"{ts}.{ext}"
        file_path.write_text(content)
        return str(file_path)
