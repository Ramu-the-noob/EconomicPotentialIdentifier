import pandas as pd
import plotly.express as px

df = pd.read_csv('top_50_aggregate_scores.csv')


df_long = df.melt(id_vars=['Country'], var_name='Year', value_name='Aggregate_Score')


df_long['Year'] = pd.to_numeric(df_long['Year'])


fig = px.line(
    df_long, 
    x='Year', 
    y='Aggregate_Score', 
    color='Country',
    title='Top 50 Economies: Aggregate Determinant Scores (1990-2022)',
    labels={'Aggregate_Score': 'Composite Score (0 to 1)', 'Year': 'Year'},
    markers=True
)


fig.update_layout(
    template='plotly_dark',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#444444'),
    hovermode='x unified', # Shows a clean vertical line with all data at that year
    legend_title_text='Countries'
)


default_visible = ['United States', 'China', 'Germany', 'India', 'Japan']

for trace in fig.data:
    if trace.name not in default_visible:
        trace.visible = 'legendonly'


output_file = 'aggregate_scores_visualization.html'
fig.write_html(output_file)
print(f"Visualization saved to {output_file}. Open it in your web browser!")
