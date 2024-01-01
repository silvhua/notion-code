import plotly.graph_objects as go
from wrangling import *
from silvhua_plot import *

def classify_unbilled(df, column='Flag', flag_name='do not bill'):

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
    df, category_column='Category', classification='Unbilled', label=True,
    agg='sum', sort_column='Elapsed', date_column='created_time', height=None,
    period='past_month', start_date=None, end_date=None
    ):
    print(f'Total rows: {len(df)}')
    classified_df = classify_projects(df)
    filtered_df = filter_by_period(classified_df, column=date_column, period=period, start_date=start_date, end_date=end_date)
    print(f'Data based on {len(filtered_df)} rows')
    aggregate_df = filtered_df[[sort_column, category_column]].groupby(
        category_column
        ).sum().sort_values(by=[sort_column], ascending=False)
    plot_int_hist(
        filtered_df, 
        groupby=category_column,
        columns=[sort_column],
        classification=classification,
        agg=agg,
        label=label,
        y_order=True,
        height=height
    )
    return aggregate_df

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