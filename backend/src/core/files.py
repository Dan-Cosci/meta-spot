from pathlib import Path
import os

BASE_DIR = Path(os.getcwd()).resolve()
SRC_DIR = BASE_DIR / "src"

TEMP_DIR = SRC_DIR / "temp"
QUE_DIR =  TEMP_DIR / "que"
JOBS_DIR = TEMP_DIR / "jobs"
FINISHED_DIR =  TEMP_DIR / "finished"


if __name__ == "__main__":
    print("BASE:", BASE_DIR)
    print("QUE:", QUE_DIR)
    print("JOBS:", JOBS_DIR)
    print("FINISHED:", FINISHED_DIR)
