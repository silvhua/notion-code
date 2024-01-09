import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from components.invoice import *
from invoicing import *
import re

client_name = "Own it Fit"
save_path = '.'
csv_filename = 'OIF_payperiods.csv'
csv_path = '../../data'
filter_dict = {
    'Task Project name': ['Coach McLoone', 'GHL Chatbot']
}

file_string = create_invoice_pyfile(
    client_name, save_path, csv_filename, csv_path, filter_dict, verbose=1
    )
@solara.component
def Page(name: str = "foo"):
    subpages = ["2024-01-30"]
    solara.Markdown(f"You are at: {name}")
    # bunch of buttons which navigate to our dynamic route
    with solara.Row():
        for subpage in subpages:
            with solara.Link(re.sub('_', '-', subpage).lower()):
                solara.Button(label=f"Go to: {subpage}")
# @solara.component
# def Page():
#     ChartsPerPeriod(category_column)