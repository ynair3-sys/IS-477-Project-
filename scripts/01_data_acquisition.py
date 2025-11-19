"""
Data Acquisition Script
Project: Sleep Patterns and Academic Performance
Authors: Yamuna Nair & Monisha Mudunuri
 
This script downloads the required datasets and verifies their integrity.
"""
 
import requests
import hashlib
import os
import pandas as pd
from pathlib import Path
 
# Create data directories if they don't exist
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)
 
def calculate_sha256(filepath):
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
 
def download_cmu_dataset():
    """Download CMU Sleep and GPA dataset."""
    url = "https://cmustatistics.github.io/data-repository/data/cmu-sleep.csv"
    output_path = DATA_DIR / "cmu_sleep.csv"
    print("=" * 60)
    print("DOWNLOADING CMU SLEEP DATASET")
    print("=" * 60)
    print(f"Source URL: {url}")
    print(f"Destination: {output_path}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise error for bad status codes
        # Save the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        # Calculate checksum
        checksum = calculate_sha256(output_path)
        print(f"✓ Download successful!")
        print(f"SHA-256: {checksum}")
        # Load and display basic info
        df = pd.read_csv(output_path)
        print(f"\nDataset Info:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Column names: {', '.join(df.columns.tolist())}")
        print(f"  File size: {os.path.getsize(output_path) / 1024:.2f} KB")
        return checksum
    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading dataset: {e}")
        return None
 
def verify_kaggle_dataset():
    """Verify the Kaggle dataset (must be downloaded manually)."""
    kaggle_path = DATA_DIR / "student_habits.csv"
    print("\n" + "=" * 60)
    print("VERIFYING KAGGLE DATASET")
    print("=" * 60)
    print(f"Expected location: {kaggle_path}")
    if not kaggle_path.exists():
        print("✗ Kaggle dataset not found!")
        print("\nMANUAL DOWNLOAD REQUIRED:")
        print("1. Go to: https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance")
        print("2. Click 'Download' (requires Kaggle account)")
        print("3. Save the CSV file as: data/raw/student_habits.csv")
        print("4. Run this script again to verify")
        return None
    try:
        # Calculate checksum
        checksum = calculate_sha256(kaggle_path)
        print(f"✓ Dataset found!")
        print(f"SHA-256: {checksum}")
        # Load and display basic info
        df = pd.read_csv(kaggle_path)
        print(f"\nDataset Info:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Column names: {', '.join(df.columns.tolist())}")
        print(f"  File size: {os.path.getsize(kaggle_path) / 1024:.2f} KB")
        return checksum
    except Exception as e:
        print(f"✗ Error reading dataset: {e}")
        return None
 
def save_checksums(cmu_checksum, kaggle_checksum):
    """Save checksums to a file for future verification."""
    checksum_file = DATA_DIR / "CHECKSUMS.txt"
    with open(checksum_file, 'w') as f:
        f.write("Dataset Checksums (SHA-256)\n")
        f.write("=" * 60 + "\n\n")
        if cmu_checksum:
            f.write(f"cmu_sleep.csv:\n{cmu_checksum}\n\n")
        if kaggle_checksum:
            f.write(f"student_habits.csv:\n{kaggle_checksum}\n\n")
        f.write(f"Generated: {pd.Timestamp.now()}\n")
    print(f"\n✓ Checksums saved to: {checksum_file}")
 
def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("DATA ACQUISITION SCRIPT")
    print("Sleep Patterns & Academic Performance Project")
    print("=" * 60 + "\n")
    # Download CMU dataset
    cmu_checksum = download_cmu_dataset()
    # Verify Kaggle dataset (manual download required)
    kaggle_checksum = verify_kaggle_dataset()
    # Save checksums
    if cmu_checksum or kaggle_checksum:
        save_checksums(cmu_checksum, kaggle_checksum)
    print("\n" + "=" * 60)
    print("ACQUISITION COMPLETE")
    print("=" * 60)
    if cmu_checksum and kaggle_checksum:
        print("✓ Both datasets ready!")
        print("\nNext steps:")
        print("1. Review the datasets in data/raw/")
        print("2. Run 02_data_cleaning.py (coming next)")
    elif cmu_checksum and not kaggle_checksum:
        print("⚠ CMU dataset ready, but Kaggle dataset needs manual download")
        print("  Follow the instructions above to download from Kaggle")
    else:
        print("⚠ Issues detected - review output above")
 
if __name__ == "__main__":
    main()