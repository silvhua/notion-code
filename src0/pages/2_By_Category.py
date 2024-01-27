import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.chart import *

category_column = 'Category'
@solara.component
def Page():
    ChartsPerPeriod(category_column)