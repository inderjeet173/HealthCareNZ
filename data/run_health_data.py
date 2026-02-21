# Import libraries
import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px

# Load CSV
df = pd.read_csv("NZ_Health_Dataset.csv")

# Age groups
bins = [0, 18, 35, 50, 100]
labels = ['0-18', '19-35', '36-50', '51+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

app = Dash(__name__)
app.title = "NZ Health Dashboard"

app.layout = html.Div([

    html.H1("New Zealand Health Dashboard",
            style={'textAlign': 'center', 'color': '#1f77b4'}),

    # ---------------- KPI SECTION ----------------
    html.Div([
        html.Div(id="total-cases", className="kpi-box"),
        html.Div(id="top-disease", className="kpi-box"),
        html.Div(id="top-region", className="kpi-box"),
        html.Div(id="avg-age", className="kpi-box"),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),

    # ---------------- FILTER SECTION ----------------
    html.Div([
        html.Div([
            html.Label("Select Year"),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                value=2025
            )
        ], style={'width': '30%'}),

        html.Div([
            html.Label("Select Region"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                multi=True
            )
        ], style={'width': '30%'}),

        html.Div([
            html.Label("Select Disease"),
            dcc.Dropdown(
                id='disease-filter',
                options=[{'label': d, 'value': d} for d in sorted(df['Disease'].unique())],
                multi=True
            )
        ], style={'width': '30%'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # ---------------- CHART SECTION ----------------
    html.Div([
        html.Div([dcc.Graph(id='bar-disease')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-region')], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div([dcc.Graph(id='bar-age')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='pie-gender')], style={'width': '48%', 'display': 'inline-block'}),
    ])

])

# ---------------- CALLBACK ----------------
@callback(
    [Output('bar-disease', 'figure'),
     Output('bar-region', 'figure'),
     Output('bar-age', 'figure'),
     Output('pie-gender', 'figure'),
     Output('total-cases', 'children'),
     Output('top-disease', 'children'),
     Output('top-region', 'children'),
     Output('avg-age', 'children')],
    [Input('year-filter', 'value'),
     Input('region-filter', 'value'),
     Input('disease-filter', 'value')]
)
def update_dashboard(selected_year, selected_regions, selected_diseases):

    filtered = df[df['Year'] == selected_year]

    if selected_regions:
        filtered = filtered[filtered['Region'].isin(selected_regions)]
    if selected_diseases:
        filtered = filtered[filtered['Disease'].isin(selected_diseases)]

    # -------- KPIs --------
    total_cases = filtered['Cases'].sum()

    if not filtered.empty:
        top_disease = filtered['Disease'].value_counts().idxmax()
        top_region = filtered['Region'].value_counts().idxmax()
        avg_age = round(filtered['Age'].mean(), 1)
    else:
        top_disease = "N/A"
        top_region = "N/A"
        avg_age = "N/A"

    kpi_total = html.H3(f"Total Cases: {total_cases}")
    kpi_disease = html.H3(f"Top Disease: {top_disease}")
    kpi_region = html.H3(f"Top Region: {top_region}")
    kpi_age = html.H3(f"Avg Age: {avg_age}")

    # -------- Charts --------
    fig_disease = px.bar(filtered, x='Disease', color='Disease',
                         title='Cases by Disease')

    region_counts = filtered.groupby('Region', as_index=False)['Cases'].sum()
    fig_region = px.bar(region_counts, x='Region', y='Cases',
                        title='Cases by Region', text='Cases')

    age_counts = filtered.groupby('Age_Group', as_index=False)['Cases'].sum()
    fig_age = px.bar(age_counts, x='Age_Group', y='Cases',
                     title='Cases by Age Group', text='Cases')

    fig_gender = px.pie(filtered, names='Gender',
                        title='Gender Distribution', hole=0.4)

    return (fig_disease, fig_region, fig_age, fig_gender,
            kpi_total, kpi_disease, kpi_region, kpi_age)

if __name__ == '__main__':
    print("Starting NZ Health Dashboard...")
    print("Open your browser and go to http://localhost:8050")
    app.run(debug=True, port=8050)