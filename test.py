from pokemon_content.pokemon_factory import PokemonFactory
from pokemon_content.pokemon_elements import PokemonElements
from pokemon_content.pokemon_rarity import PokemonRarity
from content.style import Style
import base64
from mechanics.pokemon import Pokemon
from util.img_util import pil_to_b64
import sd_generation
import render_cards

pokemon_style: Style = Style(
    subject_type="pokemon",
)

element = PokemonElements.FIRE

pf = PokemonFactory(
        theme_style=pokemon_style,
        elements=PokemonElements.ALL,
        rarities=PokemonRarity.ALL
)

with open("images/sketch3.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

    pok = pf.generate_base(element, PokemonRarity.COMMON, encoded_string)
    print(pok)
    img = render_cards.render_card(pok)
    img.show()


# with open("images/evol_0.png", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())

#     pok = Pokemon("Hello", element, PokemonRarity.COMMON, 100, 1, ref_image=encoded_string, curr_image=encoded_string, image_prompt="a evolved young fire-type pokemon, in a volcano environment, red and purple ambient lighting, anime sketch drawing style , anime 2d")
#     img = render_cards.render_card(pok)
#     img.show()


