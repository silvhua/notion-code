
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
print(classified_df.columns)

@solara.component
def ElapsedTimeChart(**kwargs):
    fig = plot_by_category(classified_df, **kwargs)