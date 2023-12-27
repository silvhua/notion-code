import plotly.graph_objects as go

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