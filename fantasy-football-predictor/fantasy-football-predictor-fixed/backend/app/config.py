from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
MODEL_DIR = DATA_DIR / "models"
EXPORT_DIR = DATA_DIR / "exports"

FIRST_SEASON = 2018
POSITIONS = ("QB", "RB", "WR", "TE")

for directory in (CACHE_DIR, MODEL_DIR, EXPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
