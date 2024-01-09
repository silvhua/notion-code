
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from invoicing import *
import solara

filename = 'notion_df.sav'
df = loadpickle(filename, '/home/silvhua/repositories/notion/data/')

@solara.component
def Page():
    start_date, end_date = get_payperiod('OIF_payperiods.csv', '/home/silvhua/repositories/notion/data/', {'index': 0, 'verbose': 1})
    client_df = get_invoice_records(df, start_date, end_date, {'Task Project name': ['Coach McLoone', 'GHL Chatbot']})
    summary_df = time_per_project(client_df)
    solara.DataFrame(summary_df)
    