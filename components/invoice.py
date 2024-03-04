import os
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
sys.path.append(r"/home/silvhua/custom_python")
import solara
from silvhua import load_txt, check_sheet_existence
from invoicing import *
import re
# from typing import Any, Dict, Optional, cast

address_filepath = '/home/silvhua/repositories/notion/private'
# @solara.component
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
# @solara.component
def Body(client_name, start_date, end_date, filter_dict, hourly_rate, gst_rate=False, timesheet_filename='OIF_timesheet', sheet_name=None):
    filename = 'notion_df.sav'
    pages_path = f'/home/silvhua/repositories/notion/src/'
    path = f'{pages_path}{client_name}'
    data_path = '/home/silvhua/repositories/notion/data/'
    timesheet_save_path='/mnt/c/Users/silvh/OneDrive/Own It Fit/invoices'

    df = loadpickle(filename, data_path)
    client_df = get_invoice_records(df, start_date, end_date, filter_dict)
    summary_df = time_per_project(client_df) 
    showlegend = True if len(summary_df.columns) >2 else False

    solara.Title(f'{client_name}_{end_date}')
    with solara.AppBarTitle():
        solara.Text(f'Silvia Hua')
    Invoice_Header(client_name)
    Pages_Sidebar(path)
    solara.HTML('p', unsafe_innerHTML=f'<b>Service dates</b>: {start_date} - {end_date}')
    Itemized_Table(summary_df, hourly_rate, gst_rate)
    with solara.Column(align='start'):
        solara.Markdown("")
        solara.Markdown(f'## Time per Project')
        Df_To_Table(summary_df)
        client_df['Unbilled'] = client_df['Unbilled'].apply(lambda x: True if x=='Unbilled Hours' else False)
        if len(summary_df) > 1:
            CustomElapsedTimeChart(
                client_df, category_column='Task Project name',
                period=None, start_date=start_date, end_date=end_date, height=100+summary_df.shape[0]*10,
                aspect_ratio=2, show=False, showlegend=showlegend
                )
    # Invoice_Timesheet(client_df)
    timesheet_files = [file for file in os.listdir(timesheet_save_path) if os.path.isfile(os.path.join(timesheet_save_path, file))]
    sheet_name = f'{client_name}_{end_date}' if sheet_name == None else sheet_name
    timesheet_filename = f'{client_name}_{end_date}_timesheet' if timesheet_filename == None else timesheet_filename
    if check_sheet_existence(timesheet_filename, timesheet_save_path, sheet_name=sheet_name) == False:
        timesheet = Create_Invoice_Timesheet(client_df)
        save_excel(
            timesheet, 
            filename=timesheet_filename, path=timesheet_save_path, sheet_name=sheet_name, 
            col_width={
                0: 12,
                'B': 20,
                'G': 30,
                'H': 40
            }
        )

def Timesheet(client_name, start_date, end_date, filter_dict, hourly_rate, gst_rate=False):
    filename = 'notion_df.sav'
    pages_path = f'/home/silvhua/repositories/notion/src/'
    path = f'{pages_path}{client_name}'
    data_path = '/home/silvhua/repositories/notion/data/'

    df = loadpickle(filename, data_path)
    client_df = get_invoice_records(df, start_date, end_date, filter_dict)
    summary_df = time_per_project(client_df) 
    showlegend = True if len(summary_df.columns) >2 else False

    solara.Title(f'{client_name}_{end_date}')
    with solara.AppBarTitle():
        solara.Text(f'Silvia Hua')
    Invoice_Header(client_name)
    Pages_Sidebar(path)
    solara.HTML('p', unsafe_innerHTML=f'<b>Service dates</b>: {start_date} - {end_date}')
    Invoice_Timesheet(client_df)
    with solara.Column(align='start'):
        solara.Markdown("")
        solara.Markdown(f'## Time per Project')
        Df_To_Table(summary_df)
        if len(summary_df) > 1:
            client_df['Unbilled'] = client_df['Unbilled'].apply(lambda x: True if x=='Unbilled Hours' else False)
            CustomElapsedTimeChart(
                client_df, category_column='Task Project name',
                period=None, start_date=start_date, end_date=end_date, height=100+summary_df.shape[0]*10,
                aspect_ratio=2, show=False, showlegend=showlegend
                )
<<<<<<< HEAD
=======
    # Invoice_Timesheet(client_df)
    timesheet_files = [file for file in os.listdir(timesheet_save_path) if os.path.isfile(os.path.join(timesheet_save_path, file))]
    timesheet_filename = f'{client_name}_{end_date}_timesheet.xlsx'
    if timesheet_filename in timesheet_files:
        print(f'\nTimesheet file with end date {end_date} already exists in {timesheet_save_path}; no new timesheet file created.\n')
    else:
        timesheet = Create_Invoice_Timesheet(client_df)
        save_excel(
            timesheet, f'{client_name}_{end_date}_timesheet', path=timesheet_save_path, 
            col_width={
                0: 12,
                'B': 20,
                'G': 30,
                'H': 40
            }
        )

def Timesheet(client_name, start_date, end_date, filter_dict, hourly_rate, gst_rate=False):
    filename = 'notion_df.sav'
    pages_path = f'/home/silvhua/repositories/notion/src/'
    path = f'{pages_path}{client_name}'
    data_path = '/home/silvhua/repositories/notion/data/'

    df = loadpickle(filename, data_path)
    client_df = get_invoice_records(df, start_date, end_date, filter_dict)
    summary_df = time_per_project(client_df) 
    showlegend = True if len(summary_df.columns) >2 else False

    solara.Title(f'{client_name}_{end_date}')
    with solara.AppBarTitle():
        solara.Text(f'Silvia Hua')
    Invoice_Header(client_name)
    Pages_Sidebar(path)
    solara.HTML('p', unsafe_innerHTML=f'<b>Service dates</b>: {start_date} - {end_date}')
    Invoice_Timesheet(client_df)
    with solara.Column(align='start'):
        solara.Markdown("")
        solara.Markdown(f'## Time per Project')
        Df_To_Table(summary_df)
        if len(summary_df) > 1:
            client_df['Unbilled'] = client_df['Unbilled'].apply(lambda x: True if x=='Unbilled Hours' else False)
            CustomElapsedTimeChart(
                client_df, category_column='Task Project name',
                period=None, start_date=start_date, end_date=end_date, height=100+summary_df.shape[0]*10,
                aspect_ratio=2, show=False, showlegend=showlegend
                )
>>>>>>> c33b46e28e17551166e14bd7d88e606a76b58382

@solara.component
def Itemized_Table(summary_df, rate, gst_rate=5, column_widths=[3, 2, 1]):
    total_hours = summary_df['Billed Hours'].sum()
    services_total = total_hours * rate
    solara.Markdown(f'## Invoice Items')
    # items_df = pd.DataFrame(columns=['Description', 'Amount'])
    # items_df.loc[0] = [f'{total_hours:.2f} hours billed at ${rate}/hour']
    style = "line-height: 0.001;"
    with solara.Columns(column_widths):
        solara.HTML(tag='h4', style=style, unsafe_innerHTML='<u>Description')
        with solara.Column(align='end'):
            solara.HTML(tag='h4', style=style, unsafe_innerHTML='<u>Amount')
        solara.HTML(tag='div', style=style, unsafe_innerHTML='')
    highlight_style = '<mark style="background-color: yellow; border: 1px solid black;"><b>'
    with solara.Columns(column_widths):
        solara.HTML(tag='div', style=style, unsafe_innerHTML=f'{total_hours:.2f} hours billed at ${rate}/hour')
        subtotal_text = f'${services_total:.2f}'
        subtotal_html = f'{highlight_style}{subtotal_text}' if gst_rate==False else subtotal_text
        with solara.Column(align='end'):
            solara.HTML(tag='div', style=style, unsafe_innerHTML=subtotal_html)
        solara.HTML(tag='div', style=style, unsafe_innerHTML='')
    if gst_rate:
        with solara.Columns(column_widths):
            gst_amount = services_total * gst_rate/100
            solara.HTML(tag='div', style=style, unsafe_innerHTML=f'GST {gst_rate}%')
            with solara.Column(align='end'):
                solara.HTML(tag='div', style=style, unsafe_innerHTML=f'${gst_amount:.2f}')
            solara.HTML(tag='div', style=style, unsafe_innerHTML='')
        with solara.Columns(column_widths):
            total = services_total + gst_amount
            solara.HTML(tag='div', style=style, unsafe_innerHTML=f'<b>TOTAL')
            with solara.Column(align='end'):
                solara.HTML(tag='h3', style=style, unsafe_innerHTML=f'{highlight_style}${total:.2f}')
            solara.HTML(tag='div', style=style, unsafe_innerHTML='')


# @solara.component
def CustomElapsedTimeChart(classified_df, show, **kwargs):
    fig, aggregate_df = plot_by_category(classified_df, date_column='Date', show=show, **kwargs)
    solara.FigurePlotly(fig)
        
@solara.component
def Show_Df(df, round=2, items_per_page=50):
    solara.DataFrame(
        df=df.round(round) if round else df,
        items_per_page=items_per_page,
        scrollable=True
        )
@solara.component
def Df_To_Table(df, round=2):
    table_string = df.round(round).to_markdown() if round else df.to_markdown()
    solara.Markdown(table_string)

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
            route = solara.resolve_path(route, level=-1)
            with solara.Link(f'{route if route != "/home" else "/"}'):
                solara.Button(label=f"{route.split('/')[-1]}")
                # solara.Button(label=f"{route}")


@solara.component
def Invoice_Timesheet(df, include_notes=True, unbilled_column='Unbilled'):
    df = Create_Invoice_Timesheet(df, include_notes=include_notes, unbilled_column=unbilled_column)
    df.columns = [f'| {column}' for column in df.columns]
    df = df.fillna('')
    Show_Df(df)

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
    