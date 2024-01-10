
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
from components.invoice import *
from silvhua import *
from invoicing import *
import solara

rate = 40
filename = 'notion_df.sav'
df = loadpickle(filename, '/home/silvhua/repositories/notion/data/')
client_name = 'OIF'
pages_path = f'/home/silvhua/repositories/notion/src/'
path = f'{pages_path}{client_name}'
start_date, end_date = get_payperiod('OIF_payperiods.csv', '/home/silvhua/repositories/notion/data/', {'index': 0, 'verbose': 1})
client_df = get_invoice_records(df, start_date, end_date, {'Task Project name': ['Coach McLoone', 'GHL Chatbot']})
summary_df = time_per_project(client_df).round(2)

total_hours = summary_df['Billed Hours'].sum() 
invoice_total = total_hours * rate

# invoice_table = f"""
#  Description | Amount
# --- | ----
# {total_hours:.2f} hours billed at ${rate}/hour | ${invoice_total:.2f}
# """
# html_table = f"""
# <table>
#   <thead>
#     <tr>
#       <th>Description</th>
#       <th>Amount</th>
#     </tr>
#   </thead>
#   <tbody>
#     <tr>
#       <td>{total_hours:.2f} hours billed at ${rate}/hour</td>
#       <td>${invoice_total:.2f}</td>
#     </tr>
#   </tbody>
# </table>
# """

@solara.component
def Page():
    Invoice_Header(client_name)
    Pages_Sidebar(path)
    solara.Markdown(f'**Service dates**: {start_date} - {end_date}')
    solara.Markdown(f'## Invoice Items')
    column_widths = [2, 1]
    with solara.Columns(column_widths):
        solara.HTML(tag='p', unsafe_innerHTML='<u>Description')
        solara.HTML(tag='p', unsafe_innerHTML='<u>Amount')
    with solara.Columns(column_widths):
        # solara.Markdown(invoice_table)
        solara.HTML(tag='p', unsafe_innerHTML=f'{total_hours:.2f} hours billed at ${rate}/hour')
        solara.HTML(tag='p', unsafe_innerHTML=f'<mark style="background-color: yellow;"><b>${invoice_total:.2f}')
    # solara.HTML(tag='p', unsafe_innerHTML=html_table)
    solara.Markdown("")
    solara.Markdown(f'## Time per Project')
    solara.DataFrame(summary_df)
    with solara.AppBarTitle():
        solara.Text(f'Silvia Hua')
    