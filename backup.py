import subprocess
import os
import sys

ADB_PORT = "127.0.0.1:21503"  # Default MEmu port
APP_PACKAGE = "air.com.flipline.papaspastariatogo"
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "./"))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
BACKUP_DIR = os.path.join(ROOT_DIR, "backups")

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def adb(cmd):
    run(f"adb connect {ADB_PORT}")
    run(f"adb root")
    run(f"adb {cmd}")

def backup():
    print("🔄 Backing up Papa's Pastaria To Go! data...")
    adb(f"shell mkdir -p /sdcard/Backups/PapasPastaria")
    adb(f"shell cp -r /data/data/{APP_PACKAGE}/* /sdcard/Backups/PapasPastaria/")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    adb(f"pull /sdcard/Backups/PapasPastaria {BACKUP_DIR}")
    print("✅ Backup complete.")

def restore():
    restore_path = os.path.join(BACKUP_DIR, "PapasPastaria")
    if not os.path.exists(restore_path):
        print("❌ No backup found at:", restore_path)
        sys.exit(1)

    print("⏪ Restoring save data...")
    adb(f"shell am force-stop {APP_PACKAGE}")

    for subfolder in ["files", "shared_prefs", "databases"]:
        local_path = os.path.join(restore_path, subfolder)
        if os.path.exists(local_path):
            adb(f"push \"{local_path}\" \"/data/data/{APP_PACKAGE}/{subfolder}\"")

    print("✅ Restore complete. Restart the app manually.")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"backup", "restore"}:
        print("Usage: python papas_backup_tool.py [backup|restore]")
        sys.exit(1)

    action = sys.argv[1]
    if action == "backup":
        backup()
    elif action == "restore":
        restore()
