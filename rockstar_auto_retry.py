import time
import dxcam
import pyautogui
import keyboard
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ================== CONFIG ==================
# RECTANGLE TO OCR (x1, y1, x2, y2) ON MAIN MONITOR
REGION = (132, 123, 1706, 852)   # <-- CHANGE ME: x1, y1, x2, y2

# CENTER OF RETRY BUTTON
RETRY_POS = (679, 606)           # <-- CHANGE ME: retry_x, retry_y

# IDLE POSITION FOR MOUSE
IDLE_POS  = (836, 829)           # <-- CHANGE ME: idle_x, idle_y

CHECK_INTERVAL = 4.0              # seconds between checks
CLICK_COOLDOWN = 12.0             # min seconds between auto-clicks

TRIGGER_WORDS = ["retry", "connection", "lost", "error"]
# ============================================

paused = False
running = True
last_click = 0

# capture PRIMARY monitor
camera = dxcam.create(output_idx=0)
pyautogui.FAILSAFE = True


def toggle_pause():
    global paused
    paused = not paused
    print("[*] PAUSED" if paused else "[*] RESUMED")


def stop_script():
    global running
    running = False
    print("[*] Exiting...")


def grab_region():
    x1, y1, x2, y2 = REGION
    frame = camera.grab(region=(x1, y1, x2, y2))
    if frame is None:
        print("[WARN] dxcam frame None")
        return None
    # BGRA -> RGB
    bgr = frame[:, :, :3]
    rgb = bgr[:, :, ::-1]
    return Image.fromarray(rgb)


def detect_text():
    img = grab_region()
    if img is None:
        return False

    text = pytesseract.image_to_string(img, config="--psm 6").lower()
    print(f"[DEBUG] OCR: {text!r}")

    return any(word in text for word in TRIGGER_WORDS)


def click_retry():
    global last_click
    print("[+] Clicking Retry at", RETRY_POS)
    pyautogui.moveTo(*RETRY_POS, duration=0.1)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.moveTo(*IDLE_POS, duration=0)
    last_click = time.time()


def test_retry():
    click_retry()


def main():
    global last_click

    print("Rockstar TEXT auto-retry running.")
    print("  Ctrl+Alt+P -> pause/resume")
    print("  Ctrl+Alt+Q -> quit")
    print("  Ctrl+Alt+R -> test Retry click\n")

    last_click = 0

    while running:
        if not paused:
            try:
                if detect_text():
                    now = time.time()
                    if now - last_click > CLICK_COOLDOWN:
                        click_retry()
                    else:
                        print("[INFO] Detected but still in cooldown")
                # keep mouse parked
                pyautogui.moveTo(*IDLE_POS, duration=0)
            except Exception as e:
                print("[!] Error in loop:", e)

        time.sleep(CHECK_INTERVAL)

    print("Goodbye.")


# Hotkeys
keyboard.add_hotkey("ctrl+alt+p", toggle_pause)
keyboard.add_hotkey("ctrl+alt+q", stop_script)
keyboard.add_hotkey("ctrl+alt+r", test_retry)

if __name__ == "__main__":
    main()
