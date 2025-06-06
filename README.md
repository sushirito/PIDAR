# PIDAR

# YOLOv8 Marine Debris Detection Pipeline

## Publication

View the original publication “Tackling Marine Pollution with IoT and Conditioned Diffusion” at the [2024 IEEE International Conference on Artificial Intelligence in Engineering and Technology (IICAIET)](https://ieeexplore.ieee.org/document/10730236).

## Overview

Marine plastic debris—especially disposable masks—poses severe environmental and health risks worldwide. Collecting real‐world underwater imagery at scale is expensive and limited by geography. This repository provides a self‐contained YOLOv8 pipeline designed to train and deploy a high‐precision mask detector (PiDAR) on cost‐effective hardware. It includes:

1. **A Dataset Preparation Module** that uses publicly shared train/validation/test splits (Google Drive links below) in YOLOv8 format.  
2. **A Training Module** that iterates over three learning rates (1e-3, 5e-4, 1e-4) for 100 epochs each, saving the best model at each step.  
3. **An Inference Module** that runs the final “best.pt” model on a test folder of marine images.  
4. **An Archiving Module** that collects YOLOv8’s prediction outputs under a timestamped folder.

Together, these modules replicate the functionality described in the PiDAR paper—training a YOLOv8 Small model to detect marine masks in under 40 ms per image, achieving mAP > 0.99 on held‐out test images. This repository represents the second portion of our publication's full code; refer to PROMPTCUE for part 1. 

---

## Project Structure

```

yolo\_pipeline/
├── inputs/                    ← User‐provided data and config
│   ├── train/                 ← YOLOv8 “train” set (images + labels)
│   ├── valid/                 ← YOLOv8 “valid” set (images + labels)
│   ├── test\_images/           ← Images for inference (no labels)
│   └── data.yaml              ← YOLOv8 data configuration file
│
├── outputs/                   ← Pipeline outputs
│   ├── runs/                  ← YOLOv8’s default “runs/” folder
│   │   ├── train/             ← Training logs & weights (one subfolder per run)
│   │   └── detect/            ← Inference outputs (“predict” folder)
│   └── archives/              ← Archived prediction folders (timestamped)
│
├── requirements.txt           ← Python dependencies
├── setup.sh                   ← Installs Ultralytics and other requirements
│
└── src/                       ← All Python source modules
├── config.py              ← Configuration constants (paths, hyperparameters)
├── data\_prep.py           ← Verifies that inputs/ exists and is correctly structured
├── train.py               ← Trains YOLOv8 over multiple learning rates
├── predict.py             ← Runs YOLOv8 inference on test\_images/
├── archive.py             ← Archives “runs/detect/predict” outputs with timestamp
└── main.py                ← Top‐level CLI: verify → train → predict → archive
```


---

## Usage Instructions

### 1. Installation & Setup

1. **Clone this repository** and enter its root directory:
   ```bash
   git clone https://github.com/YourUsername/yolo_pipeline.git
   cd yolo_pipeline
   chmod +x setup.sh
   ```

2. **Run the setup script** to install all necessary Python packages:

   ```bash
   ./setup.sh
   ```

   This installs:

   * Ultralytics YOLOv8
   * Any standard Python libraries required by `src/` (e.g., `pathlib`, `shutil`)

3. **Verify** that the following directories and files exist under `inputs/`. If any are missing, download from the links below or place your own data:

   ```bash
   inputs/
     ├── train/
     │   ├── images/        ← .jpg/.png images for training
     │   └── labels/        ← .txt label files in YOLO format
     ├── valid/
     │   ├── images/        ← .jpg/.png images for validation
     │   └── labels/        ← .txt label files in YOLO format
     ├── test_images/       ← .jpg/.png images for inference only
     └── data.yaml          ← YOLOv8 data config (train/val paths, class names)
   ```

   * **Download train set** from Google Drive:
     [Train → Google Drive](https://drive.google.com/drive/folders/1fErsPCi7UASJrSuxosGLnIFeCPb--VzM?usp=drive_link)
   * **Download valid set** from Google Drive:
     [Valid → Google Drive](https://drive.google.com/drive/folders/1f5s3s8z3G5Eu6PEMOGmkzvlquQr64Cni?usp=drive_link)
   * **Download test images** folder (.zip or folder):
     [Test → Google Drive](https://drive.google.com/file/d/1f1ZECFgroGN6-KvksDqGCRXQG1MxeNds/view?usp=drive_link)
   * **Download data.yaml** configuration:
     [data.yaml → Google Drive](https://drive.google.com/file/d/1f1ZECFgroGN6-KvksDqGCRXQG1MxeNds/view?usp=drive_link)

4. **Edit** `inputs/data.yaml` if you use a different path or class names. It should follow this format:

   ```yaml
   train: inputs/train
   val:   inputs/valid

   nc: 1
   names: ['mask']
   ```

---

### 2. Data Verification

Before training, verify that all required input paths exist and are correctly structured:

```bash
python -m src.data_prep
```

If any path is missing (e.g., `inputs/train/`, `inputs/valid/`, `inputs/data.yaml`, or `inputs/test_images/`), the script will exit with an error listing the missing paths.

---

### 3. Training

Train YOLOv8 detection models over three learning rates (1e-3, 5e-4, 1e-4) for 100 epochs each. The “best.pt” checkpoint for each LR is saved under:

```
runs/train/test1/lr=<learning_rate>/weights/best.pt
```

```bash
python -m src.train
```

**What happens**:

* For each `lr` in `[1e-3, 5e-4, 1e-4]`, YOLOv8 trains:

  ```bash
  yolo task=detect mode=train model=yolov8s.pt \
       data=inputs/data.yaml optimizer=Adam epochs=100 \
       imgsz=1280 lr0=<lr> name=test1/lr=<lr>
  ```
* Training logs, tensorboard files, and weights are stored in:

  ```
  runs/train/test1/lr=<lr>/
  ```

You can monitor training progress in real time by inspecting the `runs/train/` folder or using the Ultralytics TensorBoard integration.

---

### 4. Inference

Once training completes, run inference on the test images using the “best.pt” model from the final learning rate (1e-4). By default, YOLOv8 saves detection results under:

```
runs/detect/predict/
```

```bash
python -m src.predict
```

**What happens**:

* Identifies:

  ```
  runs/train/test1/lr=1e-4/weights/best.pt
  ```
* Runs:

  ```bash
  yolo task=detect mode=predict \
       model=runs/train/test1/lr=1e-4/weights/best.pt \
       conf=0.20 iou=0.10 \
       source=inputs/test_images
  ```
* Saves predicted images with bounding boxes under:

  ```
  runs/detect/predict/
  ```

---

### 5. Archiving Predictions

After inference, archive the entire `runs/detect/predict/` folder to a timestamped subdirectory under `outputs/archives/`. For example:

```
outputs/archives/predict-20240605-153012/
```

```bash
python -m src.archive
```

This command will copy:

```
runs/detect/predict/ → outputs/archives/predict-<YYYYMMDD-HHMMSS>/
```

---

### 6. Full Pipeline

To run the entire pipeline end-to-end (verify inputs → train → predict → archive), execute:

```bash
python -m src.main
```

You will see console logs for each stage. If any step fails (e.g., missing data or training error), the script will exit with an error message.

---

## Directory Conventions

* **`inputs/`**:

  * `train/images/` and `train/labels/` – YOLOv8 training data
  * `valid/images/` and `valid/labels/` – YOLOv8 validation data
  * `test_images/` – Inference‐only images (no labels)
  * `data.yaml` – YOLOv8 config (train/val paths, number of classes, class names)

* **`outputs/`**:

  * `runs/train/` – YOLOv8 training logs, checkpoints, and metrics
  * `runs/detect/predict/` – YOLOv8 inference results (images with bounding boxes)
  * `archives/` – Timestamped archives of prediction outputs

* **`src/`**:

  * `config.py` – All constants (paths, hyperparameters)
  * `data_prep.py` – Verifies presence of `inputs/` data
  * `train.py` – Automates YOLOv8 training over multiple learning rates
  * `predict.py` – Automates YOLOv8 inference with the final model
  * `archive.py` – Archives detection outputs under `outputs/archives/`
  * `main.py` – High-level orchestrator combining all steps
---

## Citation

If you use this pipeline for research or deployment, please cite:

```bibtex
@inproceedings{shivakumar2024tackling,
  title={Tackling Marine Pollution with IoT and Conditioned Diffusion},
  author={Shivakumar, Aditya},
  booktitle={2024 IEEE International Conference on Artificial Intelligence in Engineering and Technology (IICAIET)},
  pages={142--146},
  year={2024},
  organization={IEEE}
}
```
