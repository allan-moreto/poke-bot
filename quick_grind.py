import pyautogui
import time
import random
import threading
from pynput import keyboard

running = True  # Flag global

time.sleep(15)

def auto_click():
    global running
    while running:
        pyautogui.click()
        time.sleep(0.3)

def move_left_right():
    global running
    while running:
        # Hold LEFT
        pyautogui.keyDown('left')
        time.sleep(random.uniform(0.3, 0.6))
        pyautogui.keyUp('left')

        # Hold RIGHT
        pyautogui.keyDown('right')
        time.sleep(random.uniform(0.3, 0.6))
        pyautogui.keyUp('right')

def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc:
            print("⛔ ESC pressionado, parando...")
            running = False
            return False  # Para o listener
    except:
        pass

# Thread para ouvir o teclado
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Thread do clique automático
click_thread = threading.Thread(target=auto_click, daemon=True)
click_thread.start()

# Movimento no thread principal
move_left_right()
