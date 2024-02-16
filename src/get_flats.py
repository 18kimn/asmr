
import pandas as pd
from points import download_flats
import sys
from dotenv import load_dotenv
import os 
from PIL import Image

load_dotenv()
dirname = sys.argv[2]
api_key = os.getenv("MAPS_API_KEY")

if __name__ == "__main__":
    panoids = pd.read_csv(sys.argv[1])
    
    for i, row in panoids.head(50).iterrows():
        if not os.path.exists(f"{dirname}/2017_{row['panoid']}_0"):
            download_flats(row["panoid"], dirname, api_key)

        tile_width = 512
        tile_height = 512

        panorama = Image.new("RGB", (26 * tile_width, 13 * tile_height))

        for heading in [0, 90, 180, 270]:
            fname = f"{dirname}/2017_{row['panoid']}_{heading}"
            tile = Image.open(fname)

            panorama.paste(im=tile, box=(x * tile_width, y * tile_height))
            os.remove(fname)

            del tile
        panorama.save(final_directory + ("/%s.jpg" % panoid))
        del panorama