import sys
sys.path.append(r"/home/silvhua/custom_python")
sys.path.append(r"/home/silvhua/repositories/notion/src")
from silvhua import *
from wrangling import *
from data_viz import *
import os
import re

def get_invoice_records(df, start_date, end_date, filter_dict, show_indices=False):
    """
    Retrieves relevant time tracking records for generating an invoice 
    based on the given DataFrame, start date, end date, and filter criteria.

    Parameters:
        df (DataFrame): The input DataFrame containing project records.
        start_date (str): The start date for filtering the project records. Format: 'YYYY-MM-DD'.
        end_date (str): The end date for filtering the project records.
        filter_dict (dict): A dictionary containing filtering criteria to be used in `filter_df_all_conditions`.

    Returns:
        DataFrame: The filtered DataFrame containing the invoice records.
    """
    classified_df = classify_projects(df)
    classified_df['Date'] = classified_df['Name'].str.extract(r'(\d{4}-\d{2}-\d{2})', expand=False)

    period_df = filter_by_period(
        classified_df, column='Date', period=None, start_date=start_date, end_date=end_date
    )
    client_df = filter_df_all_conditions(
        period_df, filter_dict, verbose=False, show_indices=show_indices
    )
    return client_df

def get_payperiod(csv_filename, path, verbose=False, index=0, strip_whitespaces=False):
    """
    Get the start date and end date of a pay period from a CSV file.

    Parameters:
        - csv_filename (str): The name of the CSV file.
        - path (str): The path to the CSV file.
        - verbose (bool, optional): If True, print the start date and end date.
        - index (int, optional): The index of the pay period dates CSV file to retrieve.
        - strip_whitespaces (bool, optional): If True, strip whitespaces from column names and values.

    Returns:
        - start_date (str): The start date of the pay period.
        - end_date (str): The end date of the pay period.
    """

    payperiods = load_csv(csv_filename, path)
    if strip_whitespaces:
        payperiods.columns = payperiods.columns.str.strip()
        payperiods = payperiods.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    payperiods = payperiods.sort_values(by='end_date', ascending=False)
    start_date = payperiods['start_date'].iloc[index]
    end_date = payperiods['end_date'].iloc[index]
    if verbose:
        print(f'\nStart date: {start_date}. End date: {end_date}')
    return start_date, end_date

def time_per_project(client_df, project_column='Task Project name', unbilled_column='Unbilled'):
    """
    Calculates the total time per project for a given client DataFrame.

    Args:
        client_df (DataFrame): The DataFrame containing client data.
        project_column (str, optional): The name of the column in client_df that represents the project. 
            Defaults to 'Task Project name'.
        unbilled_column (str, optional): The name of the column in client_df that represents whether the hours 
            are billed or unbilled. Defaults to 'Unbilled'.

    Returns:
        DataFrame: A DataFrame with the total time per project, grouped by project and billed/unbilled hours.
    """
    # print(f'client_df columns from time_per_project function before processing: {client_df.columns}')
    # print(f'\n{client_df}')
    if client_df[unbilled_column].dtype == 'bool':
        client_df[unbilled_column] = client_df[unbilled_column].apply(
            lambda x: 'Billed Hours' if x==False else 'Unbilled Hours'
        )
    summary_df = pd.DataFrame(client_df.groupby([project_column, unbilled_column])['Elapsed'].agg('sum'))
    summary_df = summary_df.sort_index(level=1)
    print(f'summary_df columns from time_per_project function before unstack: {summary_df.columns}')
    print(f'\n{summary_df}')

    summary_df = summary_df.unstack()
    summary_df.columns = summary_df.columns.droplevel()
    summary_df.columns.name = None
    summary_df = summary_df.reset_index()
    summary_df = summary_df.fillna(0)
    print(f'summary_df columns from time_per_project function: {summary_df.columns}')
    return summary_df

def create_invoice_pyfile(
    client_name, start_date, end_date, filter_dict, hourly_rate, gst_rate, 
    save_path_root, 
    save=True, **kwargs
    ):
    """
    Creates a Python file that generates an invoice for a given pay period.

    """
    save_path = f'{save_path_root}/{client_name}'
    print('**Replacing placeholders**')
    template_string = load_txt('invoice_template.txt', '/home/silvhua/repositories/notion/src/')
    file_string = re.sub(r'(.*)___client_name___(.*)', rf'\1{client_name}\2', template_string)
    file_string = re.sub(r'(.*)___filter_dict___(.*)', rf'\1{filter_dict}\2', file_string)
    file_string = re.sub(r'(.*)___hourly_rate___(.*)', rf'\1 {hourly_rate} \2', file_string)
    file_string = re.sub(r'(.*)___gst_rate___(.*)', rf'\1 {gst_rate} \2', file_string)
    file_string = re.sub(r'(.*)___start_date___(.*)', rf'\1 {start_date} \2', file_string)
    file_string = re.sub(r'(.*)___end_date___(.*)', rf'\1 {end_date} \2', file_string)
    # print(file_string)

    if save:
        path = save_path
        files_in_path = [re.sub(r'\d+_(.*)', r'\1', file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        filename_without_number = f'{client_name}_{end_date}'
        if f'{filename_without_number}.py' in files_in_path:
            print(f'.py file with end date {end_date} already exists in {path}; no new py file created.\n')
        else:
            number_of_files = len(files_in_path)
            filename = f'{1000-number_of_files}_{filename_without_number}'
            save_text(
                file_string, filename=filename, path=save_path, ext='py'
            )
    
    return file_string
    
def Create_Invoice_Timesheet(df, include_notes=True, unbilled_column='Unbilled'):
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
    if df['Roadmap Item'].apply(lambda x: len(x)>0).sum() > 0:
        invoice_columns.insert(2, 'Roadmap Item')
    if 'Notes' in df.columns:
        invoice_columns.append('Notes')
    df['Unbilled'] = df[unbilled_column].apply(lambda x: 'unbilled' if x==True else '')

    df = df[invoice_columns].round(2)
    return df