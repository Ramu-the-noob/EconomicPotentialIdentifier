# Economic Potential Identifier

A small data project that scores and visualizes countries' long-term economic growth potential, using the four determinants of a rising/declining great power outlined in Ray Dalio's *The Changing World Order*: **GDP growth**, **debt**, **inequality**, and **education / human development**.

Raw indicator data is cleaned and normalized into 0-1 scores per country per year, then combined into a composite "growth potential" score and rendered as interactive Plotly dashboards.

## What it does

- Pulls raw macro data (GDP growth, government/private debt, wealth inequality, HDI) for a wide set of countries across several decades.
- Normalizes each indicator into a comparable **0-1 score**, so countries and metrics can be plotted on the same scale.
- Averages the four scores into a single **aggregate / composite score** per country, per year, as a rough proxy for "growth potential."
- Generates two self-contained HTML dashboards you can open in any browser -- no server required.

## Repository structure

```
EconomicPotentialIdentifier/
├── RawData/                     # Unprocessed source data, as downloaded
│   ├── GDPGrowth/                 - GDP growth (World Bank, World Development Indicators)
│   ├── Debt/                      - Government & private debt (World Bank, WDI/IMF)
│   ├── HDI/                       - Human Development Index (UNDP)
│   └── Inequality/                - Wealth inequality (World Inequality Database, wid.world)
│
└── FinalProject/
    ├── AllWorld/                  # Top 50 economies, one metric at a time
    │   ├── top_50_*_scores.csv          - normalized per-indicator scores
    │   ├── top_50_aggregate_scores.csv  - combined composite score
    │   ├── Main.py                      - builds the aggregate score line chart
    │   └── aggregate_scores_visualization.html  (generated output)
    │
    └── MajorPower/                # A focused set of major economies
        ├── gdp growth.csv, debt.csv, inequality.csv, HDI.csv
        ├── Main.py                      - merges all 4 indicators, builds long-run dashboard
        └── extrapolated_1980_dashboard.html  (generated output)
```

## The two dashboards

**1. Top 50 Economies -- Aggregate Score (`FinalProject/AllWorld`)**
A multi-line chart (1961-2024) of the composite growth-potential score for the world's 50 largest economies. All countries are plotted, but only a handful (US, China, Germany, India, Japan) are visible by default -- click any entry in the legend to toggle others on or off.

**2. Major Powers -- Long-Term Macro Cycles (`FinalProject/MajorPower`)**
A dashboard covering 11 major economies (US, China, UK, Germany, France, Japan, India, Russia, Brazil, Netherlands, Saudi Arabia) from 1980-2024, merging all four indicators into one score per country per year. Missing years are back/forward-filled per country. Includes a toggle button to switch between raw annual values and a 3-year moving average, which smooths out short-term volatility to make long-run cycles easier to see.

## Getting started

**Requirements:** Python 3, `pandas`, `plotly`

```bash
pip install pandas plotly
```

**Run a dashboard:**

```bash
cd FinalProject/AllWorld
python Main.py
# -> writes aggregate_scores_visualization.html, open it in your browser
```

```bash
cd FinalProject/MajorPower
python Main.py
# -> writes extrapolated_1980_dashboard.html, open it in your browser
```

Each script reads the CSVs sitting alongside it in the same folder, so run it from within that folder (as shown above).

## Data sources

- **GDP growth** -- World Bank, World Development Indicators
- **Government & private debt** -- World Bank / IMF debt datasets
- **Inequality** -- World Inequality Database ([wid.world](https://wid.world))
- **Human Development Index (HDI)** -- UNDP Human Development Reports

## Notes & limitations

- Scores are a simplified, unweighted average of the four normalized indicators -- a rough directional signal, not a rigorous economic model.
- Coverage varies by country and year; some series are shorter or sparser than others, and gaps are filled using back/forward-fill within each country.
- This is a personal/learning project inspired by the "Big Cycle" framework in *The Changing World Order* -- it is not investment advice.
