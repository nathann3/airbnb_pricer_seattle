Airbnb Yearly Revenue Estimator
==============================
web app : https://airbnb-revenue.herokuapp.com

![web_app_demo](reports/figures/web_app_demo.gif "web_app_demo")

# Synopsis
Airbnb has grown exponentially since its inception in 2008 and has proved
itself to be a promising income stream for many hosts. With limited funds as
well as competition from other hosts, prospective hosts must make data-driven
decisions to maximize their listing's earning potential. In this project, we
tackle this very problem by exploring thousands of listings in Seattle as well
as attempt to create a regression model to estimate a new listing's potential
yearly revenue.

# Outcome

The most expensive Airbnb's are located downtown. The most common Airbnb
accommodates 2 and has 1 bed and bath. The median estimated yearly revenue is
$26,171.

With a voting regressor consisting of stacked regressors of XGBoost, KNN, and
linear models, we were able to achieve an MAE of $11,512.01, an 8.4% increase
in performance from a multiple linear regression model. 

![model_comparison](reports/figures/model_comparison.png "model_comparison")

A model is only as good as the data it is trained on.\
We discuss ways to improve performance in Model Performance below.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── app                <- Flask app with HTML/CSS
    ├── data
    │   └── processed      <- The final, canonical data sets for modeling.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks ordered by number. Contains EDA,
    │                          feature engineering, feature selection, and modeling
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

# Purpose / The Airbnb Business

Airbnb has become a thriving business for many entrepreneurs and investors, but
with its exponential growth, the Airbnb market has become competitive. Like the
housing and rental market, prospective Airbnb hosts must make significant
decisions on their listing, whether they already have a place or looking to
buy/rent a place, to maximize their potential earnings. A poor listing will not
yield a good return and thus the investment money will have been wasted.

To maximize their potential earnings, a host's decisions must be data-driven.
Airbnb Yearly Revenue Estimator was created to help hosts find potential
candidate homes/apartments for Airbnb. Using data from thousands of listings,
the web app estimates the yearly revenue a listing could generate, given the
main attributes of a listing (property type, location, beds, etc...). The web
app also features an interactive map with other similar listings with their
attributes and estimated yearly revenue plotted.

The goal is to allow potential hosts to be able to make informed data-driven
decisions before committing to buy/rent a place for Airbnb. This project is
focused on the Seattle area but can be modified to be used in any other major
city.

# Airbnb Data

Airbnb listings were retrieved from Inside Airbnb, an independent organization that provides tools and data to explore
Airbnb's in cities around the world. In our project, we focus only on Seattle, WA. Scraped every month from October 2020
to July 2021, the data provides information about listings as well as their calendar availability throughout the year.

In total, 7166 listings were active within our dataset, but only a fraction of these listings were active every month.
This can be attributed to COVID because people would have to retire their listings after the loss in demand for the
travel industry. New hosts who wanted to test out the Airbnb platform also attribute to the varying number of
continuously active Airbnbs.

Most features in the data set are not required, because our mission is to create a tool for prospective Airbnb hosts to
estimate a listing's yearly revenue. To do this, we removed features that inherently contain no information as well as
features that are not readily available to the prospective host. The features leftover consist of accommodates,
bedrooms, beds, bathrooms, latitude, longitude, and property type.

We cleaned up property type by moving levels that only had a few listings to bigger and broader levels.

There were a couple of missing data points, but most of them were resolved by finding the listing in Airbnb and filling
in the missing values manually.


# yearly_revenue Feature

Airbnb does not release data on the yearly revenue their listings earn. This provides a challenge against estimating
yearly revenue. To work around this, we must create our own response variable from the data available.
The yearly_revenue feature was created by joining the availability calendars of the listings for every month. With every
month joined, we update the availability calendar to estimate the days booked throughout the year. Along with
availability, the calendar data set also provides the price for the day. Adding up all the days and their prices allows
us to estimate a listing's yearly revenue. 

This also provides a problem of really low revenue estimates. Since not all
Airbnb listings are full-time, we remove listings that are not active every
month.

# Model Building

# Model Performance

For our evaluations, we will focus on the mean absolute error (MAE) because it
is not highly sensitive to outliers like root mean squared error (RMSE) is. 
Like housing prices, yearly revenue for listings can have many outliers, where
for our model we want to create a tool that allows prospective hosts to
estimate what their yearly revenue will be. Outliers aren’t particularly bad in
for this type of model This makes MAE more appropriate than RMSE. MAE is also
much more interpretable and thus we will focus on MAE, but also provide other
metrics as well in the final evaluation.

![model_comparison](reports/figures/model_comparison.png "model_comparison")

With a voting regressor consisting of stacked regressors of XGBoost, KNN, and
linear models, we were able to achieve an MAE of $11,512.01, an 8.4% increase
in performance from a multiple linear regression model. 

Due to our limited data from Oct 2020 to July 2021, small dataset, and limited
features, our model does not perform as well as we hoped since $11k is a large
MAE compared to the median estimated yearly income. Model per performance can
definitely be improved by collecting data throughout the year and continuously
updating the model. The model's feature set is not sufficient and needs to be
supplemented with amenities and even pictures to give more information about
the quality of the listing. But as always, we risk overfitting by adding too
many features.

# Flask and Heroku Web App


# Conclusion

