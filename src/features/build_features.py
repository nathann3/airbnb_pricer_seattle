import logging
import numpy as np
import os
import pandas as pd
import re

from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from src.features import clean_data, distance

def main():
    """
    Cleans features and generate the final data set
    """
    logger = logging.getLogger(__name__)
    logger.info('cleaning data')

    fp = os.path.join('data', 'interim', 'full_time.pkl')
    full_time = pd.read_pickle(fp)

    # Convert available to boolean and price to float
    full_time['available'] = full_time.available == 't'
    full_time['price'] = full_time.price.replace('[\$,]', '', regex=True).astype(float)

    # Create booked column
    full_time['booked'] = np.logical_xor(full_time.available, 1).astype(int)

    # Change date depending on your own data's year window
    sub = full_time[full_time.date <= '2021-10-24']
    booked = sub[sub.available == False].groupby('listing_id').sum()
    booked['occupancy_rate'] = booked.booked / 365
    booked['avg_revenue_nightly'] = booked.price / 365
    booked['avg_revenue_monthly'] = booked.price / 12
    booked = booked.rename(columns={"price": "yearly_revenue"})
    booked['avg_booked_price'] = sub[sub.available == False].groupby('listing_id').mean().price

    url = 'http://data.insideairbnb.com/united-states/wa/seattle/2020-10-25/data/listings.csv.gz'
    date = re.search(r'\d{4}-\d{2}-\d{2}', url)[0]
    fp = os.path.join('data', 'raw', f'{date}listings.csv.gz')
    listings = pd.read_csv(fp)
    listings = listings.rename(columns={"id": "listing_id"})

    # Merge calendar and listings data.
    merged = pd.merge(listings, booked.reset_index(), on='listing_id', how='right')

    merged = clean_data(merged, fill=True)

    # Add distance from downtown (Replace with your city's coordinates)
    downtown_coord = (47.614668, -122.344921)
    merged['distance_dt'] = distance(downtown_coord[0], downtown_coord[1], merged.latitude, merged.longitude)

    # Clean property_type.
    merged['property_type_cleansed'] = merged['property_type']
    merged['property_type_cleansed'] = merged['property_type_cleansed'].replace(
        ['Entire serviced apartment', 'Entire loft'], 'Entire apartment')
    merged['property_type_cleansed'] = merged['property_type_cleansed'].replace(
        ['Entire cottage', 'Entire bungalow', 'Tiny house', 'Entire cabin', 'Entire villa'], 'Entire house')
    merged['property_type_cleansed'] = merged['property_type_cleansed'].replace(
        ['Room in boutique hotel', 'Private room in bed and breakfast'], 'Entire guest suite')
    merged['property_type_cleansed'] = merged['property_type_cleansed'].replace(
        ['Private room in townhouse', 'Private room in bungalow'], 'Private room in house')
    merged['property_type_cleansed'] = merged['property_type_cleansed'].replace(
        ['Private room in guest suite', 'Private room in apartment', 'Room in aparthotel',
         'Private room in condominium', 'Private room in serviced apartment', 'Private room in guesthouse',
         'Private room in loft', 'Private room in cottage', 'Private room in villa', 'Shared room',
         'Shared room in loft', 'Shared room in house', 'Shared room in apartment', 'Boat', 'Private room in treehouse',
         'Private room in tiny house', 'Private room in earth house', 'Camper/RV', 'Yurt'], 'Other')

    cols = [
        'neighbourhood_group_cleansed', 'latitude', 'longitude',
        'property_type', 'room_type', 'accommodates',
        'bathrooms_text', 'bedrooms', 'beds', 'avg_booked_price', 'occupancy_rate',
        'yearly_revenue', 'distance_dt', 'property_type_cleansed'
    ]

    fp = os.path.join('data', 'interim', 'yearly_revenue.pkl')
    pd.to_pickle(merged[cols], fp)

    # Create final data set
    cols = [
        'latitude', 'longitude',
        'accommodates', 'bathrooms_text', 'bedrooms',
        'beds', 'yearly_revenue', 'property_type_cleansed'
    ]

    fp = os.path.join('data', 'processed', 'yearly_revenue.pkl')
    pd.to_pickle(merged[cols], fp)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()