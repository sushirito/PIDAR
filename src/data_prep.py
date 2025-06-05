import sys
from pathlib import Path

def verify_inputs():
    # Importing config paths here to avoid circulars if config grows
    from config import TRAIN_DIR, VALID_DIR, DATA_YAML, TEST_IMAGES

    # Sanity check before kicking off any expensive ops
    required_paths = [TRAIN_DIR, VALID_DIR, DATA_YAML, TEST_IMAGES]
    missing_paths = [p for p in required_paths if not p.exists()]

    if missing_paths:
        print("Uh oh – we're missing some key input paths:")
        for path in missing_paths:
            print(f"   - {path}")
        print("Please check the input folder structure and try again.\n")
        sys.exit(1)  # exit in case not found for whatever reason

    print("All required input paths look good.")

if __name__ == "__main__":
    verify_inputs()