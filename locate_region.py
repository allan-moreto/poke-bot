import pyautogui
import time
import pyautogui
from PIL import ImageDraw

time.sleep(2)


# Take a screenshot
screenshot = pyautogui.screenshot()

fight_image_location = (980, 980, 1106, 1026)
fight_image_region = (940, 966, 1154, 1044)
lead_region = (1676, 800, 1996, 850)
lead_location = (1693, 814, 1884, 838)
current_pokemon_region = (800, 140, 128, 26)
# Coordinates of detected image (example from locateOnScreen)
# If using pyautogui.locateOnScreen, this will be a box: left, top, width, height
# location = pyautogui.locateOnScreen("./assets/search_images/fight.png")

# Create a drawing object
draw = ImageDraw.Draw(screenshot)

# Draw a red rectangle around detected image
# if location:
#     x, y, w, h = location
#     draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
#     print("Drew rectangle around detected image!")


# Draw a rectangle around a custom area you choose
custom_area = (lead_region)  # (left, top, right, bottom)
draw.rectangle(custom_area, outline="blue", width=3)


# Save the image with rectangles
screenshot.save("screenshot_with_boxes.png")
print("Saved screenshot_with_boxes.png")

