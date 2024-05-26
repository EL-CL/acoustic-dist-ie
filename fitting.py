import os
from fitting_lib import *
from fitting_data import *


class FittingResult:
    def __init__(self, matrix, calibration_dates, calibration_points, prediction_points):
        self.matrix = matrix
        assert calibration_dates.keys() == calibration_points.keys()
        self.ds_calibration = calculate_distances(matrix, calibration_points)
        self.ds_prediction = calculate_distances(matrix, prediction_points)
        self.ds_calibration = list(self.ds_calibration.values())
        self.ds_prediction = list(self.ds_prediction.values())
        self.ts_calibration = list(calibration_dates.values())
        self.params_log = fit_log(self.ds_calibration, self.ts_calibration)
        self.params_exp = fit_exp(self.ds_calibration, self.ts_calibration)
        self.ts_prediction_log = func_log(self.ds_prediction, *self.params_log)
        self.ts_prediction_exp = func_exp(self.ds_prediction, *self.params_exp)
        self.ts_calibration_log = func_log(self.ds_calibration, *self.params_log)
        self.ts_calibration_exp = func_exp(self.ds_calibration, *self.params_exp)
        self.errors_log = calculate_errors(self.ts_calibration, self.ts_calibration_log)
        self.errors_exp = calculate_errors(self.ts_calibration, self.ts_calibration_exp)


input_folder = 'acoustic_distances'
filenames = [filename for filename in os.listdir(input_folder)
             if filename.startswith('DTW-D_by-sum_CMN_') and filename.endswith('.csv')]
results = {}
for filename in filenames:
    feature_name = filename.removesuffix('.csv').split('_')[-1]
    if feature_name in ('GFCC', 'LPCC'):
        # Fitting failed for these features
        continue
    input_path = os.path.join(input_folder, filename)
    results[feature_name] = FittingResult(
        read_matrix(input_path),
        calibration_dates, calibration_points, prediction_points,
    )

print('Feature,RMSE,MAE,NRMSE,MAPE,RMSE,MAE,NRMSE,MAPE')
for feature, result in results.items():
    print(feature, *result.errors_log, *result.errors_exp, sep=',')
print()

selected_features = ['CQCC', 'LFCC', 'MFCC', 'NGCC', 'PNCC', 'logFBank']
print('Feature,Calibration distances...,Predicted dates (log)...,Predicted dates (exp)...')
for feature in selected_features:
    result = results[feature]
    print(feature, *result.ds_calibration, *result.ts_calibration_log, *result.ts_calibration_exp, sep=',')
print()

print('Feature,Prediction distances...,Predicted dates (log)...,Predicted dates (exp)...')
for feature in selected_features:
    result = results[feature]
    print(feature, *result.ds_prediction, *result.ts_prediction_log, *result.ts_prediction_exp, sep=',')
print()

for feature in selected_features:
    result = results[feature]
    print(feature)
    print(get_formula_log(result.params_log))
    print(get_formula_exp(result.params_exp))
    print()
