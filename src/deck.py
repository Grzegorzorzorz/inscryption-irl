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

    print("Building deck using:")
    for pack_name in deck_json["packs"]:
        print(f"\t{deck_json['packs'][pack_name]} x {pack_name}")
        for i in range(0, deck_json["packs"][pack_name]):
            deck_packs.append(packs[pack_name])

    return deck_packs


def load_card(card_path: pathlib.Path) -> Card:
    with open(card_path, "r") as f:
        try:
            card_json = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Card `{card_path.name}` is not "
                  "properly formatted. Skipping...")
            return None

    try:
        new_card = Card()
        new_card.name = card_json["name"]
        new_card.images["front"] = card_json["images"]["front"]
        new_card.images["back"] = card_json["images"]["back"]

        return new_card
    except KeyError:
        print(f"Pack {card_path.stem} is missing fields.")
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
            continue
        if (new_pard is not None):
            new_pards[new_pard.name] = new_pard

    return new_pards


def load_pack(pack_path: pathlib.Path) -> Pack:
    with open(pack_path, "r") as f:
        try:
            pack_json = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Pack `{pack_path.name}` is not "
                  "properly formatted. Skipping...")
            return None

    try:
        new_pack = Pack()
        new_pack.name = pack_json["name"]

        for card in pack_json["cards"]:
            if type(pack_json["cards"][card]) is not int:
                print(f"Pack `{new_pack.name}` contains an erronious "
                      f"card inclusion `{card}`. Skipping card...")
                continue
            for i in range(0, pack_json["cards"][card]):
                new_pack.cards.append(card)

        return new_pack
    except KeyError:
        print(f"Pack {pack_path.stem} is missing fields.")
        return None


def open_pack(pack: Pack, cards: dict[Card]) -> list[Card]:
    opened_pack = []

    for card in pack.cards:
        try:
            opened_pack.append(cards.get(card))
        except KeyError:
            print(f"Card `{card.name}` in pack `{pack.name}`"
                  " could not be found")

    return opened_pack


def open_packs(packs: list[Pack], cards: dict[Card]) -> list[Card]:
    opened_packs = []

    for pack in packs:
        opened_packs += open_pack(pack, cards)

    return opened_packs
