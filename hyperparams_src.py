import sklearn.metrics as metrics
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import grid_search_forecaster
from sklearn.ensemble import RandomForestRegressor


class modelOptimization():
    def __init__(self, forecaster, df):
        self.forecaster = forecaster
        self.lag_grid = [12, 36]
        self.param_grid = {'n_estimators': [500, 1000]}
        self.df = df


    def check_params(self):
        results_grid = grid_search_forecaster(forecaster=self.forecaster,
                                                   y=self.df['concentration'],
                                                   param_grid = self.param_grid,
                                                   lags_grid = self.lag_grid,
                                                   steps = 12,
                                                   refit = True,
                                                   metric = 'mean_absolute_error',
                                                   initial_train_size = int(len(self.df)*0.5),
                                                   return_best = True,
                                                   verbose = False,
                                                   fixed_train_size = False
                                                   )

        return(results_grid)

    def validate_results(y, y_pred):
        import sklearn.metrics as metrics
        import pandas as pd

        var = metrics.explained_variance_score(y, y_pred)
        mae = metrics.mean_absolute_error(y, y_pred)
        mse = metrics.mean_squared_error(y, y_pred)
        r2 = metrics.r2_score(y, y_pred)

        l1 = ['variance','mae','mse','r2']
        l2 = [var, mae, mse, r2]

        metric_df = pd.DataFrame(list(zip(l1,l2)))
        metric_df .columns = ['metric','value']

        return(metric_df)