import pandas as pd
import pickle

from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import sklearn.preprocessing
from sklearn_pandas import DataFrameMapper
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
import statsmodels.api as sm
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.model_selection import TimeSeriesSplit

from statsmodels.tools.eval_measures import rmse
from sklearn.ensemble import RandomForestRegressor

import bokeh
import bokeh.plotting
bokeh.io.output_notebook()

def make_dataset():
    """Return pandas dataframe with raw data set"""
    PATH = '/Users/chalpert/Documents/Columbia/Capstone/soccer-capstone/model/data/'
    data = pd.read_csv(PATH + 'Players_Combined_v3.csv')
    data = data.sort_values('season')

    # Make all columsn lowercase
    data.columns = [i.lower() for i in data.columns]

    # Normalize metrics to be on a per 90 minute basis
    data['games'] = data['app_start'] + data['app_sub']
    data['goals_per_90'] = data['goals']/data['mins']*90
    data['assists_per_90'] = data['assists']/data['mins']*90
    data['yel_per_90'] = data['yel']/data['mins']*90
    data['red_per_90'] = data['red']/data['mins']*90
    data['owng_per_90'] = data['owng']/data['mins']*90

    per_games_cols = ['shots_per_game', 'aerialswon', 'tackles', 'inter', 'fouls', 'offside_won', 'clear',
       'drb_past', 'blocks', 'keyp', 'drb', 'fouled', 'offside', 'dispossessed', 'bad_control', 
        'passes_per_game', 'crosses','long_ball', 'through_ball']

    for col in per_games_cols:
        data[col] = data[col]*data['games']/data['mins']*90

    data.rename(columns = {'passes_per_game': 'passes'}, inplace=True)
    # Drop zero values
    data = data[(data['market_val'] > 0) & (data['market_val_prev'] > 0)]
    data['log_market_val'] = np.log(data['market_val'] + 1.)
    data['log_market_val_prev'] = np.log(data['market_val_prev'] + 1.)
    data['market_val_change'] = data['market_val'] - data['market_val_prev']
    data['high_team_net_worth'] = data['team_name'].isin(['real madrid', 'espanyol barcelona', 'fc barcelona', 'fc valencia', 'atletico madrid'])
    return data

def design_matrix(data):
    Y, X = dmatrices("""market_val ~ pos_type 
                                 + pos_type*standardize(rating)
                                 + standardize(goals_per_90)
                                 + standardize(market_val_prev)
                                 + standardize(assists_per_90)
                                 + standardize(passes)
                                 + standardize(red_per_90)
                                 + standardize(tackles)*pos_type
                                 + standardize(long_ball)
                                 + standardize(keyp)
                                 + standardize(aerialswon)
                                 + standardize(inter)
                                 + standardize(pass_success)
                                 + standardize(mins)
                                 + standardize(fouls)
                                 + high_team_net_worth
                                 + standardize(shots_per_game)
                                 """, data)
    return X, Y

def design_matrix_lasso(data):
    Y, X = dmatrices("""market_val ~ pos_type 
                                 + pos_type*standardize(rating)
                                 + standardize(market_val_prev)
                                 + standardize(aerialswon)
                                 + standardize(pass_success)
                                 + standardize(mins)
                                 + high_team_net_worth
                                 + standardize(games)
                                 + standardize(tackles)
                                 + standardize(inter)
                                 + standardize(offside_won)
                                 + standardize(clear)
                                 + standardize(drb_past)
                                 + standardize(fouled)
                                 + standardize(offside)
                                 + standardize(passes)
                                 + standardize(crosses)
                                 + standardize(long_ball)
                                 + standardize(through_ball)
                                 + standardize(goals_per_90)
                                 + standardize(yel_per_90)
                                 + standardize(red_per_90)
                                 + standardize(owng_per_90)
                                 + standardize(shots_per_game)
                                 """, data)
    return X, Y

def design_matrix_2(data):
    Y, X = dmatrices("""market_val ~ pos_type 
                                 + standardize(rating)
                                 + standardize(goals_per_90)
                                 + standardize(market_val_prev)
                                 + standardize(assists_per_90)
                                 + standardize(passes)
                                 + standardize(red_per_90)
                                 + standardize(tackles)
                                 + standardize(long_ball)
                                 + standardize(keyp)
                                 + standardize(aerialswon)
                                 + standardize(inter)
                                 + standardize(pass_success)
                                 + standardize(mins)
                                 + standardize(fouls)
                                 + high_team_net_worth
                                 + standardize(shots_per_game)
                                 """, data)

    # Y, X = dmatrices("""market_val ~ 
 #                                 standardize(market_val_prev)
 #                                 """, data)

    unused = """
    + standardize(owng_per_90)
    + standardize(yel_per_90)
    + standardize(blocks)
    + standardize(clear)
    + standardize(bad_control)
    + standardize(through_ball)
    + standardize(shots_per_game)*pos_type
                              """
                                 
    return X, Y

def design_matrix_baseline(data):
    Y, X = dmatrices("""market_val ~ market_val_prev""", data)                             
    return X, Y


def design_matrix_all(data):
    Y, X = dmatrices("""market_val ~ pos_type 
                                 + pos_type*standardize(rating)
                                 + standardize(market_val_prev)
                                 + standardize(aerialswon)
                                 + standardize(pass_success)
                                 + standardize(mins)
                                 + high_team_net_worth
                                 + standardize(games)
                                 + standardize(tackles)
                                 + standardize(inter)
                                 + standardize(fouls)
                                 + standardize(offside_won)
                                 + standardize(clear)
                                 + standardize(drb_past)
                                 + standardize(blocks)
                                 + standardize(owng)
                                 + standardize(keyp)
                                 + standardize(drb)
                                 + standardize(fouled)
                                 + standardize(offside)
                                 + standardize(dispossessed)
                                 + standardize(bad_control)
                                 + standardize(passes)
                                 + standardize(crosses)
                                 + standardize(long_ball)
                                 + standardize(through_ball)
                                 + standardize(goals_per_90)
                                 + standardize(assists_per_90)
                                 + standardize(yel_per_90)
                                 + standardize(red_per_90)
                                 + standardize(owng_per_90)
                                 + standardize(shots_per_game)
                                 """, data)
    return X, Y


def vifs(X):
    cols = X.design_info.column_names
    X_array = np.asarray(X)
    for i, c in enumerate(cols):
        vif = variance_inflation_factor(X_array, i)
        if vif >= 15:
            print '*******', c, vif
        else:
            print c, vif

def sm_fit(X, Y, alpha=None, L1_wt=0.0):
    actual_v_predicted_plot = bokeh.plotting.figure(tools=['save'], x_axis_type='log', y_axis_type='log')
    resid_v_actual_plot = bokeh.plotting.figure(tools=['save'])
    cv_rmse = []
    
    ts = TimeSeriesSplit(7)
    for train_index, test_index in ts.split(X):
        X_train, Y_train = X[train_index], Y[train_index]
        X_test, Y_test = X[test_index], Y[test_index]
        model = sm.OLS(Y_train, X_train)

        if alpha is None:
            reg_results = model.fit()
        else:
            reg_results = model.fit_regularized(alpha = alpha, L1_wt=L1_wt)
        sm_plot_actual_v_predicted(actual_v_predicted_plot, reg_results, X_test, Y_test[:, 0])
        sm_plot_resid_v_actual(resid_v_actual_plot, reg_results, X_test, Y_test[:, 0])
        cv_rmse.append(rmse(reg_results.predict(X_test), Y_test[:, 0]))
    cv_rmse = pd.Series(cv_rmse, name='rmse').reset_index()
    return reg_results, resid_v_actual_plot, actual_v_predicted_plot, cv_rmse


def sm_forest_fit(X, Y, tuning_parameters=None):
    if tuning_parameters is not None:
        max_depth, min_samples_leaf, n_estimators, max_features = tuning_parameters
        max_depth, min_samples_leaf, n_estimators, max_features= int(round(max_depth)), int(round(min_samples_leaf)), int(round(n_estimators)), max_features
    else:
        max_depth = 3
        min_samples_leaf = 1
        n_estimators = 10
        max_features = 'auto'
        
    actual_v_predicted_plot = bokeh.plotting.figure(tools=['save'], x_axis_type='log', y_axis_type='log')
    resid_v_actual_plot = bokeh.plotting.figure(tools=['save'])
    cv_rmse = []
    
    ts = TimeSeriesSplit(7)
    for train_index, test_index in ts.split(X):
        X_train, Y_train = X[train_index], Y[train_index]
        X_test, Y_test = X[test_index], Y[test_index]
        model = sm.OLS(Y_train, X_train)
        reg_results = RandomForestRegressor(max_depth=max_depth, min_samples_leaf=min_samples_leaf, n_estimators=n_estimators, max_features=max_features, n_jobs=-1)
        reg_results.fit(X, Y)
        sm_plot_actual_v_predicted(actual_v_predicted_plot, reg_results, X_test, Y_test[:, 0])
        sm_plot_resid_v_actual(resid_v_actual_plot, reg_results, X_test, Y_test[:, 0])
        cv_rmse.append(rmse(reg_results.predict(X_test), Y_test[:, 0]))
    cv_rmse = pd.Series(cv_rmse, name='rmse').reset_index()
    return reg_results, resid_v_actual_plot, actual_v_predicted_plot, cv_rmse

def sm_optimize_forest(x, X_data, Y_data):
    return sm_forest_fit(X_data, Y_data, x)[3].mean().values[1]

def sm_optimize(x, X_data, Y_data, alpha=None, L1_wt=0.0):
    return sm_fit(X_data, Y_data, x, L1_wt)[3].mean().values[1]

def plot_rmse(cv_rmse):
    rmse_fig = bokeh.plotting.figure()
    rmse_fig.line(cv_rmse['index'], cv_rmse['rmse'], color='black')
    bokeh.io.show(rmse_fig)
    print cv_rmse['rmse'].mean()



def sm_plot_actual_v_predicted(fig, fitted_model, X, Y_actual):
    fig.scatter(fitted_model.predict(X) , Y_actual , alpha=.3)
    min_max = Y_actual.min(), Y_actual.max()
    actual_range = zip(min_max, min_max)
    # fig.line(min_max, min_max, color='black')


def sm_plot_resid_v_actual(fig, fitted_model, X, Y_actual):
    res = Y_actual - fitted_model.predict(X)
    fig.scatter(Y_actual / 1000000, res / 1000000, alpha=.3)

def plot_actual_v_predicted(actual_v_predicted_plot):
    actual_v_predicted_plot.xaxis.axis_label = 'Predicted Market Value (pounds)'
    actual_v_predicted_plot.yaxis.axis_label = 'Actual Market Value (pounds)'
    actual_v_predicted_plot.x_range.start = 0
    actual_v_predicted_plot.y_range.start = 0
    # actual_v_predicted_plot.toolbar_location = None
    actual_v_predicted_plot.title.text = 'Actual v Predicted Market Value (Log Scale)'
    bokeh.io.show(actual_v_predicted_plot)
    return actual_v_predicted_plot

def plot_resid_v_actual(resid_v_actual_plot):
    resid_v_actual_plot.xaxis.axis_label = 'Actual Market Value (pounds, millions)'
    resid_v_actual_plot.yaxis.axis_label = 'Residual (pounds, millions)'
    resid_v_actual_plot.x_range.start = 0
    # resid_v_actual_plot.toolbar_location = None
    resid_v_actual_plot.title.text = 'Residual v Actual'
    bokeh.io.show(resid_v_actual_plot)
    return resid_v_actual_plot






# def ridge(data):

#     X_cols = [ 'goals', 'tackles', 'preferred_foot', 'pos_type', 
#      'mins', 'shots_per_game', 'pass_success', 'passes', 'keyp']
#     X = data[X_cols]
#     # Y = data['market_val']
#     Y = np.log(data['market_val'] + 1.)

#     mapper = DataFrameMapper([
#                 #(['age'], sklearn.preprocessing.StandardScaler(), {'alias': 'age_scaled'}),
#                 #(['weight'], sklearn.preprocessing.StandardScaler(), {'alias': 'weight_scaled'}),
#                 # (['height'], sklearn.preprocessing.StandardScaler(), {'alias': 'height_scaled'}), # Collinear with weight, age, Rating
#                 (['goals'], sklearn.preprocessing.StandardScaler(), {'alias': 'goals_scaled'}),
#                 (['tackles'], sklearn.preprocessing.StandardScaler(), {'alias': 'tackles_scaled'}),
#                 # ('preferred_foot', sklearn.preprocessing.LabelBinarizer(), {'alias': 'foot'}),
#                 ('pos_type', sklearn.preprocessing.LabelBinarizer(), {'alias': 'position'}),
#                 # ('transfer_type', sklearn.preprocessing.LabelBinarizer(), {'alias': 'transfer_type'}),
#                 # (['rank_in_season'], sklearn.preprocessing.StandardScaler(), {'alias': 'rank_in_season'}),
#                 (['mins'], sklearn.preprocessing.StandardScaler(), {'alias': 'mins'}),
#                 # (['Rating'], sklearn.preprocessing.StandardScaler(), {'alias': 'rating'}),
#                 (['pass_success'], sklearn.preprocessing.StandardScaler(), {'alias': 'pass_success'}),
#                 (['shots_per_game'], sklearn.preprocessing.StandardScaler(), {'alias': 'shots_per_game'}),
#                 (['keyp'], sklearn.preprocessing.StandardScaler(), {'alias': 'keyp'}),




#     ])

#     model_pipeline = Pipeline(steps=[
#         ('features', mapper),
#         ('model', Ridge())
#     ])

#     param_grid = {
#         'model__alpha': [.1, .5, 1., 10., 20., 50.]
#     }
#     model = GridSearchCV(model_pipeline, param_grid, n_jobs=-1,
#                          verbose=1, scoring='neg_mean_squared_error',
#                          cv=TimeSeriesSplit(5))
#     fitted_model = model.fit(X, Y)
#     return fitted_model, X, Y

# def save_fitted_model(model):
#     pickle.dump(model, open("model.p","wb"))

# def load_fitted_model(filename):
#     return pickle.load(open(filename, "rb"))


# def resid(fitted_model, X, Y_actual):
#     return Y_actual - fitted_model.best_estimator_.predict(X)

def hist(data):
    hist, edges = np.histogram(data, bins=50, density=True)
    f = bokeh.plotting.figure()
    f.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")
    bokeh.io.show(f)
    return f

# def model_parameters(fitted_model):
#     return fitted_model.best_estimator_.named_steps['model']

# def main():
#     data = make_dataset()
#     fitted_model = ridge(data)
#     return fitted_model