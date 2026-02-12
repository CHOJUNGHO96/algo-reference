"""Validate backend structure without installing dependencies"""

import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))


def check_file_exists(path: str) -> bool:
    """Check if file exists"""
    return Path(path).exists()


def validate_structure():
    """Validate project structure"""
    print("Validating backend project structure...\n")

    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/core/security.py",
        "app/models/__init__.py",
        "app/models/algorithm.py",
        "app/models/category.py",
        "app/models/code_template.py",
        "app/models/difficulty.py",
        "app/models/language.py",
        "app/models/user.py",
        "app/schemas/__init__.py",
        "app/schemas/algorithm.py",
        "app/schemas/category.py",
        "app/schemas/code_template.py",
        "app/schemas/difficulty.py",
        "app/schemas/language.py",
        "app/schemas/auth.py",
        "app/api/v1/__init__.py",
        "app/api/v1/endpoints/__init__.py",
        "app/api/v1/endpoints/algorithms.py",
        "app/api/v1/endpoints/categories.py",
        "app/api/v1/endpoints/languages.py",
        "app/api/v1/endpoints/auth.py",
        "app/api/dependencies.py",
        "alembic/env.py",
        "alembic.ini",
        "requirements.txt",
        "README.md",
    ]

    all_exist = True
    for file_path in required_files:
        exists = check_file_exists(file_path)
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False

    print("\n" + "=" * 60)

    if all_exist:
        print("[OK] All required files exist!")
        print("\nNext steps: Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure PostgreSQL database")
        print("3. Start server: uvicorn app.main:app --reload")
        print("4. View docs at: http://localhost:8000/docs")
        return 0
    else:
        print("[MISSING] Some files are missing!")
        return 1


if __name__ == "__main__":
    sys.exit(validate_structure())
