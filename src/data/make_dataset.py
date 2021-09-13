# -*- coding: utf-8 -*-
import click
import logging
import numpy as np
import os
import pandas as pd
import re

from collections import Counter
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from src.data import download_data


def main():
    """
    Downloads raw data.
    """
    logger = logging.getLogger(__name__)
    logger.info('downloading raw data')

    # For use for another city, replace with links for that city.
    calendar_links = [
        'http://data.insideairbnb.com/united-states/wa/seattle/2020-10-25/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2020-11-12/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2020-12-23/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-01-23/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-02-21/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-03-18/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-04-23/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-06-30/data/calendar.csv.gz',
        'http://data.insideairbnb.com/united-states/wa/seattle/2021-07-14/data/calendar.csv.gz'
    ]

    logger.info('combining all months')

    # Download all calendar data sets.
    data_frames = {}
    for link in calendar_links:
        date = re.search(r'\d{4}-\d{2}-\d{2}', link)[0]
        fp = os.path.join('data', 'raw', f'{date}_calendar.csv.gz')
        download_data(fp, link)
        df = pd.read_csv(fp, parse_dates=['date'])
        data_frames[date] = df

    # Combine all listings data scraped each month.
    df_columns = next(iter(data_frames.values())).columns
    combined_df = pd.DataFrame(columns=df_columns)
    for df in data_frames.values():
        df_copy = df.copy()
        combined_df = pd.concat([combined_df, df_copy]).drop_duplicates(['listing_id', 'date'], keep='last')

    # Get only listings that appear every month
    ids = []
    for df in data_frames.values():
        ids.extend(df.listing_id.unique())
    greater_months = {k: v for k, v in Counter(ids).items() if v >= 9}
    combined_df.index = combined_df.listing_id
    full_time = combined_df.loc[greater_months].copy().reset_index(drop=True)

    # Export data
    fp = os.path.join('data', 'interim', 'full_time.pkl')
    pd.to_pickle(full_time, fp)

    logger.info('Download listings data set')
    url = 'http://data.insideairbnb.com/united-states/wa/seattle/2020-10-25/data/listings.csv.gz'
    date = re.search(r'\d{4}-\d{2}-\d{2}', url)[0]
    fp = os.path.join('data', 'raw', f'{date}listings.csv.gz')
    download_data(fp, url)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
