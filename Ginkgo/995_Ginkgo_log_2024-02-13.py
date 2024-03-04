
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from components.invoice import *
from silvhua import *
from components.invoice import *
import solara

client_name = 'Ginkgo'

filter_dict = {'Category': ['Ginkgo']}
hourly_rate =  30 
gst_rate =  5 
start_date = ' 2024-01-29 '
end_date = ' 2024-02-13 '
start_date = start_date.strip()
end_date = end_date.strip()

@solara.component
def Page():
    Timesheet(
        client_name=client_name, start_date=start_date, end_date=end_date, 
        filter_dict=filter_dict, hourly_rate=hourly_rate, gst_rate=gst_rate
        )