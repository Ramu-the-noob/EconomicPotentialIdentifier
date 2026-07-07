import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

def generate_extrapolated_1980_dashboard():
    core_files = ["gdp growth.csv", "debt.csv", "inequality.csv", "HDI.csv"]

    all_dfs = {}
    countries_set = set()

    for f in core_files:
        if os.path.exists(f):
            df = pd.read_csv(f)
            year_col = [c for c in df.columns if 'year' in c.lower()][0]
            df = df.rename(columns={year_col: 'Year'})

            df_long = pd.melt(df, id_vars=['Year'], var_name='Country', value_name=f)
            df_long['Country'] = df_long['Country'].str.strip()
            countries_set.update(df_long['Country'].unique())
            all_dfs[f] = df_long

    if not all_dfs:
        print("Error: Could not locate core CSV files.")
        return

    years = list(range(1980, 2025))
    grid = pd.MultiIndex.from_product([years, sorted(list(countries_set))], names=['Year', 'Country'])
    df_grid = pd.DataFrame(index=grid).reset_index()

    for f, d in all_dfs.items():
        df_grid = pd.merge(df_grid, d, on=['Year', 'Country'], how='left')

    metric_cols = list(all_dfs.keys())
    for col in metric_cols:
        df_grid[col] = df_grid.groupby('Country')[col].transform(lambda x: x.bfill().ffill())

    df_grid['Score'] = df_grid[metric_cols].mean(axis=1)

    df_avg = df_grid.sort_values(by=['Country', 'Year']).reset_index(drop=True)

    df_avg['3_Year_Smooth'] = df_avg.groupby('Country')['Score'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )

    countries = sorted(df_avg['Country'].unique())
    color_palette = px.colors.qualitative.Safe
    num_countries = len(countries)

    fig = go.Figure()

    for i, country in enumerate(countries):
        c_df = df_avg[df_avg['Country'] == country]
        fig.add_trace(go.Scatter(x=c_df['Year'], y=c_df['Score'], name=country, mode='lines', line=dict(color=color_palette[i % len(color_palette)], width=2), visible=True))
        fig.add_trace(go.Scatter(x=c_df['Year'], y=c_df['3_Year_Smooth'], name=country, mode='lines', line=dict(color=color_palette[i % len(color_palette)], width=2.5), visible=False))

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons", direction="right", active=0, x=0.5, y=1.12, xanchor="center", yanchor="top",
                buttons=list([
                    dict(label="Raw Annual Volatility", method="update", args=[{"visible": [True, False]*num_countries}, {"yaxis": {"title": "Growth Potential Index (Raw Values)"}}]),
                    dict(label="3-Year Moving Average", method="update", args=[{"visible": [False, True]*num_countries}, {"yaxis": {"title": "Growth Potential Index (3-Year Moving Average)"}}])
                ]),
            )
        ],
        template='plotly_dark', hovermode='x unified', xaxis_title='Year', yaxis_title='Growth Potential Index (Raw Values)',
        title=dict(text='Extrapolated HDI Included: Long-Term Macro Cycles (1980-2024)', x=0.05, y=0.95),
        font=dict(family="sans-serif", size=13)
    )

    output = 'extrapolated_1980_dashboard.html'
    fig.write_html(output)
    print(f"Success! Dashboard saved as '{output}'.")

if __name__ == "__main__":
    generate_extrapolated_1980_dashboard()
