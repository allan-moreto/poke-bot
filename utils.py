import pyautogui
import pytesseract
import time 
import helper
import random
import difflib



last = time.time()

FIGHT_IMAGE_PATH = "./fight.png"
FIGHT_IMAGE_REGION = (940, 966, 1154, 1044)

possible_pokemon = {"golbat", "golem", "nidorino", "magcargo", "nidorina", "gyarados", "sandslash", "ariados", "ledian", "gloom", "weepinbell", "breloom", "magneton", "crawdaunt", "rockruff", "sunflora", "clefairy", "happiny", "alakazam", "excadrill", "zoroark", "conkeldurr"}

def log(message):
    global last
    now = time.time()
    elapsed_since_last = now - last
    print(f"{elapsed_since_last:.2f} - {message}")
    last = now


def elite_run():
    safe_press("4")
    time.sleep(0.1)


def observe_screen(region=(800, 135, 158, 28), lang="eng"):
    try:
        screenshot = pyautogui.screenshot(region=region)
        # screenshot = screenshot.convert("L")
        text = pytesseract.image_to_string(screenshot, lang=lang, config="--psm 8")
        return text.strip().lower() if text else None
    except Exception:
        return None
    
def check_if_alive(pokemon):
    detected = observe_screen()
    if detected == pokemon:
        return True
    return False


# def detect_pokemon():
#     pokemon = observe_screen()
#     while pokemon not in possible_pokemon:
#         print(f"{pokemon} has NOT passed name verification")
#         if pokemon and pokemon[0] in "[]|":
#             print(f"{pokemon} HAS passed named verification and will be attacked")
#             return pokemon
#         pokemon = observe_screen()
#     return pokemon

def detect_pokemon():
    pokemon = observe_screen()
    while True:
        # Try exact match or fuzzy match
        validated = validate_pokemon_name(pokemon, possible_pokemon, cutoff=0.6)
        
        if validated:  # Passes verification
            print(f"{pokemon} corrected to {validated}")
            return validated
        
        # Special case for elite
        if pokemon and pokemon[0] in "[]|":
            print(f"{pokemon} HAS passed named verification (elite) and will be attacked")
            return pokemon
        
        print(f"{pokemon} has NOT passed name verification")
        pokemon = observe_screen()
        

def wait_for_img(image_path, region, confidence=0.9, check_interval=0.2):
    while True:
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                region=region,
                confidence=confidence,
            )
            if location:
                return True  # stop looping and return when found
        except Exception as e:
            pass
            # Catch PyAutoGUI or screenshot errors, just keep looping
        time.sleep(check_interval)

def switch_to_sweeper():
    safe_press("2")
    wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)

    safe_press("1")
    time.sleep(0.2)
    safe_press("1")
    pokemon_alive = detect_pokemon()
    while not pokemon_alive:
        pokemon_alive = detect_pokemon()
    time.sleep(6)
    return 

    

def attack(move):
    time.sleep(0.2)
    safe_press("1")
    time.sleep(0.1)
    safe_press(move)


def safe_press(key):
    print(f"[DEBUG] Pressing {key} current pokemon: {helper.current_pokemon}")
    pyautogui.press(key)


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

# def is_lead_alive(region, image, confidence=0.9):
#     try:
#         found = pyautogui.locateOnScreen(image, region, confidence=confidence) is not None
#         if found:
#             return True
#         else:
#             return False
#     except Exception as e:
#         return False

# def is_lead_alive():
#     sprite_location = pyautogui.locateOnScreen("./deoxys_sprite.png", confidence=0.9)
#     print(sprite_location)
#     return True if sprite_location else False

def is_lead_alive():
    try:
        sprite_location = pyautogui.locateOnScreen("./deoxys_sprite.png", confidence=0.9)

        return sprite_location is not None
    except pyautogui.ImageNotFoundException:
        return False
    except Exception as e:
        print("Unexpected error:", e)
        return False
    

def validate_pokemon_name(pokemon, possible_pokemon, cutoff=0.6):
    if not pokemon:
        return None
    
    # Find the closest match in possible_pokemon
    matches = difflib.get_close_matches(pokemon, possible_pokemon, n=1, cutoff=cutoff)
    
    if matches:
        return matches[0]  # return the best match
    return None
