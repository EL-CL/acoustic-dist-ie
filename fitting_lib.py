import numpy as np
import pandas as pd
from itertools import combinations
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression


def read_matrix(file_path):
    return pd.read_csv(file_path, index_col=0)


def calculate_distance(matrix, language_groups):
    distances = []
    for group_1, group_2 in combinations(language_groups, 2):
        for language_1 in group_1:
            for language_2 in group_2:
                distances.append(matrix[language_1][language_2])
    return np.mean(distances)


def calculate_distances(matrix, points):
    return {k: calculate_distance(matrix, language_groups)
            for k, language_groups in points.items()}


def func_log(d, D, b, T):
    d = np.array(d)
    return (np.log(1 - d / D) + b) * -T


def func_exp(d, a, b):
    d = np.array(d)
    return b * np.exp(a * d)


def get_formula_log(params, get_original=False):
    D, b, T = params
    if get_original:
        return f'-t / {T} = log(1 - d / {D}) + {b}'
    d0 = D * (1 - np.exp(-b))
    r = np.exp(-1000 / T / 2)
    return f't = 1000 log(({D} - d) / ({D} - {d0})) / 2 log({r})'


def get_formula_exp(params):
    a, b = params
    return f't = {b} * exp({a} * d)'


def fit_log(ds, ts):
    ds = np.array(ds)
    ts = np.array(ts)
    params, covariance = curve_fit(
        func_log, ds, ts,
        bounds=((ds.max() + 0.01, -np.inf, -np.inf), np.inf),
    )
    return params.tolist()


def fit_exp(ds, ts):
    ds = np.array(ds)
    ts = np.array(ts)
    model = LinearRegression().fit(ds.reshape((-1, 1)), np.log(ts))
    a = model.coef_[0]
    b = np.exp(model.intercept_)
    return a, b


def calculate_errors(ts, ts_predicted):
    ts = np.array(ts)
    ts_predicted = np.array(ts_predicted)
    # Root sum squared
    rss = np.sum(np.square(ts_predicted - ts))
    # Root mean square error
    rmse = np.sqrt(rss / len(ts))
    # Mean absolute error
    mae = np.sum(np.abs(ts_predicted - ts)) / len(ts)
    # Normalized root mean square error
    nrmse = rmse / (ts.max() - ts.min())
    # Mean absolute percentage error
    mape = np.sum(np.abs(ts_predicted / ts - 1)) / len(ts)
    return rmse, mae, nrmse, mape
