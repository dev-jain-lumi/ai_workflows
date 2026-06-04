Dear all,
I am glad to announce the release of an incremental update on the wind onshore project. As a reminder, this project aims at forecasting the power production of 133 onshore wind parks, currently with a focus on day-ahead. The day-ahead model also provides intraday updates every 2 hours.
This increment is centered on data source changes and data quality improvements. Notably, it removes all dependencies on ConWX and MeteoGroup, clearing a major blocker for their decommissioning (planned around mid-Q1 2026).
What has changed:
Weather inputs: Switched from MeteoGroup/ConWX to Meteomatics. Our machine learning models now use weather variables from a broader set of weather models (UKMO, ECMWF-IFS, NCEP-GFS, MOS), all provided by Meteomatics.
Metering quality: TSO metering is now sourced via the Retail data product “Metering Electricity.”  
Granularity: Forecasts are now quarter-hourly (previously, hourly values were replicated to QH).
We have temporarily replaced the forecast aggregation model by XGBoost. Aggregation will be reinstated once sufficient forecast history is available with the new models. 
Action required: None. The new forecasts are exported to Metrix under the same IDs as before.

In the coming weeks, we will closely monitor the performance of these new models and will provide updates in our monthly AI KPI meeting. 
Thanks to everyone who made this release possible. Do not hesitate to reach out if you have any questions!
Best regards,
Romain