import utils
import time
import sys
import threading
import helper


time.sleep(3)

logfile = open("log.txt", "w")
sys.stdout = logfile

FIGHT_IMAGE_REGION = (940, 966, 1154, 1044)
FIGHT_IMAGE_PATH = "./fight.png"
LEAD_REGION= (1676, 800, 1996, 850)
LEAD_PATH = "./deoxys_name.png"
CURRENT_MOVE = ""

moves = {
    "golem": "2",
    "sandslash": "2",
    "gyarados": "3",
    "magcargo": "4",
    "magneton": "4",
    "crawdaunt": "3",
    "excadrill": "4",
    "zoroark": "2"
}
running = True


def battle_loop():
    global CURRENT_MOVE, running
    while running:
        helper.current_pokemon += 1
        print(f"Current Pokemon is {helper.current_pokemon}")

        utils.wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)

        # detect current pokemon name
        pokemon = utils.detect_pokemon()

        # If detect_pokemon returned None => we ran from an elite (or detect handled escape)
        if pokemon is None:
            print("[MAIN] detect_pokemon reported run/escape — resuming walking.")
            utils.walking = True
            time.sleep(0.5)   # small pause so walker thread notices the flag
            continue

        is_in_dict = pokemon in moves

        # STOP WALKING during the whole fight (only now, since we'll actually fight)
        utils.walking = False

        # Wait for the fight image and handle the first attack

        if not is_in_dict:
            utils.attack("1")
            CURRENT_MOVE = "1"
        else:
            utils.attack(moves[pokemon])
            CURRENT_MOVE = moves[pokemon]

        time.sleep(4)
        is_alive = utils.check_if_alive(pokemon)

        if is_alive:
            time.sleep(2)
            is_alive = utils.check_if_alive(pokemon)
            if is_alive:
                is_lead_alive = utils.is_lead_alive()
                if is_lead_alive:
                    utils.wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)
                    utils.attack(CURRENT_MOVE)
                else:
                    time.sleep(0.3)
                    utils.switch_to_sweeper()
                    # do not toggle walking here; wait for battle to fully end below

        # WAIT until the fight UI disappears (battle truly over)
        utils.wait_for_battle_end(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)

        # RESUME WALKING only once the battle screen is gone
        utils.walking = True
        time.sleep(0.07)

t = threading.Thread(target=utils.walker, daemon=True)
t.start()

battle_loop()

