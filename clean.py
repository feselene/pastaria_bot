import os
import shutil

# Directories to clean
DIRS_TO_CLEAN = [
    "debug",
    "toppings"
]

def clean_directory(dir_path):
    if not os.path.exists(dir_path):
        print(f"❌ Directory not found: {dir_path}")
        return
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"🧹 Deleted: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete {file_path}: {e}")

def clean_files():
    for dir_path in DIRS_TO_CLEAN:
        clean_directory(dir_path)

def main():
    for dir_path in DIRS_TO_CLEAN:
        clean_directory(dir_path)

if __name__ == "__main__":
    main()
