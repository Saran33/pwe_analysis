# PWE Analysis

### Financial timeseries charting and analysis. 
PWE Analysis is a PWE Capital repository for analysing securities using Pandas, Plotly, Cufflinks and other tools.

`pwe` is a package for rapidly deploying the aforementioned tools.

The repository can be found at:
[Github-PWE_Analysis](https://github.com/Saran33/pwe_analysis/)

#### To install from git:
`pip install git+git://github.com/Saran33/pwe_analysis.git`

#### Download CoinMarketCap data:
```python
from pwe import charts,quan,cmc
from pwe.analysis import Security
from datetime import date
import time

start_date = "01-01-2017"
end_date = date.today().strftime("%d-%m-%Y")

BTC = cmc.cmc_data(symbol="BTC",start_date=start_date,end_date=end_date)

settlements = dict({'2021-01-29': 'CME Exp.', '2021-02-26': 'CME Exp.', 
                    '2021-03-26': 'CME Exp.', '2021-04-30': 'CME Exp.', 
                    '2021-05-28': 'CME Exp.', '2021-06-25': 'CME Exp.', 
                    '2021-07-30': 'CME Exp.'})

auto_start = '2021-01-01'
auto_end = '2021-08-15'

charts.quant_chart_int(BTC,start_date,end_date,ticker='BTC',
                       theme='white',auto_start=auto_start,auto_end=auto_end,
                       asPlot=True,showlegend=True,boll_std=2,boll_periods=20,
                       showboll=True,showrsi=True,rsi_periods=14,showama=True,
                       ama_periods=9,showvol=True,show_price_range=True,
                       textangle=60,annots=settlements)
```
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
#### Initialize Securities & Calculate Returns:
```python
BTC = Security(BTC)
BTC.get_returns(price='Close')

BTC_Bitfinex = Security(BTC_Bitfinex)
BTC_Bitfinex.get_returns(price='Last')
```
### Calculate Volume-Weighted Average Price:
```python
BTC.vwap(window=60)

BTC_Bitfinex.vwap(c='Last',window=60)
```
#### Calculate 30 Day Volatility:
```python
vol_window = 30
BTC_Bitfinex.get_vol(window=vol_window, column='Price_Returns',trading_periods=365,interval=interval)
```
#### Calculate 30 Day YangZhang Volatility Estimator (Requires OHLC data):
```python
BTC.YangZhang_estimator(window=vol_window,trading_periods=365, clean=True,interval=interval)
```
### View the DataFrame of a security:
```python
BTC.df
```
### Return the ticker:
```python
BTC_Bitfinex.ticker
```
#### Returns Profile:
```python
BTC.stats(returns='Price_Returns',price='Close',
                                          trading_periods=365,interval=interval,market_hours=24,vol_window=vol_window)
```
```console
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
```console
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

btc_dist_bar = charts.pwe_return_bar_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='bar',
                                             title='Bitfinex Bitcoin Daily Returns',
                                             ticker='BRTI',yTitle='BTC/USD (%)',xTitle=None,asPlot=asPlot,theme='white',
                                             showlegend=False,auto_start=auto_start,auto_end=end_date,tickformat='.0%',
                                             decimals=2,orientation='v',textangle=0)

btc_yz30_dist = charts.pwe_return_dist_chart(BTC,start_date,end_date,
                                             tseries='YangZhang30_Ann',kind='scatter',
                                    title='Spot Bitcoin to US Dollars (Bitfinex): Annualized Yang-Zhang 30 Day Volatility',
                                             ticker='BTC-USD YZ Vol.',yTitle='BTC/USD YZ Vol.',
                                             asPlot=asPlot,showlegend=False,theme='white',
                                             auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)

btc_vol30_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,
                                              tseries='Ann_Vol_30',kind='scatter',
                                    title='Spot Bitcoin to US Dollars: Annualized 30 Day Volatility',
                                             ticker='BTC-USD Vol.',yTitle='BTC/USD Vol.',asPlot=asPlot,
                                             showlegend=False,theme='white',auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)
```
#### Returns by Subseries: 
##### 2020
```python
BTC.get_sub_series(start_date='2020-1-1',end_date='2020-12-31')
```
```console
Subseries stored as: _2020
```
###### The ```get_sub_series``` method returns an instance of the Security class, which is an attribute of the original Security object.
```python
type(BTC._2020), BTC._2020.ticker, BTC._2020.name
```
```console
(pwe.analysis.Security, 'BTC', '_2020')
```
##### 2020 Stats:
```python
BTC._2020.stats(returns='Price_Returns',price='Close',trading_periods=365,interval='daily',market_hours=24);
```
```console
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
```console
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
```console
(4.323912901598581, 3.027919080879859, 0.7666323477904143, 3.9496364712589016)
```