import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.chart import *

category_column = 'Task Project name'
@solara.component
def Page():
    ChartsPerPeriod(category_column)