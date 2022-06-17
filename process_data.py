import pandas as pd
import numpy as np


class processData():
    def __init__(self, df):

        # drop any nan values
        # df = df[~df.isin(['NaN', 'NaT', np.nan]).any(axis=1)]

        # drop any erroneous values where concentration is below zero or above 100
        df = df[(df['concentration'] >= 0) | (df['concentration'] <= 100)]

        # remove values not in arctic (below 65 lat)
        df = df[df['lat'] >= 65.0]

        # create datetime columns
        datetimes = pd.to_datetime(df['time'])

        df['date'] = datetimes.dt.date
        df['month'] = datetimes.dt.month
        df['year'] = datetimes.dt.year

        # remove years before 1950; data is poor
        # reduced dataset to > 1980 for demonstration purposes
        df = df[df['year'] >= 1980]

        # dataframe now contains all month and year data after 1980 for all coordinates
        self.df = df

    def select_year(self, yr, month):
        # this function returns concentration of all coordinate pairs for a year/month
        # used to generate heatmap
        print(str(yr) + " " + str(month))
        df = self.df

        df = df[df['year'] == yr]  # make df based on year of interest
        df = df[df['month'] == month]  # and month of interest

        # returned df contains data for all coordinates at given year and month
        return(df)

    def prediction_df(self, lat, lon):
        pred_df = self.df
        pred_df['coords'] = list(zip(pred_df.lat, pred_df.lon))  # create coordinates list
        pred_df = pred_df.groupby(['coords', 'date']).value_counts().reset_index()  # group by coordinates and dates

        pred_df = pred_df[pred_df['coords'] == (lat, lon)]  # get df of chosen lat lon coordinates
        pred_df.drop(['lat', 'lon', 'month', 'year'], axis=1, inplace=True)  # drop unneeded columns
        pred_df.index = pd.to_datetime(pred_df['date'])  # convert index to datetime for processing

        # returns df with all month and year data for single set of coordinates
        return(pred_df)

    def mass_prediction(self):
        pred_df = self.df
        pred_df = pred_df.groupby(['coords', 'date']).value_counts().reset_index()

        pred_df.drop(['lat', 'lon', 'month', 'year'], axis=1, inplace=True)  # drop unneeded columns
        pred_df.index = pd.to_datetime(pred_df['date'])  # convert index to datetime for processing

        # returns df with all month and year data for set of coordinates in passed df
        return(pred_df)

    def get_averages(self):
        df = self.df
        df['coords'] = list(zip(df.lat, df.lon))
        df = df.groupby(['year']).mean().reset_index()
        df.drop(index=df.index[-1],
                axis=0,
                inplace=True)  # drop last entry because 2022 not complete yet/skews average
        return(df)






