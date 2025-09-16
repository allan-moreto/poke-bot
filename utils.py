import pyautogui
import pytesseract
import time
import random

last = time.time()

def log(message):
    global last
    now = time.time()
    elapsed_since_last = now - last
    print(f"{elapsed_since_last:.2f} - {message}")
    last = now


def elite_run():
    log(f"clicking number 4")
    pyautogui.press("4")
    time.sleep(0.1)
    log("ran from elites")

def wait_for_fight_img():
    print("fight image found")

def observe_screen(region=(800, 140, 128, 26), lang="eng"):
    try:
        screenshot = pyautogui.screenshot(region=region)
        screenshot = screenshot.convert("L")
        text = pytesseract.image_to_string(screenshot, lang=lang, config="--psm 7")
        return text.strip().lower() if text else None
    except Exception:
        return None
    
def check_if_alive(pokemon):
    detected = observe_screen()
    if detected == pokemon:
        return True
    return False


def detect_pokemon():
    while True:
        pokemon = observe_screen()

        if pokemon:
            return pokemon

        time.sleep(0.3) ## check if necessary

def wait_for_img(image_path, region, confidence=0.9, check_interval=0.3):

    while True:
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                region=region,
                confidence=confidence,
            )
            if location:
                log("Fight image found, may attack now!")
                return True  # stop looping and return when found
        except Exception as e:
            pass
            # Catch PyAutoGUI or screenshot errors, just keep looping
        time.sleep(check_interval)

def attack(move):
    time.sleep(0.2)
    log(f"clicking number 1")
    pyautogui.press("1")
    time.sleep(0.2)
    log(f"clicking number {move}")
    pyautogui.press(move)

def walker():
    while True:
        # Hold LEFT
        pyautogui.keyDown('left')
        time.sleep(random.uniform(0.4, 0.6))
        pyautogui.keyUp('left')

        # Hold RIGHT
        pyautogui.keyDown('right')
        time.sleep(random.uniform(0.4, 0.6))
        pyautogui.keyUp('right')

def is_lead_alive(region, image, confidence=0.9):
    try:
        found = pyautogui.locateOnScreen(image, region, confidence=confidence)
        if found:
            return True
        else:
            return False
    except Exception as e:
        return False