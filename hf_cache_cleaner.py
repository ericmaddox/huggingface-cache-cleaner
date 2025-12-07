#!/usr/bin/env python3
"""
Clean up HuggingFace cache to free disk space
"""

import os
import shutil
from pathlib import Path
import subprocess

def get_folder_size(path):
    """Get folder size"""
    try:
        result = subprocess.run(
            ['du', '-sh', str(path)],
            capture_output=True,
            text=True
        )
        return result.stdout.split()[0]
    except:
        return "Unknown"

def main():
    print("="*80)
    print("HUGGINGFACE CACHE CLEANUP")
    print("="*80)
    print()
    
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    
    if not cache_dir.exists():
        print("No cache found. Nothing to clean up.")
        return
    
    # Find all model folders
    models = [d for d in cache_dir.iterdir() if d.is_dir() and d.name.startswith("models--")]
    
    if not models:
        print("No cached models found.")
        return
    
    print(f"Found {len(models)} cached model(s):\n")
    
    for i, model in enumerate(models, 1):
        model_name = model.name.replace("models--", "").replace("--", "/")
        size = get_folder_size(model)
        print(f"{i}. {model_name}")
        print(f"   Size: {size}")
        print(f"   Path: {model}")
        print()
    
    print("="*80)
    print()
    print("Options:")
    print("1. Delete Mistral-7B only (frees ~14 GB)")
    print("2. Delete all cached models")
    print("3. Exit without deleting")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        # Delete Mistral-7B
        mistral_models = [m for m in models if "Mistral-7B" in m.name]
        if mistral_models:
            for model in mistral_models:
                model_name = model.name.replace("models--", "").replace("--", "/")
                print(f"\nDeleting {model_name}...")
                try:
                    shutil.rmtree(model)
                    print(f"✓ Deleted successfully")
                except Exception as e:
                    print(f"✗ Error: {e}")
        else:
            print("\nNo Mistral-7B models found in cache.")
    
    elif choice == "2":
        # Delete all
        confirm = input("\n⚠️  Delete ALL cached models? This cannot be undone! (yes/no): ").strip().lower()
        if confirm == "yes":
            for model in models:
                model_name = model.name.replace("models--", "").replace("--", "/")
                print(f"Deleting {model_name}...")
                try:
                    shutil.rmtree(model)
                    print(f"✓ Deleted")
                except Exception as e:
                    print(f"✗ Error: {e}")
            print("\n✓ All models deleted")
        else:
            print("Cancelled.")
    
    else:
        print("\nNo changes made.")
    
    print()
    print("="*80)

if __name__ == "__main__":
    main()
