# PWE Analysis

### Financial timeseries charting and analysis. 
PWE Analysis is a PWE Capital repository for analysing securities using Pandas, Plotly, Cufflinks and other tools.

`pwe` is a package for rapidly deploying the aforementioned tools.

The repository can be found at:
[Github-PWE_Analysis](https://github.com/Saran33/pwe_analysis/)

#### To install from git:
`pip install git+git://github.com/Saran33/pwe_analysis.git`

To run some functions, you will also need to install the C++ [TA-Lib] (https://github.com/mrjbq7/ta-lib)

#### Download CoinMarketCap data:
```python
from pwe import charts,quan,cmc
from pwe.analysis import Security
from datetime import date
import time

start_date = "01-01-2017"
end_date = date.today().strftime("%d-%m-%Y")

BTC = cmc.cmc_data(symbol="BTC",start_date=start_date,end_date=end_date)

# Initialize Security
BTC = Security(BTC)

settlements = dict({'2021-01-29': 'CME Exp.', '2021-02-26': 'CME Exp.', 
                    '2021-03-26': 'CME Exp.', '2021-04-30': 'CME Exp.', 
                    '2021-05-28': 'CME Exp.', '2021-06-25': 'CME Exp.', 
                    '2021-07-30': 'CME Exp.'})

auto_start = '2021-01-01'
auto_end = '2021-08-15'

BTC.get_fibs(period='ytd', utc=True)
support=BTC.f_618
resist=BTC.f_382

charts.quant_chart_int(BTC.df, start_date, end_date, ticker=symbol, title=None, theme='white', auto_start=auto_start, auto_end=auto_end,
                asPlot=asPlot, showlegend=True, boll_std=2, boll_periods=20, showboll=True, showrsi=True, rsi_periods=14, showama=True,
                ama_periods=9, showvol=True, showkal=False, kal_periods=1, show_range=True, annots=settlements, textangle=0, file_tag=None,
                support=support, resist=resist, annot_font_size=6, title_dates=False, title_time=False, chart_ticker=True, top_margin=0.9,
                spacing=0.08, range_fontsize=9.8885, title_x=0.5, title_y=0.933, arrowhead=6, arrowlen=-50)
```
![Candle Chart](img/BTC_BTC_01-01-2017-24-08-2021_interative_white_PWE.png)
#### Download Quandl data:
```python
# Input your key the first time and then no need to input a key argument again. 
# Your API key will be saved to the currrent directory.

BTC_Bitfinex = quan.quandl_data(ticker='BITFINEX/BTCUSD',
                                start_date=start_date,end_date=end_date, key='quandl_api_key')
                                
# If running all the code on this README page in one block, include the below sleep function:
time.sleep(1)

charts.pwe_line_chart(BTC_Bitfinex,columns=['Last'],start_date=start_date,end_date=end_date,kind='scatter',
                      title='Bitfinex Bitcoin Daily Close',
                  ticker='BTC',yTitle='BTC/USD',asPlot=True,showlegend=False,
                  theme='white',auto_start='2021-01-01',auto_end=auto_end,
                  connectgaps=False)
```
![Line (scatter) Chart](img/BTC_01-01-2017-24-08-2021_line_white_PWE.png)
#### Initialize Securities & Calculate Returns:
```python
# BTC already initialized
BTC.get_returns(price='Close')

BTC_Bitfinex = Security(BTC_Bitfinex)
BTC_Bitfinex.get_returns(price='Last')
```
#### Calculate Volume-Weighted Average Price:
```python
BTC.vwap(window=60)

BTC_Bitfinex.vwap(c='Last',window=60)
```
#### Calculate 30 Day Volatility:
```python
vol_window = 30
BTC_Bitfinex.get_vol(window=vol_window, returns='Price_Returns',trading_periods=365,interval=interval)
```
#### Calculate 30 Day YangZhang Volatility Estimator (Requires OHLC data):
```python
BTC.YangZhang_estimator(window=vol_window,trading_periods=365, clean=True,interval=interval)
```
#### View the DataFrame of a security:
```python
BTC.df
```

| Date                |     Open |    High |      Low |    Close |      Volume |   Market Cap |    Price |   Price_Returns |   Log_Returns |   Cumulative Returns |       AP |         CPV |   Cum_Volume |     VWAP |   YangZhang_30_Day |   YangZhang30_Day_Ann |   Std_30_Day |   Ann_Std_30_Day |   Vol_30_Day |   Ann_Vol_30_Day |   Ann_VS_Var_30_Day |   Ann_VS_Vol_30_Day |   Realized_Var_30_Day |   Realized_Vol_30_Day |
|:--------------------|---------:|--------:|---------:|---------:|------------:|-------------:|---------:|----------------:|--------------:|---------------------:|---------:|------------:|-------------:|---------:|-------------------:|----------------------:|-------------:|-----------------:|-------------:|-----------------:|--------------------:|--------------------:|----------------------:|----------------------:|
| 2017-01-01 00:00:00 |  963.658 | 1003.08 |  958.699 |  998.325 | 1.47775e+08 |  1.60504e+10 |  998.325 |     nan         |   nan         |            0         |  986.701 | 1.4581e+11  |  1.47775e+08 |  986.701 |                nan |                   nan |          nan |              nan |          nan |              nan |                 nan |                 nan |                   nan |                   nan |
| 2017-01-02 00:00:00 |  998.617 | 1031.39 |  996.702 | 1021.75  | 2.22185e+08 |  1.6429e+10  | 1021.75  |       0.0234643 |     0.0231932 |            0.0234643 | 1016.61  | 3.71686e+11 |  3.6996e+08  | 1004.67  |                nan |                   nan |          nan |              nan |          nan |              nan |                 nan |                 nan |                   nan |                   nan |
| 2017-01-03 00:00:00 | 1021.6   | 1044.08 | 1021.6   | 1043.84  | 1.85168e+08 |  1.67864e+10 | 1043.84  |       0.0216197 |     0.0213893 |            0.0455913 | 1036.51  | 5.63614e+11 |  5.55128e+08 | 1015.29  |                nan |                   nan |          nan |              nan |          nan |              nan |                 nan |                 nan |                   nan |                   nan |
| 2021-08-21 00:00:00 | 49327.1 | 49717   | 48312.2 | 48905.5 | 4.05852e+10 |  9.19092e+11 | 48905.5 |     -0.00878988 |   -0.00882874 |              47.9875 | 48978.2 | 6.97137e+16 |  1.8175e+12  | 38356.8 |          0.039166  |              0.748265 |    0.0335002 |         0.640021 |    0.0329806 |         0.630093 |             13.603  |             3.68823 |              0.397017 |              0.630093 |
| 2021-08-22 00:00:00 | 48869.1 | 49471.6 | 48199.9 | 49321.7 | 2.5371e+10  |  9.26962e+11 | 49321.7 |      0.00850954 |    0.00847354 |              48.4044 | 48997.7 | 6.9409e+16  |  1.79656e+12 | 38634.5 |          0.0390771 |              0.746567 |    0.0331838 |         0.633976 |    0.0326595 |         0.623959 |             13.0881 |             3.61775 |              0.389325 |              0.623959 |
| 2021-08-23 00:00:00 | 49291.7 | 50482.1 | 49074.6 | 49546.1 | 3.43051e+10 |  9.31244e+11 | 49546.1 |      0.00455162 |    0.0045413  |              48.6293 | 49700.9 | 6.99848e+16 |  1.79774e+12 | 38929.4 |          0.03913   |              0.747577 |    0.0331887 |         0.634069 |    0.032656  |         0.623891 |             12.9354 |             3.59659 |              0.38924  |              0.623891 |

#### Return the ticker:
```python
BTC_Bitfinex.ticker
```
```zsh
'BITFINEX/BTCUSD'
```
#### Returns Profile:
```python
BTC.stats(returns='Price_Returns',price='Close',
                                          trading_periods=365,interval=interval,market_hours=24,vol_window=vol_window)
```
```zsh
BTC/USD Return Stats:
Dates: 2017-01-01 00:00:00 - 2021-08-23 00:00:00
Periods: 1695 days
Trading Periods: 365 days a year
Years: 4.64

Cumulative Returns: 4862.93%

Arithmetic Mean Return: 0.321587%
Geometric Mean Return: 0.230624%

Median Return: 0.238515%

Annualaized Arithmetic Return: 222.82%
Annualized Geometric Return: 131.82%
 
Vol. of Period Returns: 4.280663%
Mean Volatility (30): 3.902691%
Mean YangZhang (30): 3.726685%

Annualized Vol: 81.78%
Annualized Mean Volatility (30): 74.56%
Annualized Mean YangZhang (30): 71.20%

Arithmetic Sharpe Ratio: 2.72
Geometric Sharpe Ratio: 1.61
 
Return Summary Security:
count    1695.000000
mean        0.003216
std         0.042479
min        -0.371695
25%        -0.015233
50%         0.002385
75%         0.021611
max         0.252472
Name: Price_Returns, dtype: float64
######
```
```python
BTC.avg_annualaized, BTC.cum_ret, BTC.ann_vol, BTC.sharpe_ratio_geo
```
```zsh
(2.2281516218402473,
 48.629276138996694,
 0.8178195890242521,
 1.6118991934777804)
```
#### Plot the Returns & Volatility Distributions:
```python
asPlot=True

btc_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='scatter',
                                    title='Daily Bitcoin Returns on Bitfinex',ticker='BTC',yTitle='BTC/USD (%)',asPlot=asPlot,
                                    showlegend=False,theme='white',auto_start='2021-01-01', auto_end=end_date,
                                    connectgaps=False,tickformat='.0%',decimals=2)
```
![Distribution Chart](img/BTC_BITFINEX_BTCUSD_01-01-2017-24-08-2021_dist_white_PWE.png)
```python
btc_dist_bar = charts.pwe_return_bar_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='bar',
                                             title='Bitfinex Bitcoin Daily Returns',
                                             ticker='BRTI',yTitle='BTC/USD (%)',xTitle=None,asPlot=asPlot,theme='white',
                                             showlegend=False,auto_start=auto_start,auto_end=end_date,tickformat='.0%',
                                             decimals=2,orientation='v',textangle=0)
```
![Bar Chart](img/BTC_BITFINEX_BTCUSD_01-01-2017-24-08-2021_bar_chart_white_PWE.png)
```python
btc_yz30_dist = charts.pwe_return_dist_chart(BTC,start_date,end_date,
                                             tseries='YangZhang30_Ann',kind='scatter',
                                    title='Spot Bitcoin to US Dollars (Bitfinex): Annualized Yang-Zhang 30 Day Volatility',
                                             ticker='BTC-USD YZ Vol.',yTitle='BTC/USD YZ Vol.',
                                             asPlot=asPlot,showlegend=False,theme='white',
                                             auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)
```
![Yang-Zhang](https://github.com/Saran33/pwe_analysis/blob/main/img/BTC-USD%20YZ%20Vol._BTC_01-01-2017-24-08-2021_dist_white_PWE.png)
```python
btc_vol30_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,
                                              tseries='Ann_Vol_30',kind='scatter',
                                    title='Spot Bitcoin to US Dollars: Annualized 30 Day Volatility',
                                             ticker='BTC-USD Vol.',yTitle='BTC/USD Vol.',asPlot=asPlot,
                                             showlegend=False,theme='white',auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)
```

![Volatility](https://github.com/Saran33/pwe_analysis/blob/main/img/BTC-USD%20Vol._BITFINEX_BTCUSD_01-01-2017-24-08-2021_dist_white_PWE.png)

#### Returns by Subseries: 
##### 2020
```python
BTC.get_sub_series(start_date='2020-1-1',end_date='2020-12-31')
```
```zsh
Subseries stored as: _2020
```
The ```get_sub_series``` method returns an instance of the Security class, which is an attribute of the original Security object.
```python
type(BTC._2020), BTC._2020.ticker, BTC._2020.name
```
```zsh
(pwe.analysis.Security, 'BTC', '_2020')
```
##### 2020 Stats:
```python
BTC._2020.stats(returns='Price_Returns',price='Close',trading_periods=365,interval='daily',market_hours=24);
```
```zsh
BTC 2020 Return Stats:
Dates: 2020-01-01 00:00:00 - 2020-12-31 00:00:00
Periods: 366 days
Trading Periods: 365 days a year
Years: 1.0

Cumulative Returns: 302.79%

Arithmetic Mean Return: 0.458186%
Geometric Mean Return: 0.381395%

Median Return: 0.266775%

Annualaized Arithmetic Return: 430.45%
Annualized Geometric Return: 301.26%
 
Vol. of Period Returns: 4.007265%
Mean Volatility (30): 3.439818%
Mean YangZhang (30): 2.914670%

Annualized Vol: 76.56%
Annualized Mean Volatility (30): 65.72%
Annualized Mean YangZhang (30): 55.68%

Arithmetic Sharpe Ratio: 5.62
Geometric Sharpe Ratio: 3.94
 
Return Summary Security:
count    366.000000
mean       0.004582
std        0.037708
min       -0.371695
25%       -0.009387
50%        0.002668
75%        0.017697
max        0.181878
Name: Price_Returns, dtype: float64
######
```
If you wish to override the derived columns of the subseries for some reason (maybe you want to change the window for rolling calculations):
```python
BTC._2020.get_returns(price='Close')

BTC._2020.YangZhang_estimator(window=vol_window, trading_periods=365, clean=True,interval=interval)

BTC._2020.get_vol(window=vol_window, column='Price_Returns',trading_periods=365,interval=interval)

BTC._2020.df
```
```python
BTC._2020.stats(returns='Price_Returns',price='Close',trading_periods=365,interval='daily',market_hours=24);
```
```zsh
BTC 2020 Return Stats:
Dates: 2020-01-01 00:00:00 - 2020-12-31 00:00:00
Periods: 365 days
Trading Periods: 365 days a year
Years: 1.0

Cumulative Returns: 302.79%

Arithmetic Mean Return: 0.459190%
Geometric Mean Return: 0.382442%

Median Return: 0.278798%

Annualaized Arithmetic Return: 432.39%
Annualized Geometric Return: 302.79%
 
Vol. of Period Returns: 4.012737%
Mean Volatility (30): 3.441800%
Mean YangZhang (30): 2.914670%

Annualized Vol: 76.66%
Annualized Mean Volatility (30): 65.76%
Annualized Mean YangZhang (30): 55.68%

Arithmetic Sharpe Ratio: 5.64
Geometric Sharpe Ratio: 3.95
 
Return Summary Security:
count    365.000000
mean       0.004592
std        0.037759
min       -0.371695
25%       -0.009402
50%        0.002788
75%        0.017784
max        0.181878
Name: Price_Returns, dtype: float64
######
```
To access the stats or other attributes for a specific time interval:
```python
BTC._2020.avg_annualaized, BTC._2020.cum_ret, BTC._2020.ann_vol, BTC._2020.sharpe_ratio_geo
```
```zsh
(4.323912901598581, 3.027919080879859, 0.7666323477904143, 3.9496364712589016)
```
