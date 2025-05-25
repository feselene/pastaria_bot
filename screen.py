import subprocess
import io
from PIL import Image

def save_adb_screenshot(output_path="adb_capture.png"):
    """
    Captures a screenshot from the emulator using ADB and saves it to the specified path.

    :param output_path: Path to save the captured image (default: 'adb_capture.png')
    """
    try:
        result = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
        image = Image.open(io.BytesIO(result)).convert("RGB")
        image.save(output_path)
        print(f"✅ Screenshot saved to {output_path}")
    except Exception as e:
        print(f"❌ Failed to capture or save ADB screenshot: {e}")


def main():
    save_adb_screenshot("adb_capture.png")


if __name__ == "__main__":
    main()
