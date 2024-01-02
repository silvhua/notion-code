import plotly.graph_objects as go
from wrangling import *
from silvhua_plot import *

def classify_unbilled(df, column='Flag', flag_name='do not bill'):
    """
    Parses the JSON data in the `Flag` column and 
    classifies the unbilled items in a DataFrame based on a specified column and flag name.

    Parameters:
        - df (pandas.DataFrame): The DataFrame containing the items to be classified.
        - column (str, optional): The name of the column containing the flag JSON data. Defaults to 'Flag'.
        - flag_name (str, optional): The name of the flag used for classification. Defaults to 'do not bill'.

    Returns:
        - pandas.DataFrame: A copy of the input DataFrame with an additional 'Unbilled' column indicating whether each item is unbilled or not.
    """

    def parse_flag(row, flag_name=flag_name):
        if row[column]:
            for flag in row[column]:
                if flag['name'] == flag_name:
                    return True
                else:
                    return False
        else:
            return False

    classified_df = df.copy()
    classified_df['Unbilled'] = classified_df.apply(parse_flag, axis=1)
    return classified_df

    
def classify_projects(df, column='Task Project name', tag_column='Task Project tags'):
    """
    Classifies projects and updates the 'Unbilled' column based on certain conditions. 

    Args:
        df (pandas.DataFrame): The input DataFrame containing project data.
        column (str, optional): The column name for project names. Defaults to 'Task Project name'.
        tag_column (str, optional): The column name for project tags. Defaults to 'Task Project tags'.

    Returns:
        pandas.DataFrame: The classified DataFrame with added 'Category' and 'Unbilled' columns.
    """
    def classify(row):
        tag_set = set(row[tag_column]) if len(row[tag_column]) > 0 else {row[tag_column]}
        if ('ginkgo' in row[column].lower()) | ('ginkgo work' in [tag.lower() for tag in row[tag_column]]):
            row['Category'] = 'Ginkgo'
        elif row[column].lower() in ['ghl chatbot', 'tech business']:
            row['Category'] = 'tech business'
            if row[column].lower() == 'tech business':
                row['Unbilled'] = True
        elif tag_set.intersection({'portfolio', 'tech ed'}):
            row['Category'] = 'tech career development'
            row['Unbilled'] = True
        elif 'defy time fitness' in [tag.lower() for tag in row[tag_column]]:
            row['Category'] = 'personal training work'
            if 'defy time fitness' not in row[column].lower():
                row['Unbilled'] = True
        elif row[column].lower() == 'career positioning':
            row['Category'] = 'career positioning'
            row['Unbilled'] = True
        elif 'admin' in [tag.lower() for tag in row[tag_column]]:
            row['Category'] = 'admin'
            row['Unbilled'] = True
        elif 'volunteer' in [tag.lower() for tag in row[tag_column]]:
            row['Category'] = 'volunteer'
            row['Unbilled'] = True
        else:
            row['Category'] = 'Other'
            row['Unbilled'] = True

        return row
    
    classified_df = classify_unbilled(df).apply(lambda x: classify(x), axis=1)
    unique_categories = classified_df['Category'].unique()
    print(f'There are {len(unique_categories)} categories: {[category for category in unique_categories]}')
    return classified_df

def plot_by_category(
    classified_df, category_column='Category', classification='Unbilled', label=True,
    agg='sum', sort_column='Elapsed', date_column='created_time', height=None,
    period='past_month', start_date=None, end_date=None
    ):
    """
    Plot the data by category and return an aggregated DataFrame.

    Parameters:
        classified_df (DataFrame): The input DataFrame that has been classified using `classify_projects` function.
        category_column (str, optional): The column name for the category. Defaults to 'Category'.
        classification (str, optional): The classification for filtering the data. Defaults to 'Unbilled'.
        label (bool, optional): Whether to label the plot. Defaults to True.
        agg (str, optional): The aggregation method. Defaults to 'sum'.
        sort_column (str, optional): The column name for sorting. Defaults to 'Elapsed'.
        date_column (str, optional): The column name for the date. Defaults to 'created_time'.
        height (int, optional): The height of the plot. Defaults to None.
        period (str, optional): The period for filtering the data. Defaults to 'past_month'.
        start_date (str, optional): The start date for filtering the data. Defaults to None.
        end_date (str, optional): The end date for filtering the data. Defaults to None.

    Returns:
        Figure: A plot of the data grouped by the category.
        DataFrame: An aggregated DataFrame grouped by the category and sorted by the sort column.
    """
    print(f'Total rows: {len(classified_df)}')
    filtered_df = filter_by_period(classified_df, column=date_column, period=period, start_date=start_date, end_date=end_date)
    min_date = filtered_df[date_column].min()
    max_date = filtered_df[date_column].max()
    print(f'Data based on {len(filtered_df)} rows')
    aggregate_df = filtered_df[[sort_column, category_column]].groupby(
        category_column
        ).sum().sort_values(by=[sort_column], ascending=False)
    fig = plot_int_hist(
        filtered_df, 
        groupby=category_column,
        columns=[sort_column],
        classification=classification,
        agg=agg,
        label=label,
        y_order=True,
        title=f'{"".join([word.title()+" " for word in period.split("_")]).strip()+": " if period else None}{min_date} to {max_date}',
        height=height
    )
    return fig, aggregate_df

def create_bar_chart(
    df, values_column='Elapsed', agg_function='sum', groupby_column='Task Project name'
    ):
    """
    Show the aggregate value of a given column, grouped by a given `groupby_column`.
    """
    # Determine the most recent month based on `created_time` of the data
    recent_month = df['created_time'].max().month - 1
    print(recent_month)
    # Select only rows where `created_time` is within the recent_month
    df = df[df['created_time'].dt.month == recent_month]
    print(f'Filtered dataframe shape: {df.shape}')
    columns = df.columns.tolist()
    columns.remove('created_time')
    data = df[columns].groupby(groupby_column).agg(agg_function)
    data = data.sort_values(by=values_column, ascending=1)

    # Calculate the figure height based on the number of bars
    figure_height = len(data) * 30 + 300 # Adjust the multiplier as needed
    
    fig = go.Figure(go.Bar(
        x=data[values_column], y=data.index, orientation='h',
    ))

    fig.update_layout(
        yaxis=dict(tickmode='array', tickvals=list(range(len(data))), ticktext=data.index, tickfont=dict(size=12)),
        height=figure_height
    )
    fig.show()