import pyautogui
import pytesseract
import time 
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


# def elite_run():
#     print("running from elite")
#     safe_press("4")
#     time.sleep(0.1)

def elite_run(max_attempts=3):
    """Try to run from an elite up to max_attempts.
    Returns True if we escaped, False if we failed and are still in battle."""
    for attempt in range(1, max_attempts + 1):
        print(f"[ELITE] Attempt {attempt} to run")
        safe_press("4")
        time.sleep(1.0)  # give the game a moment to process the run attempt

        # Did the fight UI disappear?
        if wait_for_battle_end(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION, timeout=4):
            print("[ELITE] Successfully ran away!")
            return True
        else:
            print("[ELITE] Failed to run (still in battle). Retrying...")

    print("[ELITE] Could not escape after max attempts")
    return False


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


def detect_pokemon():
    pokemon = observe_screen()
    while True:
        validated = validate_pokemon_name(pokemon, possible_pokemon, cutoff=0.6)

        # Special case for elite
        if pokemon and pokemon[0] in "[]|":
            print(f"{pokemon} elite pokemon found — attempting to run")

            wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)
            escaped = elite_run()

            if escaped:
                # we are back to overworld
                return None
            else:
                # fallback: could not run, so return the validated elite name
                # let the battle_loop handle it (attack logic will kick in)
                validated = validate_pokemon_name(pokemon, possible_pokemon, cutoff=0.6)
                print(f"[DETECT] Could not escape, fallback to fighting {validated}")
                return validated

        if validated:
            print(f"{pokemon} corrected to {validated}")
            return validated

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
    """
    Do a simple, fast switch to the second slot and attack.
    *Do not* call detect_pokemon() here. Return quickly — main loop will observe battle state.
    """
    print("[UTILS] switching to sweeper (press 2)...")
    safe_press("2")
    time.sleep(0.35)              # let the switch animation start
    # sometimes fight UI might re-assert itself; ensure we are in fight UI before attacking
    wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION, check_interval=0.15)
    safe_press("1")              # select move
    time.sleep(0.12)
    safe_press("1")              # confirm/attack
    # return immediately — main loop will wait for battle end
    return

    

def attack(move):
    time.sleep(0.2)
    safe_press("1")
    time.sleep(0.1)
    safe_press(move)


def safe_press(key):
    print(f"Pressing key: {key}")
    pyautogui.press(key)


walking = True  # global flag, controlled from main

def walker():
    global walking
    last_state = None
    while True:
        if walking:
            if last_state is not True:
                last_state = True
            # Hold LEFT
            pyautogui.keyDown('left')
            time.sleep(random.uniform(0.3, 0.6))
            pyautogui.keyUp('left')

            # Hold RIGHT
            pyautogui.keyDown('right')
            time.sleep(random.uniform(0.3, 0.6))
            pyautogui.keyUp('right')
        else:
            if last_state is not False:
                last_state = False
            time.sleep(0.03)

def wait_for_battle_end(image_path, region=None, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            loc = pyautogui.locateOnScreen(image_path, region=region, confidence=0.9)
            if not loc:  # image disappeared
                return True
        except pyautogui.ImageNotFoundException:
            # This means locateOnScreen couldn’t find the file at all → treat as "not found"
            return True
        time.sleep(0.15)

    print("[DEBUG] Timed out, image never disappeared.")
    return False

def is_lead_alive():
    try:
        sprite_location = pyautogui.locateOnScreen("./deoxys_sprite.png", confidence=0.9)

        return sprite_location is not None
    except pyautogui.ImageNotFoundException:
        return False
    except Exception as e:
        return False
    

def validate_pokemon_name(pokemon, possible_pokemon, cutoff=0.6):
    if not pokemon:
        return None
    
    # Find the closest match in possible_pokemon
    matches = difflib.get_close_matches(pokemon, possible_pokemon, n=1, cutoff=cutoff)
    
    if matches:
        return matches[0]  # return the best match
    return None
