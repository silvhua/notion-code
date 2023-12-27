import plotly.graph_objects as go

def create_bar_chart(
    df, values_column='Elapsed', agg_function='sum', groupby_column='Task Project name'
    ):
    """
    Show the aggregate value of a given column, grouped by a given `groupby_column`.
    """
    data = df.groupby(groupby_column).agg(agg_function)
    data = data.sort_values(by=values_column, ascending=1)
    
    # Calculate the figure height based on the number of bars
    figure_height = len(data) * 30  # Adjust the multiplier as needed
    
    fig = go.Figure(go.Bar(
        x=data[values_column], y=data.index, orientation='h',
    ))

    fig.update_layout(
        yaxis=dict(tickmode='array', tickvals=list(range(len(data))), ticktext=data.index, tickfont=dict(size=12)),
        height=figure_height
    )

    fig.show()