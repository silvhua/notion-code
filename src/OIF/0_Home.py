import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
from invoicing import *
import re

client_name = "OIF"
filter_dict = {
    'Category': ['Coach McLoone', 'GHL Chatbot']
}
save_path = f'/home/silvhua/repositories/notion/src/{client_name}'
path = save_path
csv_filename = f'{client_name}_payperiods.csv'
csv_path = '/home/silvhua/repositories/notion/data'

file_string = create_invoice_pyfile(
    client_name, save_path, csv_filename, csv_path, filter_dict, verbose=1
    )
@solara.component
def Page():
    Home_Page(path)
