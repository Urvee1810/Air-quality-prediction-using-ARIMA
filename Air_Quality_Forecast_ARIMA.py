# -*- coding: utf-8 -*-
"""GITHUB_AirQuality_Forecast_ARIMA .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sZsbnzOcb-l0ZPvR0Sp4AJtNLZN9aZvb

## Dataset

This data set includes hourly air pollutants data from 12 nationally-controlled air-quality monitoring sites. The air-quality data are from the Beijing Municipal Environmental Monitoring Center. The meteorological data in each air-quality site are matched with the nearest weather station from the China Meteorological Administration. The time period is from March 1st, 2013 to February 28th, 2017. Missing data are denoted as NA.

**Attributes Information:**

* No: row number
* year: year of data in this row
* month: month of data in this row
* day: day of data in this row
* hour: hour of data in this row
* PM2.5: PM2.5 concentration (ug/m^3)
* PM10: PM10 concentration (ug/m^3)
* SO2: SO2 concentration (ug/m^3)
* NO2: NO2 concentration (ug/m^3)
* CO: CO concentration (ug/m^3)
* O3: O3 concentration (ug/m^3)
* TEMP: temperature (degree Celsius)
* PRES: pressure (hPa)
* DEWP: dew point temperature (degree Celsius)
* RAIN: precipitation (mm)
* wd: wind direction
* WSPM: wind speed (m/s)
* station: name of the air-quality monitoring site

**Dataset source:** https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data
"""

#@title Download Dataset
#!wget -qq https:// (load you dataset)
print("Dataset downloaded successfully!!")

!pip -qq install pmdarima

"""### Import required Packages"""

import warnings
warnings.simplefilter('ignore')
import pmdarima as pm
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from scipy.special import expit, logit
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

"""### Load the data and analyze"""

path = "PRSA_Data_Nongzhanguan_20130301_20170228.csv"
df = pd.read_csv(path)
df

df['DATE'] = pd.to_datetime(df[['year', 'month','day','hour']])
df.set_index('DATE',drop=True, inplace=True)
df.fillna(0, inplace=True)

df.head()

# plotting multiple weather related variables with PM2.5
multi_data = df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN']]
multi_data.plot(subplots=True)
plt.show()

pd.plotting.lag_plot(df['TEMP'], lag=10)

"""#### Pair plot between Features"""

import seaborn as sns
g = sns.pairplot(df[['SO2','NO2','O3','CO', 'PM2.5']])

"""By this we can observe the correlation between the features.

We can also find the values of correlation by using pearson correlation matrix.

### Correlation plot between Features
"""

aq_pear_corr = df[['SO2','NO2','O3','CO','PM10', 'PM2.5']].corr(method='pearson')
aq_pear_corr

sns.heatmap(aq_pear_corr,annot=True)

"""Thus, we can interpret that $PM_{2.5}$ is higly correlated with $CO$ and $PM_{10}$ and moderately correlated with $NO_{2}$."""

aq_df_na = df.copy()
aq_df_na = aq_df_na.dropna()

pd.plotting.autocorrelation_plot(aq_df_na['PM2.5'])

df['PM2.5'].plot(figsize=(15,6))
plt.show()

"""### Identify the trends and seasonality from the given time series data

"""

df['PM2.5'].fillna(0, inplace=True)
df['PM2.5']

# The statsmodels library provides a suite of functions for working with time series data
from statsmodels.tsa.seasonal import seasonal_decompose
df['PM2.5'].fillna(0, inplace=True)
ts = df['PM2.5']

# ETS Decomposition
result = seasonal_decompose(ts)

# ETS plot
result.plot();

# ETS Decomposition
result = seasonal_decompose(ts[:500])

# ETS plot
result.plot();

"""### Time Series Stationarity

Check the Stationarity of time series using:
  * Dickey Fuller test
  * Rolling mean and Rolling standard deviation

Make the timeseries stationary

* Apply Log transformation and **Differencing** of the timeseries to make it stationary

Verify the stationarity with the Dickey Fuller test
"""

# Let’s create a function to run the test which determines whether a given time series is stationary
def get_stationarity(timeseries):
    # Rolling statistics
    rolling_mean = timeseries.rolling(window=12).mean()
    rolling_std = timeseries.rolling(window=12).std()

    # Rolling statistics plot
    plt.figure(figsize=(15,5))
    original = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolling_mean, color='red', label='Rolling Mean')
    std = plt.plot(rolling_std, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

get_stationarity(df['PM2.5'][:1000])

# ESTIMATING THE TREND
# Applying a log transformation is a way to reduce the variance of the series
df_log = np.log(df['PM2.5'])
plt.plot(df_log);

print(df_log.min())
df_log.replace(-np.inf, 0,inplace=True)
df_log.min()

"""Eliminating the Trend and Seasonality by **Differencing** (taking the difference with a particular time lag)"""

shift_df = pd.concat([df_log, df_log.shift(1)],axis=1)
shift_df.columns = ['Actual','Forecasted']
shift_df.head()

df_log_shift = shift_df['Actual'] - shift_df['Forecasted']
df_log_shift.dropna(inplace=True)
get_stationarity(df_log_shift[:1000])

#Perform Dickey Fuller test
result = adfuller(df_log)
print('ADF Stastistic: %f'%result[0])
print('p-value: %f'%result[1])
pvalue = result[1]
for key,value in result[4].items():
  if result[0]>value:
    print("The graph is non stationery")
    break
  else:
    print("The graph is stationary")
    break;
print('Critical values:')
for key,value in result[4].items():
    print('\t%s: %.3f ' % (key, value))

"""### Auto Correlation Plot Analysis
* Plot ACF and PACF graphs
* Analyse and identify the ARIMA (p, d, q) terms
"""

# let us plot acf and pacf graphs
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

plt.figure(figsize = (20,10))
plt.subplot(211)
plot_acf(df_log_shift, ax=plt.gca(), lags = 60)
plt.subplot(212)
plot_pacf(df_log_shift, ax=plt.gca(), lags = 60)
plt.show()

df_log = pd.DataFrame(df_log)
df_log.reset_index(inplace=True)
df_log.DATE = pd.to_datetime(df_log.DATE)
df_log.set_index('DATE',inplace=True)
df_log

# split the data into train and test
train_ar = df_log[:int(len(df_log)*0.9)]
test_ar = df_log[int(len(df_log)*0.9):]

train_ar.tail(),test_ar.head()

len(train_ar), len(test_ar)

"""### Implement ARIMA model
* Fit the timeseries data with ARIMA
* Find and interpret the loss (AIC)
"""

# ARIMA Method - 1
from math import sqrt
from sklearn.metrics import mean_squared_error
# ARIMA model
# order (2,1,2) based on auto_arima performed above
model = ARIMA(train_ar, order=(2,1,2) )
model_fit = model.fit()
print(model_fit.aic)
predictions = model_fit.predict(start=test_ar.index[0],end=test_ar.index[-1])
error = sqrt(mean_squared_error(test_ar, predictions))
print('RMSE value: %.3f' % error)

plt.figure(figsize=(17,7))
plt.plot(test_ar.index, test_ar, color='red', label='Actual Test Data')
plt.plot(test_ar.index, predictions, color='green',marker='o', linestyle='dashed', label='Predicted Data')
plt.legend();

"""### Plot the predictions"""

plt.figure(figsize=(17,7))
plt.plot(train_ar, 'green', color='blue', label='Training Data')
plt.plot(test_ar.index[:50], test_ar[:50], color='red', label='Actual Test Data')
# Ensure predictions array has the correct length and values
predictions = model_fit.predict(start=len(train_ar), end=len(train_ar) + 49) # Predict for the next 50 data points
plt.plot(test_ar.index[:50], predictions, color='green', marker='o', linestyle='dashed', label='Predicted Data')
plt.legend();

"""# Report Analysis
### 1. *Comment on the trend and seasonality of the time series data:*

Based on the seasonal decomposition plots (outputs from cells [16] and [17]), we can observe:
- Trend: There's a gradual fluctuating pattern in PM2.5 levels over time, with no consistent upward or downward trend
- Seasonality: The data shows clear seasonal patterns that repeat approximately every 12 months
- The residual component shows considerable variation, indicating high day-to-day volatility in air quality

### 2. *Comment on Dickey Fuller test analysis:*

From cell [24], we can see:
- ADF Statistic: -21.883699
- p-value: 0.000000 (extremely small)
- Critical values at different significance levels:

  1%: -3.431

  5%: -2.862

  10%: -2.567

The test indicates the time series is stationary because:
- The p-value is less than 0.05 (significant)
- The ADF statistic (-21.88) is more negative than all critical values
This means the data has consistent statistical properties over time, making it suitable for forecasting.

### *3. Is the air quality becoming poorer across the years?*
Looking at the time series plot (cell [14]):
- There isn't a clear long-term deterioration in air quality
- PM2.5 levels show periodic highs and lows
- The baseline levels remain relatively consistent across years
- Extreme spikes occur periodically but don't show an increasing trend

### *4. Spikes in poor air quality:*
From the plots and correlation analysis (cells [7], [9], [11]):
- Regular spikes appear in winter months
- Possible reasons for spikes:
  - Higher correlation with CO and PM10 suggests increased pollution from heating and vehicle emissions
  - Temperature inversions in winter trapping pollutants
  - Seasonal industrial activities
  - Increased energy consumption during colder months
"""