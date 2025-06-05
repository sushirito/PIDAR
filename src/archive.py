import shutil
import time
from pathlib import Path
from config import OUTPUTS_DIR

def archive_predictions():
    # Source for where YOLO puts its latest predictions
    source = OUTPUTS_DIR / "runs" / "detect" / "predict"

    if not source.exists():
        raise FileNotFoundError(f"No predictions found at: {source}")

    # Tag each archive with a timestamp (useful for debug)
    now = time.strftime("%Y%m%d-%H%M%S")
    archive_base = OUTPUTS_DIR / "archives"
    dest = archive_base / f"predict-{now}"

    archive_base.mkdir(parents=True, exist_ok=True)

    print(f"\nArchiving predictions...")
    print(f"From: {source}")
    print(f"To:   {dest}")

    try:
        shutil.copytree(source, dest, dirs_exist_ok=True)
        print("Archive complete.")
    except Exception as err:
        print(f"Archive failed: {err}")

if __name__ == "__main__":
    archive_predictions()