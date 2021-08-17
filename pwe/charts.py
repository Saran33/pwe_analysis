#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 19:59:32 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import warnings
import os
import time
from datetime import datetime, date, timedelta, timezone
import pandas as pd
import numpy as np
import numpy.ma as ma
from pandas_summary import DataFrameSummary
#from isoweek import Week

import plotly
import cufflinks as cf
#Enabling the offline mode for interactive plotting locally
import plotly.io as pio
#pio.templates
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
#sinit_notebook_mode(connected=True)
#cf.go_offline()
#To display the plots
#%matplotlib inline

# get_ipython().run_line_magic('matplotlib', 'inline')
import webbrowser
import dateutil
import re

# https://strftime.org/
td = date.today()
today = td.strftime("%d-%m-%Y")
today_dmy = str(today)

utc_now = datetime.utcnow()
utc_now.isoformat()
today_utc = utc_now.strftime("%d-%m-%Y")

end_date = today_dmy
end = datetime.strptime(td.strftime('%Y-%m-%d'),'%Y-%m-%d')

# utc_end = pd.to_datetime(utc_end)
utc_end = pd.Timestamp.utcnow()

interval = timedelta(1)
yesterday = td - interval
yest = yesterday.strftime("%d-%m-%Y")
yesterday_dmy = str(yest)

chart_start = utc_now - timedelta(days=365)
auto_start = chart_start.strftime("%d-%m-%Y")

def define_period(df, start_date, end_date):
    dates = pd.date_range(start_date,end_date)
    sdate = str(start_date)
    edate = str(end_date)
    chart_dates = str(sdate+" - "+edate)
    return sdate, edate, chart_dates;

PWE_skin = "#DCBBA6"
black = "#000000"
PWE_grey = "#64646F"
PWE_blue = "#a4b3c1"
ironsidegrey = "#6F6F64"
PWE_light_grey = "#a5a5a5"
PWE_ig_light_grey ='#58595b'
PWE_ig_dark_grey = '#403d3e'
vic_teal = '#d1d3d4'
PWE_black ='#231f20'

transparent = '#DCBBA600'

PWE_mono_darker = "#CE9F81"

#analagous:
PWE_yellow = "#DCD6A6"
PWE_red = "#DCA6AC"

PWE_triadic_teal = "#A6DCBB"
PWE_triadic_purple = "#BBA6DC"

#tetradic:
PWE_green = "#ACDCA6"
RegentStBlue = "#A6C7DC"
PWE_pinkyPurple = "#D6A6DC"
    
PWE_video_teal = "#006C5E"

#transparent: https://gist.github.com/lopspower/03fb1cc0ac9f32ef38f4
PWE_skin80_h = "#dcbaa6"
PWE_skin_20 = "#DCBBA633"
PWE_skin_38 = "#DCBBA661"
henanigans_light1 = "#A4A4A4"

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

"""
Cuffliks:
# https://analyticsindiamag.com/beginners-guide-to-data-visualisation-with-plotly-cufflinks/
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh

Quant Figure:
Docs: https://jpoles1.github.io/cufflinks/html/cufflinks.quant_figure.html#cufflinks.quant_figure.QuantFig.add_annotations
https://plotly.com/python/ohlc-charts/
https://jpoles1.github.io/cufflinks/html/cufflinks.quant_figure.html
https://plotly.com/python/reference/#layout-annotations
http://jorgesantos.io/slides/plotcon.qf.slides.html#/8  (Best)
https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh#5
https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code

Tweak paramaters: check the signature of these methods by pressing Shift + Tab in the Jupyter notebook.
- add_bollinger_bands() - It adds Bollinger Bands (BOLL) study to the figure.
- add_volume() - It adds volume bar charts to the figure.
- add_sma() - It adds Simple Moving Average (SMA) study to the figure.
- add_rsi() - It adds Relative Strength Indicator (RSI) study to the figure.
- add_adx() - It adds Average Directional Index (ADX) study to the figure.
- add_cci() - It adds Commodity Channel Indicator study to the figure.
- add_dmi() - It adds Directional Movement Index (DMI) study to the figure.
- add_ema() - It adds Exponential Moving Average (EMA) to the figure.
- add_atr() - It adds Average True Range (ATR) study to the figure.
- add_macd() - It adds Moving Average Convergence Divergence (MACD) to the figure.
- add_ptps() - It adds Parabolic SAR (PTPS) study to the figure.
- add_resistance() - It adds resistance line to the figure.
- add_trendline() - It adds trend line to the figure.
- add_support() - It adds support line to the figure.

Use: cf.help() or cf.help(figure) to see paramaters

"""

def quant_chart(df,start_date,end_date,ticker=None,theme='henanigans',auto_start=auto_start,auto_end=today):
    """
    
    Plots a chart in an iPython Notebook. This function will not remove Plotly tags or populate as a new browser tab.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
        boll_color = 'black'
        
    else :
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        boll_color = vic_teal #PWE_ig_light_grey
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    title = ('{}: {}'.format(ticker, chart_dates))
    
    qf = cf.QuantFig(df, title=title,legend='top',name=ticker,
                             rangeslider=False,up_color=PWE_skin,down_color=PWE_grey, fontfamily='Roboto',theme=theme) # theme='ggplot'
    
    # To make a permanent change to theme:
    qf.theme.update(up_color=PWE_skin,down_color=PWE_grey)
    
    # A rangeselector allows us to select different periods on the same chart. This can be any variety of Year, Months, Hours etc.
    # For example: steps=['1y','2 months','5 weeks','ytd','2mtd']
    rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                        bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto')
    qf.layout.update(rangeselector=rangeselector)
    
    # # Add an annotation:
    # qf.layout['annotations']['values']=[]
    # qf.add_annotations({'2019-07-26':'CME Exp.',
    #                    '2020-07-24':'CME Exp.',
    #                    '2021-04-23':'CME Exp.'},
    #                    showarrow=True,y=0,
    #                    arrowhead=6,arrowcolor=arrowcolor,fontcolor=fontcolor,
    #                    fontsize=12,textangle=0,yanchor="bottom", fontfamily='Roboto')
    
    ## Add a support or resistance line:
    #qf.add_support(date='2021-04-23',on='low',mode='starttoend', to_strfmt='%Y-%m-%d',color=PWE_blue) #text='resistance',
    
    boll_std=2
    periods=20
    qf.add_bollinger_bands(periods=periods,boll_std=boll_std,colors=[boll_color,PWE_skin_38],fill=True, name=f"BOLL({boll_std},{periods})")
    
    qf.add_volume(datalegend=True,legendgroup=True, name="Volume",showlegend=False,up_color=PWE_grey)
    
    #qf.layout.update(showlegend=True)
    
    #for trace in qf['data']: 
    #    if(trace == 'Volume'): trace['datalegend'] = False
    
    
    qf.iplot(hspan=dict(y0=38196,y1=44000,color=PWE_skin,fill=True,opacity=.3,yref='y2'),
             rangeslider=False,xrange=[auto_start,auto_end])
    
    #qf.iplot(rangeslider=False)
    
    theme = qf.theme['theme']
    return;

#def quant_chart_int(df, theme='henanigans'):

def check_folder(name):
    '''
    Check if directory exists, if not, create it
    name : a string for the directory name.
    
    '''
    check_path = os.path.isdir(name)
    print (f"checking if {name} directory exists...")

    if not check_path:
        os.makedirs(name)
        print("created folder : ", name)
    else:
        print(name, "folder already exists.")
        return name;

def add_tags(qf,tags=None,auto_start=auto_start,auto_end=today,theme='white',showarrow=True,arrowhead=6,fontsize=6,textangle=0,yanchor="bottom",fontfamily='Roboto'):
    """
    For some reaso, this will not format the textangle correctly. Copy and paste the function into a otebook andit will work correcty.
    Add settlement dates or other annotations to a figure.
    Pass in a column of annotations  in string format.
    
    """
    if tags!=None:
        dark = ("henanigans", "solar", "space")
        if str(theme) in dark:
            fontcolor = 'henanigans_light1'
            arrowcolor = 'henanigans_light1'
            style = 'dark'
        else : 
            fontcolor = PWE_ig_light_grey
            arrowcolor = PWE_ig_light_grey
            style = theme
        
        # Add an annotation:
        qf.layout['annotations']['values']=[]
        qf.add_annotations(tags,
                           showarrow=True,y=0,
                           arrowhead=arrowhead,arrowcolor=arrowcolor,fontcolor=fontcolor,
                           fontsize=fontsize,textangle=0,yanchor=yanchor,fontfamily=fontfamily)
        #qf.iplot(xrange=[auto_start,auto_ensd])
    else:
        pass
    return;
    
def pwe_format(f_name):
    print(f_name)
    cwd = os.getcwd()
    file_path_str = f'{cwd}{f_name}'
    file_path = f'{file_path_str}.html'
    print(file_path_str)
    print(file_path)
    print('')
    
    # https://www.geeksforgeeks.org/python-os-path-relpath-method/
    prefix = cwd
    relative_path = f'/{os.path.relpath(file_path,prefix)}'
    print(prefix)
    print(relative_path)
    print('')
    
    local_path_str = f'{f_name}'
    local_file_path = f'/{local_path_str}.html'
    # unf_link = f'http://localhost:8888/view{local_file_path}'
    unf_link = f'http://localhost:8888/view{relative_path}'
    print(local_path_str)
    print(local_file_path)
    print(unf_link,"(unformatted)")

    # Swap between local_path_str and relative_path for the "unf_link" calc and the 'link" clac below if 
    # the charts arent displaying in browser automatically. Or else change cwd.
    
    text_wrapper = open(file_path, encoding="utf-8")
    html_text = text_wrapper.read()
    #print(html_text)
    
    # https://www.freecodeformat.com/svg-editor.php
    plotly_svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 132 132'><defs><style>.cls-1 {fill: #3f4f75;} .cls-2 {fill: #80cfbe;} .cls-3 {fill: #fff;}</style></defs><title>plotly-logomark</title><g id='symbol'><rect class='cls-1' width='132' height='132' rx='6' ry='6'/><circle class='cls-2' cx='78' cy='54' r='6'/><circle class='cls-2' cx='102' cy='30' r='6'/><circle class='cls-2' cx='78' cy='30' r='6'/><circle class='cls-2' cx='54' cy='30' r='6'/><circle class='cls-2' cx='30' cy='30' r='6'/><circle class='cls-2' cx='30' cy='54' r='6'/><path class='cls-3' d='M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z'/><path class='cls-3' d='M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z'/><path class='cls-3' d='M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z'/><path class='cls-3' d='M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z'/></g></svg>"
    pwe_svg= "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 127.74 132'><defs><style>.a{fill:#dcbba6;}.b{fill:none;}.c{fill:#646470;}</style></defs><title>pwe-logomark</title><g id='symbol'><rect class='a' x='0.34' y='9.19' width='122.81' height='122.81'/><path class='b' d='M109.16,16.78l-40,101.35L50,65.11c-1.86,2.81-3.78,5.82-5.86,8.88C31.8,92.18,17.09,113.56,4.33,131.88H122.81V52.56l-4-10.32C116.3,35.5,112.52,25.53,109.16,16.78Z'/><path d='M111.7,8.38,109.2,2,69.4,102.84,51.46,53.18l-3,4.46C45.8,61.7,42.87,66.27,39.65,71,28.58,87.34,13,110,0,128.64v3.24H4.33C17.09,113.56,31.8,92.18,44.16,74c2.08-3.06,4-6.07,5.86-8.88l19.16,53,40-101.35c3.36,8.75,7.14,18.72,9.67,25.46l4,10.32V37.47C119.62,29,115.12,17.19,111.7,8.38Z'/><polygon class='c' points='61.84 55.95 55.97 65.64 58.34 72.16 60.6 68.42 71.28 97.98 74.28 90.38 61.84 55.95'/><path class='c' d='M121.92,0c-3.13,7.94-6.47,16.37-10,25.12-3.9,9.82-8,20.05-12.12,30.48C93,72.78,86,90.48,79.88,105.9l-2.79-7.74-3,7.6,5.57,15.41,2.62-6.65C88.92,97.68,97,77.3,104.87,57.59c3.3-8.28,6.68-16.78,10-25.12C119.44,21,123.88,9.78,127.74,0Z'/></g></svg>"
    
    
    # https://codepen.io/plotly/pen/EVgeWb
    # https://rdrr.io/cran/plotly/man/config.html
    # https://stackoverflow.com/questions/36554705/adding-config-modes-to-plotly-py-offline-modebar
    # https://gist.github.com/neo01124/449bc7df9f25c6ef055c7efbd2d89a3a
    # https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar
    
    name = f_name
    file = open(file_path).read()
    
    replaced_txt = file.replace('"linkText": "Export to plot.ly",', '"linkText": "PWE Capital",')
    replaced_txt2 = replaced_txt.replace('"plotlyServerURL": "https://plot.ly"', '"plotlyServerURL": "https://pwecapital.com/"')
    replaced_txt3 = replaced_txt2.replace('"X svg a":"fill:#447adb;","X svg a:hover":"fill:#3c6dc5;",', '"X svg a":"fill:#64646F;","X svg a:hover":"fill:#DCBBA6;",')
    replaced_txt4 = replaced_txt3.replace(plotly_svg, pwe_svg)
    replaced_txt5 = replaced_txt4.replace('e.href="https://plotly.com/",', 'e.href="https://pwecapital.com/",')
    replaced_txt6 = replaced_txt5.replace('Produced with Plotly', 'Redefining R.O.I.™')
    replaced_txt7 = replaced_txt6.replace('background:#69738a', 'background:#64646F')
    replaced_txt8 = replaced_txt7.replace('#8c97af', '#64646F')
    replaced_txt9 = replaced_txt8.replace('rgba(140,151,175,.9)', 'rgba(100, 100, 111, .9)')
    
    output_html = f"{file_path_str}_PWE.html"
    writer = open(output_html,'w')
    writer.write(replaced_txt9) 
    writer.close()
    
    # output_html_path = f"/{file_name}"
    # # chart_html = f"http://localhost:8888/view{local_path_str}_PWE.html"
    # # https://www.geeksforgeeks.org/python-os-path-splitext-method/
    # root_ext = os.path.splitext(file_path)
    # root = root_ext[0]
    # relative_path = f'/{os.path.realpath(root,prefix)}'
    # chart_html = f"file:///{relative_path}_PWE.html"
    
    ##
    output_html_path = f"{cwd}{f_name}"
    abs_path = f'/{os.path.abspath(output_html)}'
    #chart_html = f"http://localhost:8888/view{local_path_str}_PWE.html"
    chart_html = f"http://localhost:8888/view{local_path_str}"
    #chart_html = f"http://localhost:8888/view{relative_path}"
    #chart_file = f"file:///{relative_path}_PWE.html"
    chart_file = f"file:///{abs_path}"
    
    #webbrowser.open_new_tab("chrome://newtab")
    webbrowser.open_new_tab(chart_file)
    print(output_html_path)
    print(chart_html)
    print(chart_file)
    
    # Swap between local_path_str and relative_path for the "chart_html" calc if 
    # the charts aren't displaying in browser automatically. Or else change cwd to match the chart directory.
    
    return chart_html, chart_file;
    
def quant_chart_int(df,start_date,end_date,ticker=None,theme='henanigans',auto_start=auto_start,auto_end=today,asPlot=True,
                    showlegend=True,boll_std=2,boll_periods=20,showboll=False,showrsi=False,rsi_periods=14,
                   showama=False,ama_periods=9,showvol=False,show_price_range=False,tags=None,textangle=0):
    """
    
    df : The Pandas dataframe used for the chart. It must contain open, high, low and close, and may also contain volume. Anything else will be ignored, unless specified.
    
    Plots an interactive chart and opens it in a new browser tab. This function also formats the plot with PWE branding.
    
    # https://notebook.community/santosjorge/cufflinks/Cufflinks%20Tutorial%20-%20Colors
    
    Themes: ‘ggplot’,  'pearl’, 'solar’, 'space’, 'white’, 'polar’, 'henanigans’, 
    
    auto_start : The start date for the range that will automatically display on the chart. e.g. if set to the start of this year,
    the range will automatically display YTD, until a user clicks a different range. The default setting is 1 year prior to today's date, in GMT time.
    
    auto_end : The end date for the range that will automatically display on the chart. The default setting is today's date, in GMT time.
    
    asPlot : Whether to save it as a HTML plot. If True, it will save the plot and open it in a new browser tab.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = str(theme)
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    title = ('{}: {}'.format(ticker, chart_dates))
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    qf = cf.QuantFig(df, title=title,legend='top',name=ticker,
                             rangeslider=False,up_color=PWE_skin,down_color=PWE_grey, fontfamily='Roboto',theme=theme,
                    top_margin=0.9,spacing=0.08,xrange=[auto_start,auto_end]) # theme='ggplot'
    
    # To make a permanent change to theme:
    qf.theme.update(up_color=PWE_skin,down_color=PWE_grey)
    
    # A rangeselector allows us to select different periods on the same chart. This can be any variety of Year, Months, Hours etc.
    # For example: steps=['1y','2 months','5 weeks','ytd','2mtd']
    rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                        bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto')

    qf.layout.update(rangeselector=rangeselector)
    
    #Add an annotation:
    add_tags(qf, tags=tags)

    
    # Add a support or resistance line:
    #qf.add_support(date='2021-04-23',on='low',mode='starttoend', to_strfmt='%Y-%m-%d',color=PWE_blue) #text='resistance',
    
    if showboll==True:
        qf.add_bollinger_bands(periods=boll_periods,boll_std=boll_std,colors=['black',PWE_skin_38],fill=True, name=f"BOLL({boll_std},{boll_periods})")
    else:
        pass
    qf.layout.update(showlegend=showlegend)
    if showama==True:
        qf.add_ama(periods=ama_periods,width=2,color=[PWE_blue,vic_teal],legendgroup=False)
    else:
        pass
    if showrsi==True:
        qf.add_rsi(periods=rsi_periods,color=PWE_skin,legendgroup=False)
    else:
        pass
    if showvol==True:
        qf.add_volume(datalegend=True,legendgroup=True,name="Volume",showlegend=False,up_color=PWE_grey)
    else:
        pass
    
    #for trace in qf['data']: 
    #    if(trace == 'Volume'): trace['datalegend'] = False
    
    if show_price_range==True:
        fig = qf.iplot(hspan=dict(y0=41553.01,y1=50460.96,color=PWE_skin,fill=True,opacity=.3,yref='y2'),
                       rangeslider=False,asPlot=asPlot, filename=f'.{f_name}', auto_open=False)
    else:
        fig = qf.iplot(rangeslider=False,asPlot=asPlot,filename=f'.{f_name}', auto_open=False)
            
    #fig = go.Figure(fig,) 
    
    # qf.iplot(layout=dict(legend=dict(x=0.1, y=0.1)))
    #qf.iplot(title=title,rangeslider=False,layout= {"margin": {
    #            "b": 30,
    #            "l": 30,
    #            "r": 30,
    #            "t": 30
    #        }})
    
    # my_fig = df.iplot(asFigure=True)
    # my_fig.layout.legend=dict(x=-.1, y=.1)
    # my_fig.iplot() # filename='line-example.html'
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;


def single_chart(df,start_date,end_date,columns=None,kind='scatter',title=None,ticker=None,yTitle=None,showlegend=False,asPlot=False,
                      theme='white',auto_start=auto_start,auto_end=today,connectgaps=False):
    """
    
    Plots a line or scatter chart within an iPython notebook. It will not format HTML with PWE style or open in a browser window.
    
    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.
    
    kind : set 'scatter' for a line chart.
    
    Select the text 'iplot' in the function below and click shift and tab for more options.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
        
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    file_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    if columns is None:
        plt_int = df.iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{file_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    else:
        plt_int = df[columns].iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{file_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    
    
    #rangeslider: {range:['2021-01-01', '2021-08-10']}
    #range=['2021-01-01','2021-08-10']
    #add_range_selector(plt_int, axis_name='xaxis', ranges=None, default=None)
    
    #fig = go.Figure(df)
    #fig.show()
    
    print(file_name)
    return plt_int, file_name;

# help(brr.iplot)
# cf.tools.get_range_selector

def pwe_line_chart(df,start_date,end_date,columns=None,kind='scatter',title=None,ticker=None,yTitle=None,asPlot=False,theme='white',
                   showlegend=False,auto_start=auto_start,auto_end=today,connectgaps=False):
    """
    
    Plots an interactive line or scatter chart and opens it in a new browser. It also formats HTML with PWE style.
    
    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.
    
    kind : set 'scatter' for a line chart.
    
    Select the text 'iplot' in the function below and click shift and tab for more options.
    
    """    
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
        
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    if columns is None:
        plt_int = df.iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=colors,fontfamily='Roboto',theme=theme,
                           asPlot=asPlot, filename=f'./{f_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    else:
        plt_int = df[columns].iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{f_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;

def pwe_return_dist_chart(df,start_date,end_date,tseries='Price_Returns',kind='scatter',title=None, ticker=None,yTitle=None,asPlot=False,theme='white',
                          showlegend=False,auto_start=auto_start,auto_end=today,connectgaps=False,
                         tickformat='%',decimals=2): # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """
	*Put start_date ad end_date after df and before other arguemets, with no = to any value or it will throw an error.
    
    Plots an interactive returns distribiution chart and formats the HTML with PWE style.
    
    df : The dataframe to plot. 
    
    returns : a pandas series within the dataframe which contains % returns per time period.
    
    tickformat : the format for the y axis. e.g % or $.
    
    decimals: the number of decimals to round the number quoted in the hover info panel.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    df['Series_str'] = df[tseries]
    
    df['Series_str'] = pd.Series([round(val, 6) for val in df[tseries]], index = df.index)
    df['Series_str'] = pd.Series([f"{val*100:.{decimals}f}%" for val in df['Series_str']], index = df.index)
  
    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
        
    text = df['Date_Ret_str'].values.tolist()
    
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_return_dist_{style}'
    
    plt_int = df[tseries].iplot(kind=kind,showlegend=showlegend,legend='top',rangeslider=False,
                               title=chart_title,xTitle='Date', yTitle=yTitle,
                       colors=colors,fontfamily='Roboto',theme=theme,
                       asPlot=asPlot, filename=f'./{f_name}',
                       rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto', x=-0.025, y=1, visible=True),
                       xrange = [auto_start,auto_end],connectgaps=connectgaps,yaxis_tickformat=tickformat,
                       hoverinfo="text", text=text) #hovertemplate=hovertemplate
    
    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    #plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'

    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;

def pwe_return_bar_chart(df,start_date,end_date,tseries='Price_Returns',kind='scatter',title=None,ticker=None,yTitle=None,xTitle=None,asPlot=False,theme='white',
                          showlegend=False,auto_start=auto_start,auto_end=today,
                         tickformat='%',decimals=2,orientation='v',textangle=0): # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """
    
    Plots an interactive bar chart with the HTML formatted to the PWE style. It opens the plot in a new browser tab.
    
    orientation :     'v' is vertical.
                    'h' is horizontal.
    
    textangle :        The angle of the text to display on each bar. 0 is horizontal and -90 is vertical.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df,start_date,end_date);
    
    df['Series_str'] = df[tseries]
    df['Series_str'] = pd.Series([round(val, 6) for val in df[tseries]], index = df.index)
    df['Series_str'] = pd.Series([f"{val*100:.{decimals}f}%" for val in df['Series_str']], index = df.index)
    
    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
        
    hovertext = df['Date_Ret_str'].values.tolist()
    text = df['Series_str'].values.tolist()
    
    if orientation=='h':
        xTitle = yTitle
        yTitle = 'Date'
    else:
        xTitle = 'Date'
        yTitle = yTitle
    
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_return_dist_{style}'
    
    plt_int = df[tseries].iplot(kind=kind,showlegend=showlegend,legend='top',rangeslider=False,
                               title=chart_title,xTitle=xTitle, yTitle=yTitle,
                       colors=colors,fontfamily='Roboto',theme=theme,
                       asPlot=asPlot, filename=f'./{f_name}',
                       rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto', x=-0.025, y=1, visible=True),
                       xrange = [auto_start,auto_end],yaxis_tickformat=tickformat,hoverinfo="text",
                       hovertext=hovertext,text=text,orientation=orientation,
                               textangle=textangle) #hovertemplate=hovertemplate
    
    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    #plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file,plt_int;
  
def add_range_selector(layout, axis_name='xaxis', ranges=None, default=None):    
    """Add a rangeselector to the layout if it doesn't already have one.
    
    This code is only needed if switching to Plotly from Cufflinks.
    
    :param ranges: which ranges to add, e.g. ['3m', '1y', 'ytd']
    :param default_range: which range to choose as the default, e.g. '3m'
    """
    axis = layout.setdefault(axis_name, dict())
    axis.setdefault('type', 'date')
    axis.setdefault('rangeslider', dict())
    if ranges is None:
        # Make some nice defaults
        ranges = ['1m', '6m', 'ytd', '1y', 'all']
    re_split = re.compile('(\d+)')
    def range_split(range):
        split = re.split(re_split, range)
        assert len(split) == 3
        return (int(split[1]), split[2])
    # plotly understands m, but not d or y!
    step_map = dict(d='day', m='month', y='year')
    def make_button(range):
        range = range.lower()
        if range == 'all':
            return dict(step='all')
        elif range == 'ytd':
            return dict(count=1,
                label='YTD',
                step='year',
                stepmode='todate')
        else:
            (count, step) = range_split(range)
            step = step_map.get(step, step)
            return dict(count=count,
                label=range,
                step=step,
                stepmode='backward')
    axis.setdefault('rangeselector', dict(buttons=[make_button(r) for r in ranges]))
    if default is not None and default != 'all':
        end_date = datetime.datetime.today()
        if default.lower() == 'ytd':
            start_date = datetime.date(end_date.year, 1, 1)
        else:
            (count, step) = range_split(default)
            step = step_map[step] + 's'  # relativedelta needs plurals
            start_date = (end_date - dateutil.relativedelta.relativedelta(**{step: count}))
        axis.setdefault('range', [start_date, end_date])#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 19:59:32 2021

@author: Saran Connolly saran.c@pwecapital.com
"""

import warnings
import os
import time
from datetime import datetime, date, timedelta, timezone
import pandas as pd
import numpy as np
import numpy.ma as ma
from pandas_summary import DataFrameSummary
#from isoweek import Week

import plotly
import cufflinks as cf
#Enabling the offline mode for interactive plotting locally
import plotly.io as pio
#pio.templates
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objects as go
#sinit_notebook_mode(connected=True)
#cf.go_offline()
#To display the plots
#%matplotlib inline

# get_ipython().run_line_magic('matplotlib', 'inline')
import webbrowser
import dateutil
import re

# https://strftime.org/
td = date.today()
today = td.strftime("%d-%m-%Y")
today_dmy = str(today)

utc_now = datetime.utcnow()
utc_now.isoformat()
today_utc = utc_now.strftime("%d-%m-%Y")

end_date = today_dmy
end = datetime.strptime(td.strftime('%Y-%m-%d'),'%Y-%m-%d')

# utc_end = pd.to_datetime(utc_end)
utc_end = pd.Timestamp.utcnow()

interval = timedelta(1)
yesterday = td - interval
yest = yesterday.strftime("%d-%m-%Y")
yesterday_dmy = str(yest)

chart_start = utc_now - timedelta(days=365)
auto_start = chart_start.strftime("%d-%m-%Y")

def define_period(df, start_date, end_date):
    dates = pd.date_range(start_date,end_date)
    sdate = str(start_date)
    edate = str(end_date)
    chart_dates = str(sdate+" - "+edate)
    return sdate, edate, chart_dates;

PWE_skin = "#DCBBA6"
black = "#000000"
PWE_grey = "#64646F"
PWE_blue = "#a4b3c1"
ironsidegrey = "#6F6F64"
PWE_light_grey = "#a5a5a5"
PWE_ig_light_grey ='#58595b'
PWE_ig_dark_grey = '#403d3e'
vic_teal = '#d1d3d4'
PWE_black ='#231f20'

transparent = '#DCBBA600'

PWE_mono_darker = "#CE9F81"

#analagous:
PWE_yellow = "#DCD6A6"
PWE_red = "#DCA6AC"

PWE_triadic_teal = "#A6DCBB"
PWE_triadic_purple = "#BBA6DC"

#tetradic:
PWE_green = "#ACDCA6"
RegentStBlue = "#A6C7DC"
PWE_pinkyPurple = "#D6A6DC"
    
PWE_video_teal = "#006C5E"

#transparent: https://gist.github.com/lopspower/03fb1cc0ac9f32ef38f4
PWE_skin80_h = "#dcbaa6"
PWE_skin_20 = "#DCBBA633"
PWE_skin_38 = "#DCBBA661"
henanigans_light1 = "#A4A4A4"

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

"""
Cuffliks:
# https://analyticsindiamag.com/beginners-guide-to-data-visualisation-with-plotly-cufflinks/
# https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh

Quant Figure:
Docs: https://jpoles1.github.io/cufflinks/html/cufflinks.quant_figure.html#cufflinks.quant_figure.QuantFig.add_annotations
https://plotly.com/python/ohlc-charts/
https://jpoles1.github.io/cufflinks/html/cufflinks.quant_figure.html
https://plotly.com/python/reference/#layout-annotations
http://jorgesantos.io/slides/plotcon.qf.slides.html#/8  (Best)
https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh#5
https://coderzcolumn.com/tutorials/data-science/cufflinks-how-to-create-plotly-charts-from-pandas-dataframe-with-one-line-of-code

Tweak paramaters: check the signature of these methods by pressing Shift + Tab in the Jupyter notebook.
- add_bollinger_bands() - It adds Bollinger Bands (BOLL) study to the figure.
- add_volume() - It adds volume bar charts to the figure.
- add_sma() - It adds Simple Moving Average (SMA) study to the figure.
- add_rsi() - It adds Relative Strength Indicator (RSI) study to the figure.
- add_adx() - It adds Average Directional Index (ADX) study to the figure.
- add_cci() - It adds Commodity Channel Indicator study to the figure.
- add_dmi() - It adds Directional Movement Index (DMI) study to the figure.
- add_ema() - It adds Exponential Moving Average (EMA) to the figure.
- add_atr() - It adds Average True Range (ATR) study to the figure.
- add_macd() - It adds Moving Average Convergence Divergence (MACD) to the figure.
- add_ptps() - It adds Parabolic SAR (PTPS) study to the figure.
- add_resistance() - It adds resistance line to the figure.
- add_trendline() - It adds trend line to the figure.
- add_support() - It adds support line to the figure.

Use: cf.help() or cf.help(figure) to see paramaters

"""

def quant_chart(df,start_date,end_date,ticker=None,theme='henanigans',auto_start=auto_start,auto_end=today):
    """
    
    Plots a chart in an iPython Notebook. This function will not remove Plotly tags or populate as a new browser tab.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
        boll_color = 'black'
        
    else :
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        boll_color = vic_teal #PWE_ig_light_grey
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    title = ('{}: {}'.format(ticker, chart_dates))
    
    qf = cf.QuantFig(df, title=title,legend='top',name=ticker,
                             rangeslider=False,up_color=PWE_skin,down_color=PWE_grey, fontfamily='Roboto',theme=theme) # theme='ggplot'
    
    # To make a permanent change to theme:
    qf.theme.update(up_color=PWE_skin,down_color=PWE_grey)
    
    # A rangeselector allows us to select different periods on the same chart. This can be any variety of Year, Months, Hours etc.
    # For example: steps=['1y','2 months','5 weeks','ytd','2mtd']
    rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                        bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto')
    qf.layout.update(rangeselector=rangeselector)
    
    # # Add an annotation:
    # qf.layout['annotations']['values']=[]
    # qf.add_annotations({'2019-07-26':'CME Exp.',
    #                    '2020-07-24':'CME Exp.',
    #                    '2021-04-23':'CME Exp.'},
    #                    showarrow=True,y=0,
    #                    arrowhead=6,arrowcolor=arrowcolor,fontcolor=fontcolor,
    #                    fontsize=12,textangle=0,yanchor="bottom", fontfamily='Roboto')
    
    ## Add a support or resistance line:
    #qf.add_support(date='2021-04-23',on='low',mode='starttoend', to_strfmt='%Y-%m-%d',color=PWE_blue) #text='resistance',
    
    boll_std=2
    periods=20
    qf.add_bollinger_bands(periods=periods,boll_std=boll_std,colors=[boll_color,PWE_skin_38],fill=True, name=f"BOLL({boll_std},{periods})")
    
    qf.add_volume(datalegend=True,legendgroup=True, name="Volume",showlegend=False,up_color=PWE_grey)
    
    #qf.layout.update(showlegend=True)
    
    #for trace in qf['data']: 
    #    if(trace == 'Volume'): trace['datalegend'] = False
    
    
    qf.iplot(hspan=dict(y0=38196,y1=44000,color=PWE_skin,fill=True,opacity=.3,yref='y2'),
             rangeslider=False,xrange=[auto_start,auto_end])
    
    #qf.iplot(rangeslider=False)
    
    theme = qf.theme['theme']
    return;

#def quant_chart_int(df, theme='henanigans'):

def check_folder(name):
    '''
    Check if directory exists, if not, create it
    name : a string for the directory name.
    
    '''
    check_path = os.path.isdir(name)
    print (f"checking if {name} directory exists...")

    if not check_path:
        os.makedirs(name)
        print("created folder : ", name)
    else:
        print(name, "folder already exists.")
        return name;

def add_tags(qf,tags=None,auto_start=auto_start,auto_end=today,theme='white',showarrow=True,arrowhead=6,fontsize=6,textangle=0,yanchor="bottom",fontfamily='Roboto'):
    """
    For some reaso, this will not format the textangle correctly. Copy and paste the function into a otebook andit will work correcty.
    Add settlement dates or other annotations to a figure.
    Pass in a column of annotations  in string format.
    
    """
    if tags!=None:
        dark = ("henanigans", "solar", "space")
        if str(theme) in dark:
            fontcolor = 'henanigans_light1'
            arrowcolor = 'henanigans_light1'
            style = 'dark'
        else : 
            fontcolor = PWE_ig_light_grey
            arrowcolor = PWE_ig_light_grey
            style = theme
        
        # Add an annotation:
        qf.layout['annotations']['values']=[]
        qf.add_annotations(tags,
                           showarrow=True,y=0,
                           arrowhead=arrowhead,arrowcolor=arrowcolor,fontcolor=fontcolor,
                           fontsize=fontsize,textangle=0,yanchor=yanchor,fontfamily=fontfamily)
        #qf.iplot(xrange=[auto_start,auto_ensd])
    else:
        pass
    return;
    
def pwe_format(f_name):
    print(f_name)
    cwd = os.getcwd()
    file_path_str = f'{cwd}{f_name}'
    file_path = f'{file_path_str}.html'
    print(file_path_str)
    print(file_path)
    print('')
    
    # https://www.geeksforgeeks.org/python-os-path-relpath-method/
    prefix = cwd
    relative_path = f'/{os.path.relpath(file_path,prefix)}'
    print(prefix)
    print(relative_path)
    print('')
    
    local_path_str = f'{f_name}'
    local_file_path = f'/{local_path_str}.html'
    # unf_link = f'http://localhost:8888/view{local_file_path}'
    unf_link = f'http://localhost:8888/view{relative_path}'
    print(local_path_str)
    print(local_file_path)
    print(unf_link,"(unformatted)")

    # Swap between local_path_str and relative_path for the "unf_link" calc and the 'link" clac below if 
    # the charts arent displaying in browser automatically. Or else change cwd.
    
    text_wrapper = open(file_path, encoding="utf-8")
    html_text = text_wrapper.read()
    #print(html_text)
    
    # https://www.freecodeformat.com/svg-editor.php
    plotly_svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 132 132'><defs><style>.cls-1 {fill: #3f4f75;} .cls-2 {fill: #80cfbe;} .cls-3 {fill: #fff;}</style></defs><title>plotly-logomark</title><g id='symbol'><rect class='cls-1' width='132' height='132' rx='6' ry='6'/><circle class='cls-2' cx='78' cy='54' r='6'/><circle class='cls-2' cx='102' cy='30' r='6'/><circle class='cls-2' cx='78' cy='30' r='6'/><circle class='cls-2' cx='54' cy='30' r='6'/><circle class='cls-2' cx='30' cy='30' r='6'/><circle class='cls-2' cx='30' cy='54' r='6'/><path class='cls-3' d='M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z'/><path class='cls-3' d='M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z'/><path class='cls-3' d='M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z'/><path class='cls-3' d='M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z'/></g></svg>"
    pwe_svg= "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 127.74 132'><defs><style>.a{fill:#dcbba6;}.b{fill:none;}.c{fill:#646470;}</style></defs><title>pwe-logomark</title><g id='symbol'><rect class='a' x='0.34' y='9.19' width='122.81' height='122.81'/><path class='b' d='M109.16,16.78l-40,101.35L50,65.11c-1.86,2.81-3.78,5.82-5.86,8.88C31.8,92.18,17.09,113.56,4.33,131.88H122.81V52.56l-4-10.32C116.3,35.5,112.52,25.53,109.16,16.78Z'/><path d='M111.7,8.38,109.2,2,69.4,102.84,51.46,53.18l-3,4.46C45.8,61.7,42.87,66.27,39.65,71,28.58,87.34,13,110,0,128.64v3.24H4.33C17.09,113.56,31.8,92.18,44.16,74c2.08-3.06,4-6.07,5.86-8.88l19.16,53,40-101.35c3.36,8.75,7.14,18.72,9.67,25.46l4,10.32V37.47C119.62,29,115.12,17.19,111.7,8.38Z'/><polygon class='c' points='61.84 55.95 55.97 65.64 58.34 72.16 60.6 68.42 71.28 97.98 74.28 90.38 61.84 55.95'/><path class='c' d='M121.92,0c-3.13,7.94-6.47,16.37-10,25.12-3.9,9.82-8,20.05-12.12,30.48C93,72.78,86,90.48,79.88,105.9l-2.79-7.74-3,7.6,5.57,15.41,2.62-6.65C88.92,97.68,97,77.3,104.87,57.59c3.3-8.28,6.68-16.78,10-25.12C119.44,21,123.88,9.78,127.74,0Z'/></g></svg>"
    
    
    # https://codepen.io/plotly/pen/EVgeWb
    # https://rdrr.io/cran/plotly/man/config.html
    # https://stackoverflow.com/questions/36554705/adding-config-modes-to-plotly-py-offline-modebar
    # https://gist.github.com/neo01124/449bc7df9f25c6ef055c7efbd2d89a3a
    # https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar
    
    name = f_name
    file = open(file_path).read()
    
    replaced_txt = file.replace('"linkText": "Export to plot.ly",', '"linkText": "PWE Capital",')
    replaced_txt2 = replaced_txt.replace('"plotlyServerURL": "https://plot.ly"', '"plotlyServerURL": "https://pwecapital.com/"')
    replaced_txt3 = replaced_txt2.replace('"X svg a":"fill:#447adb;","X svg a:hover":"fill:#3c6dc5;",', '"X svg a":"fill:#64646F;","X svg a:hover":"fill:#DCBBA6;",')
    replaced_txt4 = replaced_txt3.replace(plotly_svg, pwe_svg)
    replaced_txt5 = replaced_txt4.replace('e.href="https://plotly.com/",', 'e.href="https://pwecapital.com/",')
    replaced_txt6 = replaced_txt5.replace('Produced with Plotly', 'Redefining R.O.I.™')
    replaced_txt7 = replaced_txt6.replace('background:#69738a', 'background:#64646F')
    replaced_txt8 = replaced_txt7.replace('#8c97af', '#64646F')
    replaced_txt9 = replaced_txt8.replace('rgba(140,151,175,.9)', 'rgba(100, 100, 111, .9)')
    
    output_html = f"{file_path_str}_PWE.html"
    writer = open(output_html,'w')
    writer.write(replaced_txt9) 
    writer.close()
    
    # output_html_path = f"/{file_name}"
    # # chart_html = f"http://localhost:8888/view{local_path_str}_PWE.html"
    # # https://www.geeksforgeeks.org/python-os-path-splitext-method/
    # root_ext = os.path.splitext(file_path)
    # root = root_ext[0]
    # relative_path = f'/{os.path.realpath(root,prefix)}'
    # chart_html = f"file:///{relative_path}_PWE.html"
    
    ##
    output_html_path = f"{cwd}{f_name}"
    abs_path = f'/{os.path.abspath(output_html)}'
    #chart_html = f"http://localhost:8888/view{local_path_str}_PWE.html"
    chart_html = f"http://localhost:8888/view{local_path_str}"
    #chart_html = f"http://localhost:8888/view{relative_path}"
    #chart_file = f"file:///{relative_path}_PWE.html"
    chart_file = f"file:///{abs_path}"
    
    #webbrowser.open_new_tab("chrome://newtab")
    webbrowser.open_new_tab(chart_file)
    print(output_html_path)
    print(chart_html)
    print(chart_file)
    
    # Swap between local_path_str and relative_path for the "chart_html" calc if 
    # the charts aren't displaying in browser automatically. Or else change cwd to match the chart directory.
    
    return chart_html, chart_file;
    
def quant_chart_int(df,start_date,end_date,ticker=None,theme='henanigans',auto_start=auto_start,auto_end=today,asPlot=True,
                    showlegend=True,boll_std=2,boll_periods=20,showboll=False,showrsi=False,rsi_periods=14,
                   showama=False,ama_periods=9,showvol=False,show_price_range=False,tags=None,textangle=0):
    """
    
    df : The Pandas dataframe used for the chart. It must contain open, high, low and close, and may also contain volume. Anything else will be ignored, unless specified.
    
    Plots an interactive chart and opens it in a new browser tab. This function also formats the plot with PWE branding.
    
    # https://notebook.community/santosjorge/cufflinks/Cufflinks%20Tutorial%20-%20Colors
    
    Themes: ‘ggplot’,  'pearl’, 'solar’, 'space’, 'white’, 'polar’, 'henanigans’, 
    
    auto_start : The start date for the range that will automatically display on the chart. e.g. if set to the start of this year,
    the range will automatically display YTD, until a user clicks a different range. The default setting is 1 year prior to today's date, in GMT time.
    
    auto_end : The end date for the range that will automatically display on the chart. The default setting is today's date, in GMT time.
    
    asPlot : Whether to save it as a HTML plot. If True, it will save the plot and open it in a new browser tab.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = str(theme)
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    title = ('{}: {}'.format(ticker, chart_dates))
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    qf = cf.QuantFig(df, title=title,legend='top',name=ticker,
                             rangeslider=False,up_color=PWE_skin,down_color=PWE_grey, fontfamily='Roboto',theme=theme,
                    top_margin=0.9,spacing=0.08,xrange=[auto_start,auto_end]) # theme='ggplot'
    
    # To make a permanent change to theme:
    qf.theme.update(up_color=PWE_skin,down_color=PWE_grey)
    
    # A rangeselector allows us to select different periods on the same chart. This can be any variety of Year, Months, Hours etc.
    # For example: steps=['1y','2 months','5 weeks','ytd','2mtd']
    rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                        bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto')

    qf.layout.update(rangeselector=rangeselector)
    
    #Add an annotation:
    add_tags(qf, tags=tags)

    
    # Add a support or resistance line:
    #qf.add_support(date='2021-04-23',on='low',mode='starttoend', to_strfmt='%Y-%m-%d',color=PWE_blue) #text='resistance',
    
    if showboll==True:
        qf.add_bollinger_bands(periods=boll_periods,boll_std=boll_std,colors=['black',PWE_skin_38],fill=True, name=f"BOLL({boll_std},{boll_periods})")
    else:
        pass
    qf.layout.update(showlegend=showlegend)
    if showama==True:
        qf.add_ama(periods=ama_periods,width=2,color=[PWE_blue,vic_teal],legendgroup=False)
    else:
        pass
    if showrsi==True:
        qf.add_rsi(periods=rsi_periods,color=PWE_skin,legendgroup=False)
    else:
        pass
    if showvol==True:
        qf.add_volume(datalegend=True,legendgroup=True,name="Volume",showlegend=False,up_color=PWE_grey)
    else:
        pass
    
    #for trace in qf['data']: 
    #    if(trace == 'Volume'): trace['datalegend'] = False
    
    if show_price_range==True:
        fig = qf.iplot(hspan=dict(y0=41553.01,y1=50460.96,color=PWE_skin,fill=True,opacity=.3,yref='y2'),
                       rangeslider=False,asPlot=asPlot, filename=f'.{f_name}', auto_open=False)
    else:
        fig = qf.iplot(rangeslider=False,asPlot=asPlot,filename=f'.{f_name}', auto_open=False)
            
    #fig = go.Figure(fig,) 
    
    # qf.iplot(layout=dict(legend=dict(x=0.1, y=0.1)))
    #qf.iplot(title=title,rangeslider=False,layout= {"margin": {
    #            "b": 30,
    #            "l": 30,
    #            "r": 30,
    #            "t": 30
    #        }})
    
    # my_fig = df.iplot(asFigure=True)
    # my_fig.layout.legend=dict(x=-.1, y=.1)
    # my_fig.iplot() # filename='line-example.html'
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;


def single_chart(df,start_date,end_date,columns=None,kind='scatter',title=None,ticker=None,yTitle=None,showlegend=False,asPlot=False,
                      theme='white',auto_start=auto_start,auto_end=today,connectgaps=False):
    """
    
    Plots a line or scatter chart within an iPython notebook. It will not format HTML with PWE style or open in a browser window.
    
    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.
    
    kind : set 'scatter' for a line chart.
    
    Select the text 'iplot' in the function below and click shift and tab for more options.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
        
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    file_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    if columns is None:
        plt_int = df.iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{file_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    else:
        plt_int = df[columns].iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{file_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    
    
    #rangeslider: {range:['2021-01-01', '2021-08-10']}
    #range=['2021-01-01','2021-08-10']
    #add_range_selector(plt_int, axis_name='xaxis', ranges=None, default=None)
    
    #fig = go.Figure(df)
    #fig.show()
    
    print(file_name)
    return plt_int, file_name;

# help(brr.iplot)
# cf.tools.get_range_selector

def pwe_line_chart(df,start_date,end_date,columns=None,kind='scatter',title=None,ticker=None,yTitle=None,asPlot=False,theme='white',
                   showlegend=False,auto_start=auto_start,auto_end=today,connectgaps=False):
    """
    
    Plots an interactive line or scatter chart and opens it in a new browser. It also formats HTML with PWE style.
    
    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.
    
    kind : set 'scatter' for a line chart.
    
    Select the text 'iplot' in the function below and click shift and tab for more options.
    
    """    
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
        
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_interative_{style}'
    
    if columns is None:
        plt_int = df.iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=colors,fontfamily='Roboto',theme=theme,
                           asPlot=asPlot, filename=f'./{f_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    else:
        plt_int = df[columns].iplot(kind=kind,showlegend=showlegend,rangeslider=False,
                           title=chart_title,xTitle='Date', yTitle=yTitle,
                           colors=[PWE_skin,PWE_grey],fontfamily='Roboto',
                           theme=theme,asPlot=asPlot, filename=f'.{f_name}',
                      rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],
                                         bgcolor=(PWE_skin,.2),fontsize=12,fontfamily='Roboto',
                                         x=-0.025, y=1,visible=True),xrange=[auto_start,auto_end],
                      connectgaps=connectgaps)
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;

def pwe_return_dist_chart(df,start_date,end_date,tseries='Price_Returns',kind='scatter',title=None, ticker=None,yTitle=None,asPlot=False,theme='white',
                          showlegend=False,auto_start=auto_start,auto_end=today,connectgaps=False,
                         tickformat='%',decimals=2): # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """
	*Put start_date ad end_date after df and before other arguemets, with no = to any value or it will throw an error.
    
    Plots an interactive returns distribiution chart and formats the HTML with PWE style.
    
    df : The dataframe to plot. 
    
    returns : a pandas series within the dataframe which contains % returns per time period.
    
    tickformat : the format for the y axis. e.g % or $.
    
    decimals: the number of decimals to round the number quoted in the hover info panel.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df, start_date, end_date);
    
    df['Series_str'] = df[tseries]
    
    df['Series_str'] = pd.Series([round(val, 6) for val in df[tseries]], index = df.index)
    df['Series_str'] = pd.Series([f"{val*100:.{decimals}f}%" for val in df['Series_str']], index = df.index)
    
    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
        
    text = df['Date_Ret_str'].values.tolist()
    
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_return_dist_{style}'
    
    plt_int = df[tseries].iplot(kind=kind,showlegend=showlegend,legend='top',rangeslider=False,
                               title=chart_title,xTitle='Date', yTitle=yTitle,
                       colors=colors,fontfamily='Roboto',theme=theme,
                       asPlot=asPlot, filename=f'./{f_name}',
                       rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto', x=-0.025, y=1, visible=True),
                       xrange = [auto_start,auto_end],connectgaps=connectgaps,yaxis_tickformat=tickformat,
                       hoverinfo="text", text=text) #hovertemplate=hovertemplate
    
    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    #plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'

    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file;

def pwe_return_bar_chart(df,start_date,end_date,tseries='Price_Returns',kind='scatter',title=None,ticker=None,yTitle=None,xTitle=None,asPlot=False,theme='white',
                          showlegend=False,auto_start=auto_start,auto_end=today,
                         tickformat='%',decimals=2,orientation='v',textangle=0): # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """
    
    Plots an interactive bar chart with the HTML formatted to the PWE style. It opens the plot in a new browser tab.
    
    orientation :     'v' is vertical.
                    'h' is horizontal.
    
    textangle :        The angle of the text to display on each bar. 0 is horizontal and -90 is vertical.
    
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark :
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else : 
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme
        
    colors=[PWE_skin,PWE_grey,black,vic_teal,PWE_blue,PWE_ig_light_grey,PWE_ig_dark_grey]
    
    auto_start = str(auto_start)
    auto_end = str(auto_end)
    
    sdate,edate,chart_dates = define_period(df,start_date,end_date);
    
    df['Series_str'] = df[tseries]
    df['Series_str'] = pd.Series([round(val, 6) for val in df[tseries]], index = df.index)
    df['Series_str'] = pd.Series([f"{val*100:.{decimals}f}%" for val in df['Series_str']], index = df.index)
    
    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
        
    hovertext = df['Date_Ret_str'].values.tolist()
    text = df['Series_str'].values.tolist()
    
    if orientation=='h':
        xTitle = yTitle
        yTitle = 'Date'
    else:
        xTitle = 'Date'
        yTitle = yTitle
    
    #chart_title = '{} ({}) : {}'.format(title,ticker,chart_dates)
    chart_title = '{} ({})'.format(title,ticker)
    check_folder('charts')
    f_name= f'/charts/{ticker}_{sdate}-{edate}_return_dist_{style}'
    
    plt_int = df[tseries].iplot(kind=kind,showlegend=showlegend,legend='top',rangeslider=False,
                               title=chart_title,xTitle=xTitle, yTitle=yTitle,
                       colors=colors,fontfamily='Roboto',theme=theme,
                       asPlot=asPlot, filename=f'./{f_name}',
                       rangeselector=dict(steps=['Reset','3Y','2Y','1Y','YTD','6M', '1M'],bgcolor=(PWE_skin,.2),
                                        fontsize=12,fontfamily='Roboto', x=-0.025, y=1, visible=True),
                       xrange = [auto_start,auto_end],yaxis_tickformat=tickformat,hoverinfo="text",
                       hovertext=hovertext,text=text,orientation=orientation,
                               textangle=textangle) #hovertemplate=hovertemplate
    
    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    #plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'
    
    chart_html, chart_file = pwe_format(f_name)
    
    return chart_html, chart_file,plt_int;
  
def add_range_selector(layout, axis_name='xaxis', ranges=None, default=None):    
    """Add a rangeselector to the layout if it doesn't already have one.
    
    This code is only needed if switching to Plotly from Cufflinks.
    
    :param ranges: which ranges to add, e.g. ['3m', '1y', 'ytd']
    :param default_range: which range to choose as the default, e.g. '3m'
    """
    axis = layout.setdefault(axis_name, dict())
    axis.setdefault('type', 'date')
    axis.setdefault('rangeslider', dict())
    if ranges is None:
        # Make some nice defaults
        ranges = ['1m', '6m', 'ytd', '1y', 'all']
    re_split = re.compile('(\d+)')
    def range_split(range):
        split = re.split(re_split, range)
        assert len(split) == 3
        return (int(split[1]), split[2])
    # plotly understands m, but not d or y!
    step_map = dict(d='day', m='month', y='year')
    def make_button(range):
        range = range.lower()
        if range == 'all':
            return dict(step='all')
        elif range == 'ytd':
            return dict(count=1,
                label='YTD',
                step='year',
                stepmode='todate')
        else:
            (count, step) = range_split(range)
            step = step_map.get(step, step)
            return dict(count=count,
                label=range,
                step=step,
                stepmode='backward')
    axis.setdefault('rangeselector', dict(buttons=[make_button(r) for r in ranges]))
    if default is not None and default != 'all':
        end_date = datetime.datetime.today()
        if default.lower() == 'ytd':
            start_date = datetime.date(end_date.year, 1, 1)
        else:
            (count, step) = range_split(default)
            step = step_map[step] + 's'  # relativedelta needs plurals
            start_date = (end_date - dateutil.relativedelta.relativedelta(**{step: count}))
        axis.setdefault('range', [start_date, end_date])