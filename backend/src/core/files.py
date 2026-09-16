import os
from pathlib import Path

BASE_DIR = Path(os.getcwd()).resolve()
SRC_DIR = BASE_DIR / "src"

TEMP_DIR = SRC_DIR / "temp"
QUE_DIR =  TEMP_DIR / "que"
JOBS_DIR = TEMP_DIR / "jobs"
FINISHED_DIR =  TEMP_DIR / "finished"
