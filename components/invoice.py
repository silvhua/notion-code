import os
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
import solara
from silvhua import load_txt
from invoicing import *
import re
from typing import Any, Dict, Optional, cast

address_filepath = '/home/silvhua/repositories/notion/private'
@solara.component
def Home_Page(client_name, save_path_root):
    path = f'{save_path_root}/{client_name}'
    solara.Title('Silvia Hua Invoicing')
    subpages = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    print(f'{subpages}')
    subpages.remove('0_Home.py')
    subpages.remove('__init__.py')
    # bunch of buttons which navigate to our dynamic route
    with solara.Row():
        for subpage in subpages:
            route = re.sub(r'\d+_', '', subpage)
            route = re.sub('_', '-', route).lower()
            route = re.sub('.py', '', route)
            with solara.Link(f'{route}'):
                solara.Button(label=f"Go to: {route}")
@solara.component
def Body(client_name, filter_dict, rate):
    filename = 'notion_df.sav'
    data_path = '/home/silvhua/repositories/notion/data/'
    pages_path = f'/home/silvhua/repositories/notion/src/'
    path = f'{pages_path}{client_name}'

    df = loadpickle(filename, data_path)
    start_date, end_date = get_payperiod(f'{client_name}_payperiods.csv', data_path, {'index': 0, 'verbose': 1})
    client_df = get_invoice_records(df, start_date, end_date, filter_dict)
    summary_df = time_per_project(client_df)
    total_hours = summary_df['Billed Hours'].sum() 
    invoice_total = total_hours * rate

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
    Show_Df(summary_df)
    with solara.AppBarTitle():
        solara.Text(f'Silvia Hua')
    # Invoice_Timesheet(client_df)
        
@solara.component
def Show_Df(df, round=2, items_per_page=50):
    solara.DataFrame(
        df=df.round(round) if round else df,
        items_per_page=items_per_page,
        scrollable=True
        )

@solara.component
def Load_Text(filename, path, first_line_tag='h3'):
    text = load_txt(filename, path)
    if first_line_tag:
        html_string = f'<{first_line_tag}>'
    else:
        html_string = ''
    lines = text.split('\n')
    line_no = 0
    for line in lines:
        html_string +=f'<br>{line}' 
        if first_line_tag and line_no == 0:
            html_string += f'</{first_line_tag}>'
        line_no += 1
    solara.HTML(tag='p', unsafe_innerHTML=html_string)

@solara.component
def Invoice_Header(client: str):
    # solara.Title(f'Invoice') # Changes the page title from default, which is the cleaned script name
    with solara.Columns([1,1]):
        solara.Text('BILL TO:')
        solara.Text('FROM:')
    with solara.Columns([1,1]):
        Load_Text(f'{client}_address.txt', address_filepath, first_line_tag='h3')
        Load_Text('address.txt', address_filepath, first_line_tag='h3')

@solara.component
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


@solara.component
def Invoice_Timesheet(df, include_notes=True, unbilled_column='Unbilled'):
    df['Date'] = df['Name'].str.extract(r'(\d{4}-\d{2}-\d{2})', expand=False)
    invoice_columns = [
        'Date',
        'Task Project name',
        'start time',
        'end time',
        'Elapsed',
        'Unbilled',
        'Task Name'
    ]
    # if include_roadmap_item:
    #     invoice_columns.insert(2, 'Roadmap Item')
    if df['Roadmap Item'].apply(lambda x: len(x)>0).sum() > 0:
        invoice_columns.insert(2, 'Roadmap Item')
    if 'Notes' in df.columns:
        invoice_columns.append('Notes')
    df['Unbilled'] = df[unbilled_column].apply(lambda x: 'unbilled' if x=='Unbilled Hours' else '')

    df = df[invoice_columns].round(2)
    df.columns = [f'| {column}' for column in df.columns]
    Show_Df(df)
    