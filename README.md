# PWE Analysis

### Financial timeseries charting and analysis. 
PWE Analysis is a repository for analysing securities using Pandas, Plotly, Cufflinks and other tools.

The repository can be found at:
[Github-PWE_Analysis](https://github.com/Saran33/pwe_analysis/)

#### To install from pypi:
`pip install pwe`

#### Download CoinMarketCap data:
```python
from pwe import charts,returns,vol,quan,cmc
from datetime import date
import time

start_date = "01-01-2017"
end_date = date.today().strftime("%d-%m-%Y")

BTC = cmc.cmc_data(ticker="BTC",start_date=start_date,end_date=end_date)

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
                       textangle=60,tags=settlements)
```
#### Download Quandl data:
```python
BTC_Bitfinex = quan.quandl_data(ticker='BITFINEX/BTCUSD',
                                start_date=start_date,end_date=end_date)
                                
# If running all the code on this README page in one block, include the below sleep function:
time.sleep(1)

charts.pwe_line_chart(BTC_Bitfinex,columns=['Last'],start_date=start_date,end_date=end_date,kind='scatter',
                      title='Bitfinex Bitcoin Daily Close',
                  ticker='BTC',yTitle='BTC/USD',asPlot=True,showlegend=False,
                  theme='white',auto_start='2021-01-01',auto_end=auto_end,
                  connectgaps=False)
```
#### Calculate Returns:
```python
returns.get_returns(BTC, price='Close');
returns.get_returns(BTC_Bitfinex, price='Last');
```

#### Calculate 30 Day Volatility:
```python
vol.get_vol(BTC_Bitfinex, window=30, column='Price_Returns',trading_periods=365);
```
#### Calculate 30 Day YangZhang Volatility Estimator (Requires OHLC data):
```python
vol.YangZhang_estimator(BTC, window=30, trading_periods=365, clean=True);
```
#### Returns Profile:
```python
bitfinex_btc_stats = returns.return_stats(BTC_Bitfinex,returns='Price_Returns',price='Last',
                                          trading_periods=365,interval='daily',market_hours=24)
```
#### Plot the Returns & Volatility Distributions:
```python
asPlot=True
start_date= '2021-01-01'
btc_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='scatter',
                                    title='Daily Bitcoin Returns on Bitfinex',ticker='BTC',yTitle='BTC/USD (%)',asPlot=asPlot,
                                    showlegend=False,theme='white',auto_start='2021-01-01', auto_end=end_date,
                                    connectgaps=False,tickformat='%',decimals=2)

btc_dist_bar = charts.pwe_return_bar_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='bar',
                                             title='Bitfinex Bitcoin Daily Returns',
                                             ticker='BRTI',yTitle='BTC/USD (%)',xTitle=None,asPlot=asPlot,theme='white',
                                             showlegend=False,auto_start=auto_start,auto_end=end_date,tickformat='%',
                                             decimals=2,orientation='v',textangle=0)

btc_yz30_dist = charts.pwe_return_dist_chart(BTC,start_date,end_date,
                                             tseries='YangZhang30_Ann',kind='scatter',
                                    title='Spot Bitcoin to US Dollars (Bitfinex): Annualized Yang-Zhang 30 Day Volatility',
                                             ticker='BTC-USD YZ Vol.',yTitle='BTC/USD YZ Vol.',
                                             asPlot=asPlot,showlegend=False,theme='white',
                                             auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='%',decimals=2)

btc_vol30_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,
                                              tseries='Ann_Vol_30',kind='scatter',
                                    title='Spot Bitcoin to US Dollars: Annualized 30 Day Volatility',
                                             ticker='BTC-USD Vol.',yTitle='BTC/USD Vol.',asPlot=asPlot,
                                             showlegend=False,theme='white',auto_start='2021-01-01',auto_end=end_date,
                                             connectgaps=False,tickformat='%',decimals=2)
```
#### Returns by Subseries: 
##### 2019
```python
df_2019 = returns.get_sub_series(BTC,start_date='2019-1-1',end_date='2019-12-31')
df_2019.name = 2019
df_2019

returns.get_returns(df_2019, price='Close');
vol.YangZhang_estimator(df_2019, window=30, trading_periods=365, clean=True);
vol.get_vol(df_2019, window=30, column='Price_Returns',trading_periods=365);
df_2019

stats_2019 = returns.return_stats(df_2019,returns='Price_Returns',price='Close',trading_periods=365,interval='daily',market_hours=24);

```
