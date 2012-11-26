import sys
sys.path.append('../../../')

from pycast.common.timeseries import TimeSeries
from pycast.methods import HoltWintersMethod
from pycast.optimization import GridSearch
from pycast.errors import SymmetricMeanAbsolutePercentageError as SMAPE

with open('MC1001_season_indices.csv','r') as season_indices:
	season_indices.readline() #header
	with open('MC1001.csv', 'r') as data_file:
		counter = 1
		for series_line in data_file.readlines()[1:]:
			#series line has format: Series,N Obs,Seasonality,NF,Type,Starting date,Category,1,2,3 ...
			series_tuples = series_line.split(',')
			number_obeservations = int(series_tuples[1])
			number_forecast = int(series_tuples[3])

			orig = TimeSeries(isNormalized=True)
			for i in range(number_obeservations):
				orig.add_entry(i, series_tuples[i + 7]) #offset to first data entry in line
			#print orig
			
			forecast_check = TimeSeries(isNormalized=True)
			for j in range(number_obeservations, number_obeservations + number_forecast):
				forecast_check.add_entry(j, float(series_tuples[j + 7]))

			#print forecast_check

			#Season indices are given in season file
			season_indices_tuple = season_indices.readline().split(',')
			seasonLength = int(season_indices_tuple[1])
			season_values = []
			for i in range(seasonLength):
				season_values.append(float(season_indices_tuple[i + 2]))
			#print season_values

			hwm = HoltWintersMethod(seasonLength = seasonLength, valuesToForecast = number_forecast)
			hwm.set_parameter("seasonValues", season_values)

			#Optimize parameters
			gridSearch = GridSearch(SMAPE)
			optimal_forecasting, error, optimal_params = gridSearch.optimize(orig, [hwm])
			predicted = optimal_forecasting.execute(orig)

			#Now add forecasted values to original and calculate error
			orig += forecast_check
			assert len(orig) == len(predicted), "Prediction and original season should have the same length."

			total_error = SMAPE()
			total_error.initialize(orig, predicted)

			forecast_error = SMAPE()
			forecast_error.initialize(forecast_check, TimeSeries.from_twodim_list(predicted[-len(forecast_check):]))

			print counter, error.get_error(), total_error.get_error(), forecast_error.get_error()
			counter += 1