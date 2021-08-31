import math
import os
import re
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

def clean_data(df, fill=False):
    """
    Cleans listing data. Getting rid of many features that are unnecessary for
    predicting yearly revenue.
    """
    dropped = df.drop(['listing_url', 'scrape_id', 'last_scraped',
                       'picture_url', 'host_thumbnail_url',
                       'calendar_last_scraped', 'has_availability'], axis=1)
    dropped = dropped.drop(['neighbourhood', 'bathrooms', 'calendar_updated'], axis=1)
    dropped['price'] = dropped['price'].replace('[\$,]', '', regex=True).astype(float)

    dropped['bathrooms_text'] = dropped['bathrooms_text'].replace(
        ['Shared half-bath', 'Half-bath', 'Private half-bath'], '0.5 baths').fillna('0')
    dropped['bathrooms_text'] = [''.join(re.findall('\d*\.?\d+', item)) for item in
                                       dropped['bathrooms_text']]
    dropped['bathrooms_text'] = dropped['bathrooms_text'].astype(float)

    if fill:
        dropped = fill_df(dropped)
    return dropped

def fill_df(df):
    """
    Fill missing bedrooms with value from beds, and vice versa.
    If still missing fill with 0 and 1 respectively.
    """
    filled = df.copy()
    filled['bedrooms'].fillna(filled['beds'], inplace=True)
    filled['beds'].fillna(filled['bedrooms'], inplace=True)
    filled['bedrooms'].fillna(0, inplace=True)
    filled['beds'].fillna(1, inplace=True)
    return filled

def subset(df, property_type, accommodates, bedrooms):
    """
    Filters listings DataFrame by property type, number of accommodations and
    bedrooms.
    """
    filter = (df.property_type == property_type) & (df.accommodates == accommodates) & (df.bedrooms == bedrooms)
    if df[filter].shape[0] == 0:
        return None
    return df[filter]