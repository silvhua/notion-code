
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from components.invoice import *
from silvhua import *
from invoicing import *
import solara

filename = 'notion_df.sav'
df = loadpickle(filename, '/home/silvhua/repositories/notion/data/')
client_name = 'OIF'
pages_path = f'/home/silvhua/repositories/notion/src/'
path = f'{pages_path}{client_name}'

@solara.component
def Page():
    Invoice_Header(client_name)
    subpages = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    subpages.remove('0_Home.py')
    subpages.remove('__init__.py')
    # bunch of buttons which navigate to our dynamic route
    with solara.Sidebar():
        for subpage in subpages:
            route = re.sub(r'\d+_', '', subpage)
            route = re.sub('_', '-', route).lower()
            route = re.sub('.py', '', route)
            with solara.Link(f'../{route}'):
            # with solara.Link(f'{pages_path}{route}'):
                solara.Button(label=f"{route}")
    start_date, end_date = get_payperiod('OIF_payperiods.csv', '/home/silvhua/repositories/notion/data/', {'index': 0, 'verbose': 1})
    client_df = get_invoice_records(df, start_date, end_date, {'Task Project name': ['Coach McLoone', 'GHL Chatbot']})
    summary_df = time_per_project(client_df)
    solara.DataFrame(summary_df)
    