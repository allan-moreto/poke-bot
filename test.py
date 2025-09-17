import pytesseract
import pyautogui
import time


time.sleep(2)

def observe_screen(region=((830, 400, 160, 22)), lang="eng"):
    try:
        screenshot = pyautogui.screenshot(region=region)
        # screenshot = screenshot.convert("L")

        text = pytesseract.image_to_string(screenshot, lang=lang, config="--psm 8")
        return text if text else None
    except Exception:
        return None
    
def is_elite():
    name = observe_screen()

    print(name)

is_elite()
def is_lead_alive():
    name = observe_screen((830, 400, 160, 22))
    print(f"THIs is CHeckin is Pokemon namE is Present in is_lead_alive {name}")

is_lead_alive()
