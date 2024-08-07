from dataclasses import dataclass, field
from functools import cached_property
from content.style import Style
from mechanics.element import Element
from mechanics.rarity import Rarity
from mechanics.ability import Ability

STAR_UNICODE = "★ "


@dataclass
class Pokemon:

    name: str
    element: Element
    rarity: Rarity
    hp: int
    series_index: int
    ref_image: str   # base64 reference image
    abilities: list[Ability] = field(default_factory=list)
    description: str = ""
    part_of_evolution: bool = False
    style: Style = field(default_factory=Style)

    image_prompt: str | None = None
    visual_description: str | None = None

    # Generated image
    curr_image: str | None = None    # base64 generated image

    def __repr__(self):
        rarity_stars = STAR_UNICODE * (self.rarity.index + 1)
        message = f"{self.name} ({self.element.ascii_name()})\n"
        message += f"HP: {self.hp}\n"
        message += f"Rarity: {rarity_stars} ({self.rarity.name})\n"
        message += f"Abilities:\n"
        for ability in self.abilities:
            message += f"  {ability}\n"

        message += f"Description:\n"
        message += f"{self.description}\n\n"
        message += f"Image Prompt:\n"
        message += f"{self.image_prompt}\n\n"
        return message

    def to_json(self):
        return {
            "name": self.name,
            "element": self.element.name,
            "rarity": self.rarity.name,
            "rarity_index": self.rarity.index,
            "hp": self.hp,
            "abilities": [ability.to_json() for ability in self.abilities],
            "image_prompt": self.image_prompt,
            "curr_image": self.curr_image,
            "description": self.description
        }

    @property
    def image_file(self):
        return f"{self.index:03d}_{self.snake_case_name}.png"

    @cached_property
    def snake_case_name(self):
        return self.name.lower().replace(" ", "_")

    def def_json():
        return {
            "element": "fire",
            "rarity": "common",
            "rarity_index": 1,
            "hp": 80,
            "abilities": ["hello1", "hello2"],
            "image_prompt": "some prompt",
            "curr_image": "base64 image"
        }

