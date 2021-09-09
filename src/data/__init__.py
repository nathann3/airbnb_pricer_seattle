import math
import os
import requests

from tqdm import tqdm


def download_data(fp, url=None):
    """
    Downloads data from a url to file path.
    """
    if not url:
        url = 'http://data.insideairbnb.com/united-states/wa/seattle/2020-07-14/data/listings.csv.gz'
    r = requests.get(url, stream=True)
    block_size = 1024
    total_size = int(r.headers.get('content-length', 0))
    num_iterables = math.ceil(total_size / block_size)

    # Download if not already downloaded.
    if not os.path.exists(fp):
        dir, name = os.path.split(fp)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(fp, "wb") as file:
            for data in tqdm(
                r.iter_content(block_size), total=num_iterables, unit="KB", unit_scale=True
            ):
                file.write(data)


def subset(df, property_type, accommodates, bedrooms):
    """
    Filters listings DataFrame by property type, number of accommodations and
    bedrooms.
    """
    filter = (df.property_type_cleansed == property_type) & (df.accommodates == accommodates) & (df.bedrooms == bedrooms)
    if df[filter].shape[0] == 0:
        return None
    return df[filter]