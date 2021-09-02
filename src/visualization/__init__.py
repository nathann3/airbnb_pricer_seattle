import folium
import numpy as np


def seattle_map(location=[47.61807, -122.42945], zoom_start=12):
    """
    Creates a Folium map of Seattle by default.
    """
    map = folium.Map(location=location,
               tiles='Stamen Terrain',
               zoom_start=zoom_start,
               min_zoom=12,
               )

    return map

def place_listings(df, m, preds=None, radius=5):
    """
    Place listings as markers on a map. Tooltip include listing information as
    well as predicted yearly revenue.
    """
    if type(preds) is np.ndarray:
        for i in range(len(df)):
            folium.CircleMarker(
                location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
                tooltip=('Property Type: {}<br>'
                         'Accommodates:  {}<br>'
                         'Bedrooms: {}<br>'
                         'Beds: {}<br>'
                         'Bathrooms: {}<br>'
                         'Estimated Yearly Revenue: ${:,.2f}').format(df.iloc[i]['property_type_cleansed'],
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
                         'Bathrooms: {}').format(df.iloc[i]['property_type_cleansed'],
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