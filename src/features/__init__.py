import numpy as np
import re

def distance(lat1, lon1, lat2, lon2):
    """Calculate distance in miles between two coordinates"""
    # approximate radius of earth in miles
    R = 3959

    lat1 = lat1 * np.pi / 180.0
    lon1 = np.deg2rad(lon1)
    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)

    d = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2

    return 2 * R * np.arcsin(np.sqrt(d))

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
