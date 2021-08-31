from utils import clean_data, distance, subset, prep_df, place_listings

import folium
import numpy as np
import pandas as pd

from flask import Flask, render_template, request, jsonify
from geopy import Nominatim
from joblib import load


app = Flask(__name__)

# Download and clean
raw_listings = pd.read_csv('listings.csv.gz')
drop_listings = clean_data(raw_listings)

@app.route('/')
def hello_world():
    # Map
    m = folium.Map(location=[47.61807, -122.42945],
                   tiles='Stamen Terrain',
                   zoom_start=12,
                   min_zoom=12,
                   )

    place_listings(drop_listings, m)
    html_map = m._repr_html_()
    html_map = html_map[:73] + '100vh' + html_map[74:]
    return render_template('land.html', cmap=html_map)

@app.route('/calculate_result')
def calculate():
    model = load('model.joblib')
    accommodates = int(request.args.get('accommodates'))
    bedrooms = int(request.args.get('bedrooms'))
    beds = int(request.args.get('beds'))
    bathrooms = float(request.args.get('bathrooms'))
    address = request.args.get('address')
    property_type = ' '.join(request.args.get('property_type').split("_"))[1:-1]

    if accommodates < 1 or accommodates > 16 \
            or bedrooms < 0 or bedrooms > 8 \
            or beds < 0 or beds > 16 \
            or bathrooms < 0 or bathrooms > 6:

        return jsonify({"result": "Error"})

    input_df = process_input(accommodates, bedrooms, beds, bathrooms, address, property_type)
    output = round(model.predict(input_df)[0], 2)

    m = folium.Map(location=[input_df.latitude, input_df.longitude],
                   tiles='Stamen Terrain',
                   zoom_start=14,
                   min_zoom=12,
                   )

    folium.Marker(
        location=[input_df.latitude, input_df.longitude],
        tooltip=('Property Type: {}<br>'
                 'Accommodates:  {}<br>'
                 'Bedrooms: {}<br>'
                 'Beds: {}<br>'
                 'Bathrooms: {}').format(property_type,
                                         accommodates,
                                         bedrooms,
                                         beds,
                                         bathrooms
                                         ),
        icon=folium.DivIcon(
            html='<p class="marker" style="color: #FF5A5F; font-size: 42px;">'
                 '<i class="fa fa-home" aria-hidden="true"></i>'
                 '</p>')
    ).add_to(m)

    sub = subset(drop_listings, property_type, accommodates, bedrooms)
    if sub is None:
        sub_preds = np.array(00000.00)
        sub = ''
    else:
        preped_df = prep_df(sub)
        sub_preds = model.predict(preped_df)
        place_listings(sub, m, preds=sub_preds, radius=7)

    html_map = m._repr_html_()
    html_map = html_map[:73] + '100vh' + html_map[74:]

    median_rev = round(np.median(sub_preds), 2)
    median_rev = '${:,.2f}'.format(median_rev)
    return jsonify({"result": '${:,.2f}'.format(output),
                    "map": html_map,
                    "n_listings": len(sub),
                    "attr": (property_type, accommodates, bedrooms, median_rev)})

def process_input(accommodates, bedrooms, beds, bathrooms, address, property_type):
    # Get coordinates
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(address)

    # # Calculate distance from downtown
    # downtown_coord = (47.614668, -122.344921)
    # distance_dt = distance(downtown_coord[0], downtown_coord[1], location.latitude, location.longitude)
    #
    # features = [[location.latitude, location.longitude, property_type,
    #                      accommodates, bathrooms, bedrooms, beds, distance_dt]]
    # columns = ['latitude', 'longitude', 'property_type', 'accommodates',
    #    'bathrooms_text', 'bedrooms', 'beds', 'distance_dt']

    features = [[location.latitude, location.longitude, property_type,
                         accommodates, bathrooms, bedrooms, beds]]
    columns = ['latitude', 'longitude', 'property_type', 'accommodates',
       'bathrooms_text', 'bedrooms', 'beds']
    df = pd.DataFrame(features, columns=columns)

    return df


if __name__ == '__main__':
    app.run(debug=True)