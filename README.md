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
from pwe import charts,returns,vol,quan,cmc
from datetime import date
import time

security = 'Bitcoin'
symbol = 'BTC'
market = 'USD'
interval = 'daily'
chart_interval = 'Daily'
period = 'Day'
p = 'Day'
asPlot = True
start_date = "01-01-2017"
end_date = date.today().strftime("%d-%m-%Y")

BTC = cmc.cmc_data(ticker="BTC",start_date=start_date,end_date=end_date)

settlements = dict({'2021-01-29': 'CME Exp.', '2021-02-26': 'CME Exp.', 
                    '2021-03-26': 'CME Exp.', '2021-04-30': 'CME Exp.', 
                    '2021-05-28': 'CME Exp.', '2021-06-25': 'CME Exp.', 
                    '2021-07-30': 'CME Exp.'})

# The default range to display on charts:
auto_start = '2021-01-01'
auto_end = '2021-08-15'

charts.quant_chart_int(BTC,start_date,end_date,ticker=symbol,
                       theme='white',auto_start=auto_start,auto_end=auto_end,
                       asPlot=asPlot,showlegend=True,boll_std=2,boll_periods=20,
                       showboll=True,showrsi=True,rsi_periods=14,showama=True,
                       ama_periods=9,showvol=True,show_price_range=True,
                       textangle=60,annots=settlements)
```
#### Download Quandl data:
```python
# Input your key the first time and then no need to input a key argument again. 
# Your API key will be saved to the currrent directory.

BTC_Bitfinex = quan.quandl_data(ticker='BITFINEX/BTCUSD',
                                start_date=start_date,end_date=end_date, key='MY_API_KEY')
                                
# If running all the code on this README page in one block, include the below sleep function:
time.sleep(1)

charts.pwe_line_chart(BTC_Bitfinex,columns=[price],start_date=start_date,end_date=end_date,kind='scatter',
                      title=f'{exchange} {security} {chart_interval} {price}',
                  ticker=symbol,yTitle=f'{symbol}/{market}',asPlot=asPlot,showlegend=False,
                  theme='white',auto_start=auto_start,auto_end=auto_end,
                  connectgaps=False)
```
#### Calculate Returns:
```python
returns.get_returns(BTC, price='Close');
returns.get_returns(BTC_Bitfinex, price='Last');
```

#### Calculate 30 Day Volatility:
```python
vol_window = 30
vol.get_vol(BTC_Bitfinex, window=vol_window, column='Price_Returns',trading_periods=365,interval=interval);
```
#### Calculate 30 Day YangZhang Volatility Estimator (Requires OHLC data):
```python
vol.YangZhang_estimator(BTC, window=vol_window,trading_periods=365, clean=True,interval=interval);
```
#### Returns Profile:
```python
bitfinex_btc_stats = returns.return_stats(BTC_Bitfinex,returns='Price_Returns',price='Last',
                                          trading_periods=365,interval=interval,market_hours=24,vol_window=vol_window)
```
#### Plot the Returns & Volatility Distributions:
```python
asPlot=True
start_date= '2021-01-01'
btc_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='scatter',
                                    title=f'{chart_interval} {security} Returns on {exchange}',ticker=symbol,
                                    yTitle=f'{symbol}/{market} (%)',asPlot=asPlot,showlegend=False,theme='white',
                                    auto_start=auto_start, auto_end=end_date,connectgaps=False,tickformat='.0%',decimals=2)

btc_dist_bar = charts.pwe_return_bar_chart(BTC_Bitfinex,start_date,end_date,tseries='Price_Returns',kind='bar',
                                             title=f'{exchange} {security} {chart_interval} Returns',ticker=symbol,
                                             yTitle=f'{symbol}/{market} (%)',xTitle=None,asPlot=asPlot,theme='white',
                                             showlegend=False,auto_start=auto_start,auto_end=end_date,tickformat='.0%',
                                             decimals=2,orientation='v',textangle=0)

btc_yz30_dist = charts.pwe_return_dist_chart(BTC,start_date,end_date,
                                             tseries=f'YangZhang{vol_window}_{p}_Ann',kind='scatter',
                                    title=f'Spot {security} to US Dollars ({exchange}): Annualized Yang-Zhang {vol_window} {period} Volatility',
                                             ticker=f'{symbol}-{market} YZ Vol.',yTitle=f'{symbol}/{market} YZ Vol.',
                                             asPlot=asPlot,showlegend=False,theme='white',
                                             auto_start=auto_start,auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)

btc_vol30_dist = charts.pwe_return_dist_chart(BTC_Bitfinex,start_date,end_date,
                                              tseries=f'Ann_Vol_{vol_window}_{p}',kind='scatter',
                                    title=f'Spot {security} to US Dollars: Annualized {vol_window} {period} Volatility',
                                             ticker=f'{symbol}-{market} Vol.',yTitle=f'{symbol}/{market} Vol.',asPlot=asPlot,
                                             showlegend=False,theme='white',auto_start=auto_start,auto_end=end_date,
                                             connectgaps=False,tickformat='.0%',decimals=2)
```
#### Returns by Subseries: 
##### 2019
```python
df_2019 = returns.get_sub_series(BTC,start_date='2019-1-1',end_date='2019-12-31')
df_2019.name = 2019
df_2019

returns.get_returns(df_2019, price='Close');
vol.YangZhang_estimator(df_2019, window=vol_window, trading_periods=365, clean=True,interval=interval);
vol.get_vol(df_2019, window=vol_window, column='Price_Returns',trading_periods=365,interval=interval);
df_2019

stats_2019 = returns.return_stats(df_2019,returns='Price_Returns',price='Close',trading_periods=365,interval='daily',market_hours=24);

```
