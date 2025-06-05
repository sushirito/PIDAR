import subprocess
from pathlib import Path
from config import (
    RUN_ID, LEARNING_RATES, RUNS_DIR, TEST_IMAGES
)

def predict_with_best():
    # Pick the model from the final training run (assuming it's the best one for now)
    final_lr = LEARNING_RATES[-1]  # just grabbing the last one
    model_path = RUNS_DIR / "train" / RUN_ID / f"lr={final_lr}" / "weights" / "best.pt"

    if not model_path.exists():
        raise FileNotFoundError(f" Couldn't find the model at {model_path}")

    # YOLOv8 inference command. This should work if all paths and CLI are set up right
    cmd_parts = [
        "yolo",
        "task=detect",
        "mode=predict",
        f"model={model_path}",
        "conf=0.20",      # keeping the confidence threshold pretty low
        "iou=0.10",       # also a low IoU (might need tweaking depending on application)
        f"source={TEST_IMAGES}"
    ]

    # FYI: not using shlex.join here just to keep it readable in the print
    full_cmd = " ".join(cmd_parts)
    print(f"About to run inference with:\n{full_cmd}\n")

    # Run the command, assuming yolo is accessible in PATH
    subprocess.run(full_cmd, shell=True, check=True)

# Useful for quick testing
if __name__ == "__main__":
    predict_with_best()