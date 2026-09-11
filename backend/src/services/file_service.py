import json
from pathlib import Path

def write_file(base: Path, file_name: str, data) -> Path:
    path = Path(base, file_name)
    path.write_text(data)
    return path

def read_file(base: Path, file_name: str) -> dict:
    path = Path(base, file_name)
    data = json.loads(path.read_text())
    return data

def rename_file(base: Path, file_name: str, new_file_name: str):
    file = Path(base, file_name)
    new_file = Path(base, new_file_name)
    return file.rename(new_file)


def clean_job(path):
    """Remove a file if it exists (used to clean up interim downloads)."""
    file = Path(path)
    if file.exists():
        file.unlink()
