import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
from invoicing import *
import re

client_name = "OIF"
save_path = '/home/silvhua/repositories/notion/src/OIF'
path = save_path
csv_filename = 'OIF_payperiods.csv'
csv_path = '/home/silvhua/repositories/notion/data'
filter_dict = {
    'Task Project name': ['Coach McLoone', 'GHL Chatbot']
}

file_string = create_invoice_pyfile(
    client_name, save_path, csv_filename, csv_path, filter_dict, verbose=1
    )
@solara.component
def Page():
    subpages = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    subpages.remove('0_Home.py')
    subpages.remove('__init__.py')
    # bunch of buttons which navigate to our dynamic route
    with solara.Row():
        for subpage in subpages:
            route = re.sub(r'\d+_', '', subpage)
            route = re.sub('_', '-', route).lower()
            route = re.sub('.py', '', route)
            with solara.Link(route):
                solara.Button(label=f"Go to: {route}")
