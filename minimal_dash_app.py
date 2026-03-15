from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = html.Div([
    html.H1(children='', style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.Label('Country (linear-plot):'),
            dcc.Dropdown(df.country.unique(), ['Canada', 'Brazil'], id='dropdown-selection', multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label('Y-axis (linear-plot):'),
            dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='line-y')
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('X-axis (bubble-plot):'),
            dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'gdpPercap', id='axis-x')
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('Y-axis (bubble-plot):'),
            dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'lifeExp', id='axis-y')
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('Size (bubble-plot):'),
            dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='axis-s')
        ], style={'width': '15%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '10px', 'marginBottom': '20px'}),

    html.Div([
        html.Div([dcc.Graph(id='graph-content')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='scatter-content')], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([dcc.Graph(id='bar-chart')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='pie-chart')], style={'width': '50%', 'display': 'inline-block'}),
    ])
])

@callback(
        Output('pie-chart', 'figure'),
        Input('graph-content', 'hoverData')
)

def update_pie(hover_data):
    if not hover_data:
        year = 2007
    else:
        year = hover_data['points'][0]['x']

    dff = df[df.year == year]
    
    return px.pie(dff, values = 'pop', names = 'continent',
                      title = f'Населеление по континентам в {year} году')

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('line-y', 'value')
)

def update_graph(value, y_column):
    # Use .isin() because 'countries' is now a list
    if not value:
        return px.line(title='Выберите хотя бы одну страну')
    dff = df[df.country.isin(value)]
    
    # Use the y_column variable to make the chart dynamic
    return px.line(dff, x='year', y=y_column, color='country', 
                   title = f'Динамика изменения показателя {y_column} для стран {", ".join(value)}')

@callback(
    Output('scatter-content', 'figure'),
    Input('axis-x', 'value'),
    Input('axis-y', 'value'),
    Input('axis-s', 'value'),
    Input('graph-content', 'hoverData'),
    # prevent_initial_call = True
)

def update_scatter(x_column, y_column, s_column, hover_data):
    
    if not hover_data:
        year = 2007
    else:
        year = hover_data['points'][0]['x']
    dff = df[df.year == year]
    # Use the y_column variable to make the chart dynamic
    return px.scatter(dff, x=x_column, y=y_column, size=s_column, color='continent',
                      hover_name='country',
                      opacity = 0.7,
                      title = f"Зависимость показателей {x_column}  от {y_column} для стран за {year} год")

@callback(
    Output('bar-chart', "figure"),
    Input('graph-content', 'hoverData')
)

def update_bar(hover_data):
    if not hover_data:
        year = 2007
    else:
        year = hover_data['points'][0]['x']
    
    dff = df[df.year == year]
    dff_top15 = dff.sort_values(by='pop', ascending=False).head(15)

    return px.bar(dff_top15, x = 'country', y = 'pop',
                  title=f'Топ-15 стран по населению в {year} году')

if __name__ == '__main__':
    app.run(debug=True)