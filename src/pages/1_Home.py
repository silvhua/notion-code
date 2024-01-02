import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.chart import *

@solara.component
def Page():
    ElapsedTimeChart(
        category_column='Task Project name', classification='Unbilled', period='week', 
        agg='sum', sort_column='Elapsed', date_column='created_time'
        )
    ElapsedTimeChart(
        category_column='Task Project name', classification='Unbilled', period='past_week', 
        agg='sum', sort_column='Elapsed', date_column='created_time'
        )