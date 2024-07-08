from mechanics.pokemon import Pokemon
import requests
import os
import base64
from dotenv import load_dotenv

def generate(pokemon:Pokemon, control_strength:float=0.5, output_file=None):
    """
    'pokemon'
    'control_strength' - how strong the sketch has an effect
    """

    host = "https://api.stability.ai/v2beta/stable-image/control/sketch"

    # TODO: From pokemon desc class, grab a prompt
    prompt = pokemon.image_prompt
    sketch = pokemon.ref_image
    params = {
        "prompt":prompt,
        "image":base64.b64decode(sketch),
        "control_strength": control_strength,
        "style_preset": "anime",
        "aspect_ratio": "1:1",
    }

    response = send_generation_request(host, params)

    # Decode response
    encoded_image = response.json()["image"]

    decoded_image = base64.b64decode(encoded_image)
    # Save and display result
    if output_file is not None:
        with open(output_file, "wb") as f:
            f.write(decoded_image)
        print(f"Saved image {output_file}")

    return encoded_image

def generate_without_sketch(pokemon:Pokemon, output_file: str = None):

    host = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    prompt = pokemon.image_prompt

    params = {
        "prompt":prompt,
        "style_preset": "anime",
        "aspect_ratio": "1:1",
        "model": "sd3-medium"
    }

    response = send_generation_request(host, params)

    # Decode response
    encoded_image = response.json()["image"]

    decoded_image = base64.b64decode(encoded_image)
    # Save and display result
    if output_file is not None:
        with open(output_file, "wb") as f:
            f.write(decoded_image)
        print(f"Saved image {output_file}")

    return encoded_image


def generate_evol(pokemon: Pokemon, output_file: str=None):

    url = "https://api.getimg.ai/v1/stable-diffusion-xl/ip-adapter"

    encoded_string = pokemon.ref_image
    prompt = pokemon.image_prompt

    payload = {
        "adapter": "content",
        "prompt": prompt,
        "strength": 0.2,
        "image": encoded_string
    }

    response = getimg_send(url, payload)

    encoded_image = response.json()["image"]
    decoded_image = base64.b64decode(encoded_image)

    if output_file is not None:
        # Write the decoded bytes to a file
        with open(output_file, "wb") as image_file:
            image_file.write(decoded_image)

        print(f"Image saved as {output_file}")

    return encoded_image

def getimg_send(url, payload):
    load_dotenv()
    skey = os.getenv("GETIMG_KEY")
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {skey}"
    }

    print(f"Sending REST request to {url}")
    response = requests.post(url, json=payload, headers=headers)

    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

def generate_sprite(img):
    """
    'img' - a hi res image
    """

    nonbg_img = remove_bg(img)

def remove_bg(img):
    """
    'img' - img for the background to be removed
    """
    pass

def send_generation_request(
    host,
    params,
):
    load_dotenv()
    skey = os.getenv("STABILITY_KEY")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {skey}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = image
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

