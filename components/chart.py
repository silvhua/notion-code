
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from wrangling import *
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from data_viz import *
import solara

filename = 'notion_df.sav'
path = '/home/silvhua/repositories/notion/data/'
df = loadpickle(filename, path)
classified_df = classify_projects(df)

@solara.component
def ElapsedTimeChart(**kwargs):
    
    classified_df['Date'] = classified_df['Name'].str.extract(r'(\d{4}-\d{2}-\d{2})', expand=False)
    fig = plot_by_category(classified_df, date_column='Date', **kwargs)

@solara.component
def ChartsPerPeriod(category_column):
    periods = ['week', 'past_week', 'past_month', 'past_quarter']
    for period in periods:
        ElapsedTimeChart(
            category_column=category_column, classification='Unbilled', period=period, 
            agg='sum', sort_column='Elapsed'
            )