
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from components.invoice import *
from silvhua import *
from components.invoice import *
import solara

client_name = 'OIF'
filter_dict = {'Task Project name': ['Coach McLoone', 'GHL Chatbot']}
rate = 40


@solara.component
def Page():
    Body(client_name, filter_dict, rate, gst_rate=0)