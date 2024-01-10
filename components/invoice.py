import os
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
import solara
from silvhua import load_txt
import re

address_filepath = '/home/silvhua/repositories/notion/private'
@solara.component
def Load_Text(filename, path):
    text = load_txt(filename, path)
    text = text.replace('\n', '\n\n')
    return solara.Markdown(text)

@solara.component
def Invoice_Header(client: str):
    # solara.Title(f'Invoice') # Changes the page title from default, which is the cleaned script name
    with solara.Columns([1,1]):
        solara.Markdown('BILL TO:')
        solara.Markdown('FROM:')
    with solara.Columns([1,1]):
        Load_Text(f'{client}_address.txt', address_filepath)
        Load_Text('address.txt', address_filepath)

def Pages_Sidebar(path):
    subpages = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    # subpages.remove('0_Home.py')
    subpages.remove('__init__.py')
    subpages = sorted(subpages)
    # bunch of buttons which navigate to our dynamic route
    with solara.Sidebar():
        for subpage in subpages:
            route = re.sub(r'\d+_', '', subpage)
            route = re.sub('_', '-', route).lower()
            route = re.sub('.py', '', route)
            route = f'../{route}'
            with solara.Link(f'{route if route != "../home" else "/"}'):
            # with solara.Link(f'{pages_path}{route}'):
                solara.Button(label=f"{route.strip('./')}")