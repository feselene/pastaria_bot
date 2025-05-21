import pyautogui

print("🔍 Move your mouse around the screen — press Ctrl+C to stop.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse at X: {x}, Y: {y}", end="\r")
except KeyboardInterrupt:
    print("\n🛑 Done.")
