
from skforecast.ForecasterAutoreg import ForecasterAutoreg
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class predictIce():
    def __init__(self, df):
        # set steps to 12 to train on all but last year
        self.steps = 12  # months
        self.df = df

        self.traindf = df[:-self.steps]  # training dataset
        self.testdf = df[-self.steps:]  # testing dataset of 1 year

    def forecaster(self):
        # for a single location, not currently called
        # call random forests regressor to make forecast
        forecasting = ForecasterAutoreg(regressor=RandomForestRegressor(random_state=123, n_estimators=500), lags=12)

        # fit model to training data
        forecasting.fit(y=self.traindf['concentration'])

        # uncomment following lines to perform hyperparameter tuning: already done
        # hp = hyperparameterOptimization(forecasting, self.traindf)
        # tunedparams = hp.check_params()

        # make dataframe of predicted values for next year
        predictions = pd.DataFrame(forecasting.predict(steps=self.steps))

        from pandas.tseries.offsets import DateOffset  # use DateOffset to create additional entries in df
        ts = self.df.index[-1]  # get last timeseries entry in dataset

        newdates = [] # create list to hold new dates
        for i in range(1, 13, 1):  # range from 1 (january) to 12 (december)
            new_d = ts + DateOffset(months=i)  # get new date by adding months to last entry in df ts
            newdates.append(new_d)  # add to list
        predictions.index = newdates  # set new dates as index of predictions dataframe
        predictions.to_csv('predictedValues.csv')  # save predictions to csv

    def predict_concentration(self):
        # forecasting with RandomForestRegressor, lags = 12 for last year as prediction data
        forecasting = ForecasterAutoreg(regressor=RandomForestRegressor(random_state=123), lags=12)
        # set random_state to 123 to repeat results and check for other inconsistencies
        # fit model
        forecasting.fit(y=self.traindf['concentration'])

        # return the last predicted value (1 year in future)
        q = forecasting.predict(12)
        return(q.iloc[-1], forecasting)

