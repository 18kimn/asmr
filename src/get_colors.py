import colorsys

import cv2
import numpy as np
import pandas as pd

ocr = pd.read_csv("outputs/clean_ocr.csv")
files = ocr["filename"].unique()


def get_colors():
    file_dfs = []
    for i, file in enumerate(files):
        print(f"Processing {file} ({i}/{len(files)})")
        file_ocr = ocr[ocr["filename"] == file].copy()
        image = cv2.imread(file)
        colors = []
        for _, row in file_ocr.iterrows():
            x = row["left"]
            y = row["top"]
            width = row["width"]
            height = row["height"]
            cropped_image = image[y : y + height, x : x + width]
            hsv_crop = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
            hue_hist = cv2.calcHist([hsv_crop], [0], None, [180], [0, 180])
            dominant_hues = np.argmax(hue_hist)
            rgb_color = colorsys.hsv_to_rgb(dominant_hues / 180, 1.0, 1.0)
            # Convert the RGB color to hex code
            hex_code = "#{:02x}{:02x}{:02x}".format(
                int(rgb_color[0] * 255),
                int(rgb_color[1] * 255),
                int(rgb_color[2] * 255),
            )
            colors.append(hex_code)

        file_ocr["color"] = colors
        file_dfs.append(file_ocr)

    colors = pd.concat(file_dfs, ignore_index=True)
    colors.to_csv("outputs/colors.csv")


get_colors()
