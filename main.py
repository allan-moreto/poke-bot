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
    "excadrill": "4"
}
running = True


def battle_loop():
    global CURRENT_MOVE
    global running
    while running:
        helper.current_pokemon += 1
        print(f"Current Pokemon is {helper.current_pokemon}")
        pokemon = utils.detect_pokemon()
        # running = False
        is_in_dict = pokemon in moves

        utils.wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)
        # time.sleep(1)
        utils.elite_run() # this might need to get fixed.. if runs from elite, still going to wait 4 seconds and attack which will mess with timing, for now lets skip this

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
                # is_lead_alive = utils.is_lead_alive(LEAD_PATH, LEAD_REGION, 0.9)
                is_lead_alive = utils.is_lead_alive()

                if is_lead_alive:
                    utils.wait_for_img(FIGHT_IMAGE_PATH, FIGHT_IMAGE_REGION)
                    utils.attack(CURRENT_MOVE)
                    time.sleep(5)
                    continue
                    # running = True
                else:
                    time.sleep(.3)
                    utils.switch_to_sweeper()
                    continue
                    # running = True
            else:
                continue
                # running = True
        else:
            continue
        #     # running = True


# def walk():
#     global running, walking
#     while running:
#         if walking:
#             # Hold LEFT
#             pyautogui.keyDown('left')
#             time.sleep(random.uniform(0.4, 0.6))
#             pyautogui.keyUp('left')

#             # Hold RIGHT
#             pyautogui.keyDown('right')
#             time.sleep(random.uniform(0.4, 0.6))
#             pyautogui.keyUp('right')
#         else:
#             time.sleep(0.1) 


# # game_thread = threading.Thread(target=battle_loop)
# walk_thread = threading.Thread(target=walk)

# # game_thread.start()
# walk_thread.start()

t = threading.Thread(target=utils.walker, daemon=True)
t.start()

battle_loop()



        

        




        
#check if pokemon has been detected using OCR and return pokemon name also create a pokemon template to test if pokemon is still alive or not...


#pokemon performs initial attack using corresponding move waits 5 seconds and checks if pokemon is alive

#check if pokemon is alive
# to check if current oponent pokemon is alive. 

# if pokemon is dead, break

# if not dead
# check if lead pokemon is alive
    #if alive, wait_for_image + attack(move)
    #if dead switch pokemon + wait_for_image + 1+1 attack









