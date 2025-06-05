import os
from pathlib import Path

# === Project Directory Setup ===

# Base directory of this project (assuming this script lives under /src or similar)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# === Input Paths ===

# Main input folder (expected structure: train/, valid/, test_images/, etc.)
INPUTS_DIR = PROJECT_ROOT / "inputs"

TRAIN_DIR = INPUTS_DIR / "train"          # should contain train/images and train/labels
VALID_DIR = INPUTS_DIR / "valid"          # same structure as train
TEST_IMAGES = INPUTS_DIR / "test_images"  # just images here, no labels needed

# YOLOv8 config YAML file
DATA_YAML = INPUTS_DIR / "data.yaml"

# === Output Paths ===

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
RUNS_DIR = OUTPUTS_DIR / "runs"

# === Training Config ===

EPOCHS = 100
IMG_SIZE = 1280  # make sure your GPU can handle this resolution

# A unique identifier for this batch of experiments
RUN_ID = "test1"  # change this when rerunning to avoid overwriting results

# Try a few learning rates – sweep manually for now
LEARNING_RATES = [1e-3, 5e-4, 1e-4]

# NOTE: After training, YOLOv8 will save best.pt under:
#       outputs/runs/train/<RUN_ID>/lr=<lr>/weights/best.pt
