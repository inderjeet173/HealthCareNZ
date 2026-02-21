import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px

# Load CSV
df = pd.read_csv("NZ_Health_Dataset.csv")

# Age groups
bins = [0, 18, 35, 50, 100]
labels = ['0-18', '19-35', '36-50', '51+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# Initialize Dash app
app = Dash(__name__)
app.title = "NZ Health Dashboard"

# Layout with dropdown filters and grid style
app.layout = html.Div([
    html.H1("New Zealand Health Dashboard", style={'textAlign': 'center', 'color':'#1f77b4'}),
    
    html.Div([
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                value=2025
            ),
        ], style={'width':'30%', 'display':'inline-block', 'padding':'10px'}),
        
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                value=None,
                multi=True,
                placeholder="All regions"
            ),
        ], style={'width':'30%', 'display':'inline-block', 'padding':'10px'}),
        
        html.Div([
            html.Label("Select Disease:"),
            dcc.Dropdown(
                id='disease-filter',
                options=[{'label': d, 'value': d} for d in sorted(df['Disease'].unique())],
                value=None,
                multi=True,
                placeholder="All diseases"
            ),
        ], style={'width':'30%', 'display':'inline-block', 'padding':'10px'}),
    ], style={'textAlign':'center'}),
    
    html.Div([
        html.Div([dcc.Graph(id='bar-disease')], style={'width':'48%', 'display':'inline-block'}),
        html.Div([dcc.Graph(id='bar-region')], style={'width':'48%', 'display':'inline-block'}),
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='bar-age')], style={'width':'48%', 'display':'inline-block'}),
        html.Div([dcc.Graph(id='pie-gender')], style={'width':'48%', 'display':'inline-block'}),
    ])
])

# Callback to update charts
@callback(
    [Output('bar-disease', 'figure'),
     Output('bar-region', 'figure'),
     Output('bar-age', 'figure'),
     Output('pie-gender', 'figure')],
    [Input('year-filter', 'value'),
     Input('region-filter', 'value'),
     Input('disease-filter', 'value')]
)
def update_charts(selected_year, selected_regions, selected_diseases):
    filtered = df[df['Year'] == selected_year]
    
    if selected_regions:
        filtered = filtered[filtered['Region'].isin(selected_regions)]
    if selected_diseases:
        filtered = filtered[filtered['Disease'].isin(selected_diseases)]
    
    # Cases by Disease with hover info
    fig_disease = px.bar(
        filtered, x='Disease', color='Disease', title='Cases by Disease',
        hover_data={'Cases': True, 'Age_Group': False, 'Region': False},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Cases by Region
    region_counts = filtered.groupby('Region', as_index=False)['Cases'].sum()
    fig_region = px.bar(
        region_counts, x='Region', y='Cases', title='Cases by Region',
        text='Cases', color='Cases', color_continuous_scale='Oranges'
    )
    
    # Cases by Age Group
    age_counts = filtered.groupby('Age_Group', as_index=False)['Cases'].sum()
    fig_age = px.bar(
        age_counts, x='Age_Group', y='Cases', title='Cases by Age Group',
        text='Cases', color='Cases', color_continuous_scale='Blues'
    )
    
    # Gender distribution
    fig_gender = px.pie(
        filtered, names='Gender', title='Gender Distribution',
        color_discrete_map={'Male':'#636EFA','Female':'#EF553B'},
        hole=0.3
    )
    
    fig_disease.update_traces(hovertemplate='%{x}: %{y} cases')
    fig_region.update_traces(hovertemplate='%{x}: %{y} cases')
    fig_age.update_traces(hovertemplate='%{x}: %{y} cases')
    
    return fig_disease, fig_region, fig_age, fig_gender

if __name__ == '__main__':
    print("Starting NZ Health Dashboard...")
    print("Open your browser and go to http://localhost:8050")
    app.run(debug=True, port=8050)
