# Air-quality-prediction-using-ARIMA

*This project was completed as part of PG Level Advanced Certification Programme in Computational Data Science coursework at Centre for Continuing Education - Indian Institute of Science in collaboration with Talent Sprint.*

A special thanks to Prof. Dr. Shashi Jain & Mentor Mr. Sachin Sharma 

Problem Statement: Implement ARIMA model to forecast the air quality using Beijing air quality dataset

Module: Business Analytics 

Project Type: Team 

## Learning Outcome: 
- perform EDA on time series data
- analyze the auto correlation and partial auto correlation plots
- implement the ARIMA model and forecast the air quality

## Overview
A comprehensive time series analysis of Beijing's air quality data from 2013 to 2017, focusing on PM2.5 concentrations and their relationships with other pollutants and meteorological factors. The project implements statistical modeling techniques to understand pollution patterns and predict future air quality levels.

## Theory: 

ARIMA stands for auto-regressive integrated moving average. It’s a way of modelling time series data for forecasting (i.e., for predicting future points in the series), in such a way that:
- a pattern of growth/decline in the data is accounted for (“auto-regressive” part)
- the rate of change of the growth/decline in the data is accounted for (the “integrated” part)
- noise between consecutive time points is accounted for (the “moving average” part)

## Key Features
- Time series analysis of hourly air quality data
- Correlation analysis between multiple pollutants
- Seasonal decomposition of PM2.5 trends
- Stationarity testing and transformation
- ARIMA modeling for pollution forecasting
- Interactive visualizations of pollution patterns

## Tools & Technologies
- Python
- Pandas & NumPy
- Statsmodels
- Scikit-learn
- Matplotlib & Seaborn
- PMDarima

## Results
The analysis reveals seasonal patterns in air pollution levels, with significant correlations between different pollutants. The ARIMA model provides forecasting capabilities with detailed error metrics and visualization of predictions.
