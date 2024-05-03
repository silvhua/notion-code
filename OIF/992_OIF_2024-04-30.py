
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from components.invoice import *
from silvhua import *
from components.invoice import *
import solara

client_name = 'OIF'

filter_dict = {'Task Project name': ['Coach McLoone', 'GHL Chatbot']}
hourly_rate =  40 
gst_rate =  0 
start_date = ' 2024-04-01 '
end_date = ' 2024-04-30 '
start_date = start_date.strip()
end_date = end_date.strip()

@solara.component
def Page():
    Body(
        client_name=client_name, start_date=start_date, end_date=end_date, 
        filter_dict=filter_dict, hourly_rate=hourly_rate, gst_rate=gst_rate
        )