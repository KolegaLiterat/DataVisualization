import math

import pandas as pd
from PIL import Image, ImageDraw, ImageColor


def get_brand_names(dataframe: pd.DataFrame) -> list[str]:
    brand_names: list[str] = pd.unique(dataframe['brand'])

    return brand_names


def get_brand_entries(dataframe: pd.DataFrame, brand: str) -> pd.DataFrame:
    brand_entries = dataframe.loc[dataframe['brand'] == brand]

    return brand_entries


def calculate_background_height(brand_entries: pd.DataFrame) -> int:
    return math.ceil(len(brand_entries) / 10) * 32


def draw_shades(filename: str, height: int, colors: list[str]):
    background = Image.new('RGB', (320, height), (128, 128, 128))
    draw = ImageDraw.Draw(background)
    coordinates = [0, 0, 32, 32]

    lines: int = int(height / 32 + 1)
    color_index: int = 0

    for y in range(0, lines):
        for x in range(0, 10):
            if color_index < len(colors):
                draw.rectangle(coordinates, fill=colors[color_index], outline=(128, 128, 128))
                coordinates[0] = coordinates[0] + 32
                coordinates[2] = coordinates[2] + 32

                color_index = color_index + 1
            else:
                break

        coordinates[1] = coordinates[1] + 32
        coordinates[3] = coordinates[3] + 32
        coordinates[0] = 0
        coordinates[2] = 32


    jpg_name: str = filename + '.jpg'
    background.save(jpg_name, quality=95)


def main():
    dataframe = pd.read_csv('allShades.csv')

    brand_names: list[str] = get_brand_names(dataframe)

    for brand in brand_names:
        brand_entries: pd.DataFrame = get_brand_entries(dataframe, brand)
        height: int = calculate_background_height(brand_entries)
        colors: list[str] = list(brand_entries['hex'])

        draw_shades(brand, height, colors)


if __name__ == '__main__':
    main()
