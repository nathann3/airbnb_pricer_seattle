import folium
import numpy as np
import re


def clean_data(df):
        drop_listings = df.drop(['listing_url', 'scrape_id', 'last_scraped',
                                           'picture_url', 'host_thumbnail_url',
                                           'calendar_last_scraped', 'has_availability'], axis=1)
        drop_listings = drop_listings.drop(['neighbourhood', 'bathrooms', 'calendar_updated'], axis=1)
        drop_listings['price'] = drop_listings['price'].replace('[\$,]', '', regex=True).astype(float)

        drop_listings['bathrooms_text'] = drop_listings['bathrooms_text'].replace(
            ['Shared half-bath', 'Half-bath', 'Private half-bath'], '0.5 baths').fillna('0')
        drop_listings['bathrooms_text'] = [''.join(re.findall('\d*\.?\d+', item)) for item in
                                           drop_listings['bathrooms_text']]
        drop_listings['bathrooms_text'] = drop_listings['bathrooms_text'].astype(float)

        # fill bedrooms with value from beds, vice versa
        # if still missing fill with 0 and 1
        drop_listings['bedrooms'].fillna(drop_listings['beds'], inplace=True)
        drop_listings['beds'].fillna(drop_listings['bedrooms'], inplace=True)
        drop_listings['bedrooms'].fillna(0, inplace=True)
        drop_listings['beds'].fillna(1, inplace=True)

        return drop_listings

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

def subset(df, property_type, accommodates, bedrooms):
    filter = (df.property_type == property_type) & (df.accommodates == accommodates) & (df.bedrooms == bedrooms)
    if df[filter].shape[0] == 0:
        print('IT IS 0')
        return None
    return df[filter]

def prep_df(df):
    cols = ['latitude', 'longitude', 'property_type', 'accommodates',
          'bathrooms_text', 'bedrooms', 'beds',]
    filled = df[cols].copy()
    filled['bedrooms'].fillna(filled['beds'], inplace=True)
    filled['beds'].fillna(filled['bedrooms'], inplace=True)
    filled['bedrooms'].fillna(0, inplace=True)
    filled['beds'].fillna(1, inplace=True)
    return filled


def place_listings(df, m, preds=None, radius=5):
    if type(preds) is np.ndarray:
        for i in range(len(df)):
            folium.CircleMarker(
                location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
                tooltip=('Property Type: {}<br>'
                         'Accommodates:  {}<br>'
                         'Bedrooms: {}<br>'
                         'Beds: {}<br>'
                         'Bathrooms: {}<br>'
                         'Estimated Yearly Revenue: ${:,.2f}').format(df.iloc[i]['property_type'],
                                                                df.iloc[i]['accommodates'],
                                                                int(df.iloc[i]['bedrooms']),
                                                                int(df.iloc[i]['beds']),
                                                                df.iloc[i]['bathrooms_text'],
                                                                preds[i]
                                                 ),
                radius=radius,
                color='#00A699',
                fill_color='#FF5A5F',
                fill_opacity=1,
                opacity=0.5,
                weight=1,
            ).add_to(m)

    else:
        for i in range(len(df)):
            folium.CircleMarker(
                location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
                tooltip=('Property Type: {}<br>'
                         'Accommodates:  {}<br>'
                         'Bedrooms: {}<br>'
                         'Beds: {}<br>'
                         'Bathrooms: {}').format(df.iloc[i]['property_type'],
                                                 df.iloc[i]['accommodates'],
                                                 int(df.iloc[i]['bedrooms']),
                                                 int(df.iloc[i]['beds']),
                                                 df.iloc[i]['bathrooms_text']
                                                 ),
                radius=radius,
                color='#00A699',
                fill_color='#FF5A5F',
                fill_opacity=1,
                opacity=0.5,
                weight=1,
            ).add_to(m)