import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.chart import *

category_column = 'Category'
@solara.component
def Page():
    ElapsedTimeChart(
        category_column=category_column, classification='Unbilled', period='week', 
        agg='sum', sort_column='Elapsed', date_column='created_time'
        )
    ElapsedTimeChart(
        category_column=category_column, classification='Unbilled', period='past_week', 
        agg='sum', sort_column='Elapsed', date_column='created_time'
        )