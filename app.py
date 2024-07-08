import random
from flask import Flask, render_template, request, jsonify
import base64
from pokemon_content.pokemon_factory import PokemonFactory
from content.style import Style
from pokemon_content.pokemon_elements import PokemonElements
from pokemon_content.pokemon_rarity import PokemonRarity
from mechanics.pokemon import Pokemon
from render_cards import render_card
from util.img_util import pil_to_b64
import json

app = Flask(__name__)

pf = PokemonFactory(
    theme_style=Style(subject_type="pokemon"),
    rarities=PokemonRarity.ALL,
    elements=PokemonElements.ALL
)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    if data['img_provided']:
        if data['image'] is None or data['series'] is None:
                return "Bad request", 400
    else:
        if data['series'] is None:
                return "Bad request", 400


    image_data = None

    if data['img_provided']:
        image_data = data['image']
        image_data = image_data.split(',')[1]

    series = int(data['series'])

    elt = random.choice(PokemonElements.ALL)
    rarity = random.choice(PokemonRarity.ALL)

    pok_base = pf.generate_base(elt, rarity, image_data)

    poks = [pok_base]
    if series > 1:
        for i in range(1, series):
            pok_evol = pf.generate_evol(poks[i - 1])
            poks.append(pok_evol)

    cards = [pil_to_b64(render_card(pok)).decode('utf-8') for pok in poks]
    poks_json = [pok.to_json() for pok in poks]

    payload = jsonify({"cards":cards, "pokemons":poks_json})

    return payload

if __name__ == '__main__':
    app.run()
