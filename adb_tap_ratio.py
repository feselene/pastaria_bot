import subprocess
import argparse

def adb_tap_relative(x_ratio: float, y_ratio: float):
    if not (0 <= x_ratio <= 1 and 0 <= y_ratio <= 1):
        raise ValueError("x_ratio and y_ratio must be between 0 and 1.")

    # Get screen resolution
    result = subprocess.run(["adb", "shell", "wm", "size"], capture_output=True, text=True)
    output = result.stdout.strip()

    if "Physical size" not in output:
        raise RuntimeError(f"Failed to get screen size: {output}")

    resolution = output.split("Physical size: ")[1]
    screen_width, screen_height = map(int, resolution.split("x"))

    # Calculate absolute coordinates
    x = int(screen_width * x_ratio)
    y = int(screen_height * y_ratio)

    # Perform the tap
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    print(f"Tapped at ({x}, {y}) on a screen of size {screen_width}x{screen_height}")

def main():
    adb_tap_relative(0.2152, 0.03)

if __name__ == "__main__":
    main()

