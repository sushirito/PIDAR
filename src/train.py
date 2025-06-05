import subprocess
from pathlib import Path
from config import (
    TRAIN_DIR, VALID_DIR, DATA_YAML, 
    EPOCHS, IMG_SIZE, RUN_ID, LEARNING_RATES, RUNS_DIR
)

def train_all_lrs():
    # Make sure our output directory exists
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    for lr in LEARNING_RATES:
        run_label = f"{RUN_ID}/lr={lr}"
        
        # Assembling YOLO training command
        cmd_args = [
            "yolo",
            "task=detect",
            "mode=train",
            "model=yolov8s.pt",  # you can swap this out with bigger model depnding on usecase
            f"data={DATA_YAML}",
            "optimizer=Adam",    # went with Adam; could experiment later
            f"epochs={EPOCHS}",
            f"imgsz={IMG_SIZE}",
            f"lr0={lr}",         # hyperparameter we're sweeping
            f"name={run_label}"
        ]

        full_cmd = " ".join(cmd_args)
        print(f"\n--- Training with lr={lr} ---")
        print(f"Command: {full_cmd}\n")

        # Running the training command
        try:
            subprocess.run(full_cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Training failed for lr={lr} \nDetails: {e}\n")
            continue

if __name__ == "__main__":
    train_all_lrs()