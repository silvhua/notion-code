
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

# @solara.component
# def DataFrame()