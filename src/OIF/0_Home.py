import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
from invoicing import *
import re

client_name = "OIF"
filter_dict = {
    'Task Project name': ['Coach McLoone', 'GHL Chatbot']
}
hourly_rate = 40
gst_rate = 0

### the rest remain the same across clients ### 
save_path_root = f'/home/silvhua/repositories/notion/src'
csv_path = '/home/silvhua/repositories/notion/data'
start_date, end_date = get_payperiod(f'{client_name}_payperiods.csv', csv_path, verbose=True)
print(f'\n**Creating invoice .py file**')
file_string = create_invoice_pyfile(
    client_name, start_date, end_date, filter_dict, hourly_rate, gst_rate,
    save_path_root, 
    )
@solara.component
def Page():
    Home_Page(client_name, save_path_root)
