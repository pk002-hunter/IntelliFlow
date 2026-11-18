import os
from pathlib import Path
from PIL import Image

def scan_for_corrupted_images(dataset_path):
    # Supported image extensions
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    path = Path(dataset_path)
    corrupted_count = 0
    
    print(f"Scanning images in: {path.absolute()}...\n")
    
    for img_path in path.rglob("*"):
        if img_path.suffix.lower() in valid_exts:
            try:
                with Image.open(img_path) as img:
                    img.verify() # Check file integrity
            except Exception as e:
                print(f"[CORRUPTED] {img_path} -> Error: {e}")
                corrupted_count += 1

    print(f"\nScan finished. Total corrupted/invalid images found: {corrupted_count}")

if __name__ == '__main__':
    base = Path(__file__).resolve().parent / "IDDDetectionsYOLODataset"
    for split in ["train", "val"]:
        img_folder = base / split / "images"
        if img_folder.exists():
            scan_for_corrupted_images(img_folder)
