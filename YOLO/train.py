import os
import glob
import yaml
import torch
from ultralytics import YOLO

# ==============================================================================
# CONFIGURATION: YOUR UNZIPPED DATASET FOLDER NAME
# ==============================================================================
DATASET_DIR_NAME = "IDDDetectionsYOLODataset"

def configure_yaml(dataset_dir):
    """Locates and updates data.yaml with absolute paths for YOLO."""
    print("\nLocating and verifying data.yaml...")
    yaml_candidates = glob.glob(os.path.join(dataset_dir, '**', 'data.yaml'), recursive=True)
    if not yaml_candidates:
        raise FileNotFoundError(f"Could not find data.yaml inside '{dataset_dir}' directory! Make sure the folder structure is correct.")
    
    yaml_path = os.path.abspath(yaml_candidates[0])
    base_dir = os.path.dirname(yaml_path)

    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    # Clean up relative 'path' entry to prevent conflicting path concatenation
    data.pop('path', None)

    # Determine train and val image directories safely
    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'valid') if os.path.exists(os.path.join(base_dir, 'valid')) else os.path.join(base_dir, 'val')

    data['train'] = os.path.join(train_dir, 'images') if os.path.exists(os.path.join(train_dir, 'images')) else train_dir
    data['val'] = os.path.join(val_dir, 'images') if os.path.exists(os.path.join(val_dir, 'images')) else val_dir

    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
        
    print(f"✅ Updated paths in {yaml_path}:")
    print(f"  - train: {data['train']}")
    print(f"  - val:   {data['val']}")
    return yaml_path

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(current_dir, DATASET_DIR_NAME)

    # 1. Verify that the dataset folder actually exists
    if not os.path.isdir(dataset_dir):
        raise FileNotFoundError(f"Could not find folder '{DATASET_DIR_NAME}' in '{current_dir}'. Please ensure it is in the same directory as this script.")
    
    print(f"✅ Found dataset folder at: {dataset_dir}")

    # 2. Fix data.yaml paths
    yaml_path = configure_yaml(dataset_dir=dataset_dir)

    # 3. Check GPU Setup
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"\n🚀 NVIDIA GPU detected: {gpu_name}")
        device_arg = 0
    else:
        print("\n⚠️ CUDA is not detected! Training will run on CPU.")
        device_arg = 'cpu'

    # 4. Initialize YOLO model
    print("\nLoading base model...")
    model = YOLO('yolov8n.pt')

    # Project output directory
    save_dir = os.path.join(current_dir, 'runs')

    # 5. Train with RTX 4050-optimized settings
    print(f"\nStarting YOLO training...")
    results = model.train(
        resume=True,
        data=yaml_path,
        epochs=30,               # Adjust epochs as desired
        imgsz=640,               # Standard image resolution
        batch=16,                # Safe batch size for 6GB RTX 4050 VRAM
        device=device_arg,       # Dedicated GPU (RTX 4050)
        workers=0,               # Prevents Windows multiprocessing crashes
        plots=False,             # Fixes Windows access violation crash in plot_images thread at epoch 1
        exist_ok=True,           # Reuses folder instead of creating indian_driving_model-1, -2, etc.
        project=save_dir,
        name='indian_driving_model',
        save=True
    )

    print("\n✅ Training finished successfully!")
    save_run_dir = getattr(results, 'save_dir', os.path.join(save_dir, 'indian_driving_model'))
    best_weights = os.path.join(save_run_dir, 'weights', 'best.pt')
    print(f"Best weights saved at: {best_weights}")

# Windows multiprocessing guard
if __name__ == '__main__':
    train()
