import sys
sys.path.append(r"/home/silvhua/custom_python")
sys.path.append(r"/home/silvhua/repositories/notion/src")
from silvhua import *
from wrangling import *
from data_viz import *
import os
import re

def get_invoice_records(df, start_date, end_date, filter_dict):
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

    period_df = filter_by_period(
        classified_df, column='created_time', period=None, start_date=start_date, end_date=end_date
    )
    client_df = filter_df_all_conditions(period_df, filter_dict, verbose=False)
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
        - start_date (datetime): The start date of the pay period.
        - end_date (datetime): The end date of the pay period.
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
    if client_df[unbilled_column].dtype == 'bool':
        client_df[unbilled_column] = client_df[unbilled_column].apply(
            lambda x: 'Billed Hours' if x else 'Unbilled Hours'
        )
    df = pd.DataFrame(client_df.groupby([project_column, unbilled_column])['Elapsed'].agg('sum'))

    df = df.unstack()
    df.columns = df.columns.droplevel()
    df.columns.name = None
    df = df.reset_index()
    df = df.fillna(0)
    return df

def create_invoice_pyfile(
    client_name, save_path, csv_filename, csv_path, filter_dict,
    save=True, **kwargs
    ):
    """
    Creates a Python file that generates an invoice for a given pay period.

    """

    file_string = f"""
import sys
sys.path.append(r"/home/silvhua/repositories/notion/src")
from invoicing import *
import solara

filename = 'notion_df.sav'
df = loadpickle(filename, '{csv_path}')

@solara.component
def Page():
    start_date, end_date = get_payperiod('{csv_filename}', '{csv_path}', {kwargs})
    client_df = get_invoice_records(df, start_date, end_date, {filter_dict})
    summary_df = time_per_project(client_df)
    solara.DataFrame(summary_df)
    """
    if save:
        path = save_path
        start_date, end_date = get_payperiod(
            f'{client_name}_payperiods.csv', csv_path, verbose=0
            )
        files_in_path = [re.sub(r'\d+_(.*)', r'\1', file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        filename_without_number = f'{client_name}_{end_date}'
        if f'{filename_without_number}.py' in files_in_path:
            print(f'\n.py file with end date {end_date} already exists in {path}; no new py file created.')
        else:
            number_of_files = len(files_in_path)
            filename = f'{1000-number_of_files}_{filename_without_number}'
            save_text(
                file_string, filename=filename, path=save_path, ext='py'
            )
    
    return file_string