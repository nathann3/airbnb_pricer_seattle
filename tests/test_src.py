from unittest import TestCase
from tempfile import TemporaryDirectory
from src import data, features
from app import app

import pandas as pd
import numpy as np


class FeaturesTests(TestCase):
    def test_distance(self):
        """Ensure the straight line distance (mi) calculation is correct"""
        la_coords = 34.052235, -118.243683
        nyc_coords = 40.730610, -73.935242
        straight_line_dist = features.distance(la_coords[0], la_coords[1],
                                               nyc_coords[0], nyc_coords[1])

        self.assertAlmostEqual(2448.15, straight_line_dist, -1)

class DataTests(TestCase):
    def setUp(self):
        """Generate test DataFrame"""
        super(DataTests, self).setUp()
        columns = ["latitude", "longitude", "accommodates",
                   "bathrooms_text", "bedrooms", "beds",
                   "price", "property_type_cleansed"]

        self.df = pd.DataFrame(
    {
        "latitude": [34.052235, 34.052235, 40.730610, 40.730610],
        "longitude": [-118.243683, -118.243683, -73.935242, -73.935242],
        "accommodates": [1, 1, 2, 2],
        "bathrooms_text": ["Half-bath", "Private half-bath", "Shared half-bath", "1"],
        "bedrooms": [np.nan, 2, 3, np.nan],
        "beds": [1, 2, np.nan, np.nan],
        "price": ['$123', '$456', '$789', '$321'],
        "property_type_cleansed": [
            "Entire apartment",
            "Entire condominium",
            "Entire house",
            "Entire house",
        ],
    },
    columns=columns,
)
    def test_fill_df(self):
        """Ensure all missing data are filled"""
        filled = features.fill_df(self.df)
        self.assertEqual(0, filled.isnull().sum().sum())
        self.assertTrue(([1, 2, 3, 0] == filled.bedrooms).all())
        self.assertTrue(([1, 2, 3, 1] == filled.beds).all())

    def test_clean_data(self):
        """Ensure price and bathrooms_test is formated correctly"""
        cleaned = features.clean_data(self.df)
        self.assertEqual(np.float64, cleaned.price.dtype)
        self.assertEqual(np.float64, cleaned.bathrooms_text.dtype)
        self.assertTrue(([0.5, 0.5, 0.5, 1] == cleaned.bathrooms_text).all())

    def test_subset(self):
        """Ensure the right listings are filtered through"""
        sub = data.subset(self.df, "Entire house", 2, 3)
        self.assertEqual("$789", sub.price.values)

    def test_no_subset(self):
        """Ensure returns None if no listings were found"""
        sub = data.subset(self.df, "Entire apartment", 2, 3)
        self.assertEqual(None, sub)

class AppTests(TestCase):
    def test_process_input(self):
        """Ensure the correct DataFrame in generated given the input"""
        columbus_sf_coords = 37.7964, -122.4049
        columbus_sf_address = "128 Columbus Ave, San Francisco, CA 94133, US"
        df = app.process_input(2, 4, 8, 16, columbus_sf_address, "Entire apartment")
        self.assertAlmostEqual(columbus_sf_coords[0],  df.latitude.values[0], 3)