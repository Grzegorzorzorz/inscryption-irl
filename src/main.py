#!/bin/env python3

import deck
import sheet

import glob
import pathlib
import shutil

import wand.image


def prepare(project_root: pathlib.Path):
    try:
        shutil.rmtree(project_root.joinpath("out/img"))
    except FileNotFoundError:
        pass
    try:
        project_root.joinpath("out/").mkdir()
    except FileExistsError:
        pass
    try:
        project_root.joinpath("out/img").mkdir()
    except FileExistsError:
        pass


def compile(project_root: pathlib):
    # Load in all of our card and pack definitions.
    cards = deck.load("card", project_root.joinpath("defs/"))
    packs = deck.load("pack", project_root.joinpath("defs/"))

    images = sheet.load_images(project_root.joinpath("res/"), cards)

    opened_packs = deck.open_packs(
        deck.load_composition(
            project_root.joinpath("defs/deck.json"), packs),
        cards
    )

    card_images = sheet.dereference_card_images(opened_packs, images)
    sheet.tile_images(card_images, "front", "741x1098", "3x3") \
        .save(filename=project_root.joinpath("out/img/front-%d.png"))
    sheet.tile_images(card_images, "back", "691x1050", "3x3") \
        .save(filename=project_root.joinpath("out/img/back-%d.png"))


def convert(project_root: pathlib):
    # TODO: Bit of a hack, make all images 24 bit depth, otherwise FPDF
    # will complain. I tried to make it work without reloading, but sadly it
    # didn't work.

    print("Converting bit depth...")
    for image_path in glob.glob(str(project_root.joinpath("out/img/*"))):
        img_path = pathlib.Path(image_path)
        with wand.image.Image(filename=img_path, format="png") as img:
            img.depth = 8
            img.format = "PNG"
            img.save(filename=img_path)


def link(project_root: pathlib):
    # TODO: move card size to config file, it would give this more use cases.
    # width = 58 * 3
    # height = 89 * 3
    width = 57.5 * 3
    height = 89 * 3

    pdf = sheet.compile_pdf(project_root.joinpath("out/"), height, width)
    pdf.output(project_root.joinpath("out/cards.pdf"), "F")


def main():
    project_root = pathlib.Path(__file__).resolve().parent.parent

    prepare(project_root)
    compile(project_root)
    convert(project_root)
    link(project_root)


if __name__ == "__main__":
    main()
