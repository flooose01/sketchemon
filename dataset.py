import subprocess
import constants
import numpy as np
import cv2
import matplotlib.pyplot as plt

MAX_POKEMON = 1024

def get_dataset():
    for i in range(1, constants.MAX_POKEMON + 1):
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
        subprocess.run(["wget", "-P", "./dataset", url])


def preprocess():
    """
    Create sketches for each sprite in /dataset
    """

    # Change transparent background to white
    # for better edge detection
    for i in range(1, constants.MAX_POKEMON + 1):
        white_bg(i)
        sketch(i)
        print(f"{i} preprocessed")

def white_bg(num):
    image = cv2.imread(f"dataset/{num}.png", cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 4:
        # Split the image into its components
        b, g, r, a = cv2.split(image)

        # Create a white background with the same dimensions
        white_background = np.ones_like(image, dtype=np.uint8) * 255  # All white background
        white_background = cv2.cvtColor(white_background, cv2.COLOR_BGR2BGRA)

        # Blend the image with the white background using the alpha channel
        alpha = a / 255.0
        for c in range(0, 3):
            white_background[:, :, c] = white_background[:, :, c] * (1 - alpha) + image[:, :, c] * alpha

        # Remove the alpha channel by converting to BGR
        result = cv2.cvtColor(white_background, cv2.COLOR_BGRA2BGR)
    else:
        # If the image doesn't have an alpha channel, just convert it to BGR
        result = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    cv2.imwrite(f"dataset/white_{num}.png", result)

def sketch(num):
    """
    Create sketches for sprite 'num'
    """
    gray_sprite = cv2.imread(f"dataset/white_{num}.png", cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(gray_sprite, threshold1=90, threshold2=270)
    edges = 255 - edges
    cv2.imwrite(f"dataset/sketch_{num}.png", edges)

preprocess()