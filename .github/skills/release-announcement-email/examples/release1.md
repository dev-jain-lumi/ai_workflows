Dear all,

We’re happy to announce several improvements to the Solar S50 forecasts (residential clients with solar panels)

Processes & Data Enhancements

Smarter Learning: Our Day-Ahead, Intraday, and Solar Proxy Actuals models now leverage the best available allocation data, aligning with Fluvius’ Settle2.0 changes.
✅ Higher data quality for allocations
🔄 Weekly model training to better capture recent trends, instead of less accurate bi-monthly training in place since last fall


Intraday forecast:

After extensive testing, we’ve deployed a new Intraday model,  already sent to Argus and the RT dashboard. Key improvements:

☀️Extended Training Horizon: Previously specialized on the 4-hours ahead horizon, the model now trains on all quarter-hourly horizons (15 min to 6 hours ahead) for better generalization and short-term accuracy.
Recent Elia measurements are now included, for a better short-term responsiveness
Performance Boost: Backtesting results indicate an improvement in MAPE of up to 3%, depending on the period.
 

 

Solar Proxy Actuals:

Enhanced Inputs: In addition to Elia PV power data per province, the model now incorporates recent weather observations.
☀️ Reduces the structural underestimation seen in recent months, with monthly MAPE improving by up to 2%.
 

 

🚀 What’s Next?

Model Innovation: Experiment with new model types to further refine forecasts.
Weather Data Integration: Euro1k weather forecasts are now available in NEO—we will test their impact on forecast accuracy.
 

 

Let us know if you have any questions or feedback.

 

Best regards,
DI Team