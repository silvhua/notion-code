import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
from invoicing import *
import re

client_name = "OIF"
filter_dict = {
    'Category': ['Coach McLoone', 'GHL Chatbot']
}

save_path_root = f'/home/silvhua/repositories/notion/src'
csv_path = '/home/silvhua/repositories/notion/data'
file_string = create_invoice_pyfile(
    client_name, save_path_root, csv_path, filter_dict, verbose=1
    )
@solara.component
def Page():
    Home_Page(client_name, save_path_root)
