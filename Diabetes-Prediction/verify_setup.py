"""
Quick setup script to verify the new structure works
"""
import sys
from pathlib import Path

def check_structure():
    """Verify all key folders and files exist."""
    project_root = Path(__file__).parent
    
    required_paths = [
        'src/preprocessing/transformers.py',
        'src/training/train_model.py',
        'src/inference/predict.py',
        'src/evaluation/evaluate.py',
        'tests/test_diabetes_prediction.py',
        'config/config.py',
        'README_NEW.md',
        'INTERVIEW_NOTES.md',
        'PROJECT_STRUCTURE.md',
        '.gitignore'
    ]
    
    print("🔍 Checking project structure...")
    all_exist = True
    
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} - MISSING!")
            all_exist = False
    
    if all_exist:
        print("\n✅ All files created successfully!")
        print("\n📚 Next steps:")
        print("  1. Read RESTRUCTURING_SUMMARY.md for overview")
        print("  2. Read INTERVIEW_NOTES.md for interview prep")
        print("  3. Run: pytest tests/ -v")
        print("  4. Run: python -m src.training.train_model")
    else:
        print("\n❌ Some files are missing. Please check the structure.")
        sys.exit(1)

if __name__ == '__main__':
    check_structure()
