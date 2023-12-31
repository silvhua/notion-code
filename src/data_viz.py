import plotly.graph_objects as go
from wrangling import *
from silvhua_plot import *

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
        if 'ginkgo' in row[column].lower():
            row['Category'] = 'Ginkgo'
        elif tag_set.intersection({'portfolio', 'tech ed'}):
            row['Category'] = 'tech career development'
            row['Unbilled'] = True
        elif row[column].lower() in ['ghl chatbot', 'tech business']:
            row['Category'] = 'tech business'
            if row[column].lower() == 'tech business':
                row['Unbilled'] = True
        elif 'defy time fitness' in [tag.lower() for tag in row[tag_column]]:
            row['Category'] = 'personal training work'
            if 'defy time fitness' not in row[column].lower():
                row['Unbilled'] = True
        elif row[column].lower() == 'career positioning':
            row['Category'] = 'career positioning'
            row['Unbilled'] = True
        else:
            row['Category'] = 'Other'
            row['Unbilled'] = True

        return row
    
    classified_df = df.apply(lambda x: classify(x), axis=1)
    unique_categories = classified_df['Category'].unique()
    print(f'There are {len(unique_categories)} categories: {[category for category in unique_categories]}')
    return classified_df

def plot_aggregate(df, columns=None, classification=None, label=1, barmode='stack', n_columns=1, height=150, y_order=None):
    """
    Use Plotly to plot multiple histograms using the specified columns of a dataframe.
    Arguments:
    - df: Dataframe.
    - columns (optional): Columns of dataframe on which to create the histogram. If blank, all numeric data will be plotted.
    - classification (optional): Provide name of colum containing binary classification values 0 and 1. 
        Data points classified as 1 will be in red.
    - label (optional): Label of classification column. Default is 1.
    - barmode ('stack', 'group', or 'overlay'; optional): How the different will be shown. Default is 'stack'.
    - n_columns (optional): Number of columns in the figure. Default is 2.
    - height (optional): Height of each subplot in pixels. Default is 150.
    - y_order (optional): List of values to specify the order of the y axis. Default is None.

    """
    if columns == None:
        columns = df.dtypes[df.dtypes != 'object'].index.tolist()
    n_rows = (len(columns)-1) // n_columns + 1
    fig = make_subplots(rows=n_rows, cols=n_columns, subplot_titles=columns)
    for i, feature in enumerate(columns):
        if classification:
            zero = df.sort_values(feature)[df.sort_values(feature)[classification] != label]
            one = df.sort_values(feature)[df.sort_values(feature)[classification] == label]
            fig.add_trace(go.Histogram(y=zero[feature],
                marker_color='blue',
                orientation='h',
                opacity=0.5), 
                row=i//n_columns+1, col=i % n_columns + 1
                )
            fig.add_trace(go.Histogram(y=one[feature],
                marker_color='red',
                orientation='h',
                opacity=0.5),
                row=i//n_columns+1, col=i % n_columns + 1)
        else:
            fig.add_trace(go.Bar(x=df[feature]), 
            row=i//n_columns+1, col=i % n_columns + 1)
    
    if classification:
        title = f'Observations with {classification} of value {label} are indicated in red'
    else:
        title = 'Value counts'
    fig.update_layout(
        showlegend=False,
        height=(n_rows+1)*height,
        barmode=barmode,
        # bargap=0.1,
        title=title,
        title_x=0.5,
        title_xanchor='center',
        # title_y=0.1,
        title_yanchor='top'
    )
    fig.update_xaxes(title=dict(
        standoff=0,
        ),
        title_text='number of observations',
        row=n_rows
    )
    # if y_order:
    #     fig.update_yaxes(categoryorder='array', categoryarray=y_order)
    fig.show()


def plot_by_category(df, category_column='Category', sort_column='Elapsed'):
    classified_df = classify_projects(df)
    aggregate_df = classified_df[[sort_column, category_column]].groupby(
        category_column
        ).sum().sort_values(by=[sort_column], ascending=True)
    index_list = aggregate_df.index.tolist()
    print(index_list)

    plot_aggregate(
        classified_df, columns=[category_column],
        # classification='Unbilled',
        label=True,
        y_order=index_list
    )
    return aggregate_df