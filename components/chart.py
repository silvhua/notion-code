
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
    fig = plot_by_category(classified_df, **kwargs)

@solara.component
def ChartsPerPeriod(category_column):
    periods = ['week', 'past_week', 'past_month', 'past_quarter']
    for period in periods:
        ElapsedTimeChart(
            category_column=category_column, classification='Unbilled', period=period, 
            agg='sum', sort_column='Elapsed', date_column='created_time'
            )