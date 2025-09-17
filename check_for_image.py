import time
import pyautogui

time.sleep(3)

def is_image_present(image_path, region=None, confidence=0.9):
    """
    Checks if the given image exists on the screen (or in a region).
    
    Parameters:
    - image_path: str, path to the image file
    - region: tuple (x, y, width, height), optional search area
    - confidence: float, 0.0-1.0 confidence threshold
    
    Returns:
    - True if image found, False otherwise
    """
    try:
        return pyautogui.locateOnScreen(image_path, region=region, confidence=confidence) is not None
    except Exception as e:
        print(f"Error detecting image: {e}")
        return False

# Example usage
if __name__ == "__main__":
 # Path to your image
    IMAGE_PATH = "./deoxys_name.png"

# Optional: define a region to limit search (x, y, width, height)
    SEARCH_REGION = (1676, 800, 1996, 850)
    
    if is_image_present(IMAGE_PATH, region=SEARCH_REGION):
        print("Image detected!")
    else:
        print("Image not detected.")
