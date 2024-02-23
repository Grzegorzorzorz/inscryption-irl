import json
import pathlib

from dataclasses import dataclass
from dataclasses import field


@dataclass
class Card:
    name: str = ""
    images: dict[str] = field(default_factory=dict[str])


@dataclass
class Pack:
    name: str = ""
    cards: list[str] = field(default_factory=list[str])


def load_composition(deck_path: pathlib.Path,
                     packs: dict[Pack]) -> list[Pack]:
    with open(deck_path, "r") as f:
        deck_json = json.load(f)

    deck_packs = []

    print(deck_json)
    for pack_name in deck_json["packs"]:
        for i in range(0, deck_json["packs"][pack_name]):
            deck_packs.append(packs[pack_name])

    return deck_packs


def load_card(card_path: pathlib.Path) -> Card:
    with open(card_path, "r") as f:
        card_json = json.load(f)

    try:
        new_card = Card()
        new_card.name = card_json["name"]
        new_card.images["front"] = card_json["images"]["front"]
        new_card.images["back"] = card_json["images"]["back"]

        return new_card
    except KeyError:
        return None


def load(type: str, def_path: pathlib.Path):
    # A pard is a mixture of a pack and card ;)
    new_pards = {}
    for pard_definition in \
            def_path.joinpath(f"{type}s/").glob("**/*.json"):
        if type == "pack":
            new_pard = load_pack(pard_definition)
        elif type == "card":
            new_pard = load_card(pard_definition)
        else:
            return None
        new_pards[new_pard.name] = new_pard

    return new_pards


def load_pack(pack_path: str) -> Pack:
    with open(pack_path, "r") as f:
        pack_json = json.load(f)

    try:
        new_pack = Pack()
        new_pack.name = pack_json["name"]

        for card in pack_json["cards"]:
            for i in range(0, pack_json["cards"][card]):
                new_pack.cards.append(card)

        return new_pack

    except KeyError:
        return None


def open_pack(pack: Pack, cards: dict[Card]) -> list[Card]:
    opened_pack = []

    for card in pack.cards:
        opened_pack.append(cards.get(card))

    return opened_pack


def open_packs(packs: list[Pack], cards: dict[Card]) -> list[Card]:
    opened_packs = []

    for pack in packs:
        opened_packs += open_pack(pack, cards)

    return opened_packs
