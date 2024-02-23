import deck

import glob
import math
import pathlib

import fpdf
import wand.image


def load_images(res_dir: pathlib.Path,
                cards: dict[deck.Card]) -> dict[wand.image.Image]:
    images = {}

    for card in cards:
        front_image = cards[card].images["front"]
        if images.get(f"f:{front_image}") is None:
            images[f"f:{front_image}"] = wand.image.Image(
                filename=res_dir.joinpath(f"fronts/{front_image}")
            )

        back_image = cards[card].images["back"]
        if images.get(f"b:{back_image}") is None:
            images[f"b:{back_image}"] = wand.image.Image(
                filename=res_dir.joinpath(f"backs/{back_image}")
            )

    return images


def tile_images(
        images: dict[list[wand.image.Image]],
        side: str,
        geometry: str,
        layout: str
) -> wand.image.Image:
    if side != "front" and side != "back":
        return None

    card_sheet = wand.image.Image()
    print(side)

    if side == "front":
        for image in images[side]:
            card_sheet.image_add(image)
    else:
        for i in range(0, math.ceil(len(images[side]) / 3)):
            row = images[side][i*3:(i*3)+3]
            while len(row) < 3:
                row.append(wand.image.Image(width=1, height=1))
            for image in reversed(row):
                card_sheet.image_add(image)

    card_sheet.montage(thumbnail=geometry, tile=layout)
    card_sheet.format = "png"

    return card_sheet


def dereference_card_images(
        cards: list[deck.Card],
        images: dict[wand.image.Image]
) -> dict[list[wand.image.Image]]:
    card_images = {}
    card_images["front"] = []
    card_images["back"] = []

    for card in cards:
        card_images["front"].append(
                images.get(f"f:{card.images.get('front')}"))
        card_images["back"].append(
                images.get(f"b:{card.images.get('back')}"))

    return card_images


def compile_pdf(out_dir: pathlib.Path,
                height: int, width: int) -> fpdf.FPDF():
    pdf = fpdf.FPDF()
    images = glob.glob(str(out_dir.joinpath("img/*")))

    for i in range(0, math.floor(len(images) / 2)):
        pdf.add_page()
        pdf.image(str(out_dir.joinpath(f"img/front-{i}.png")),
                  (210 - width) / 2, (297 - height) / 2, width, height)
        pdf.add_page()
        pdf.image(str(out_dir.joinpath(f"img/back-{i}.png")),
                  (210 - width) / 2, (297 - height) / 2, width, height)

    return pdf
