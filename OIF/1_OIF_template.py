
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