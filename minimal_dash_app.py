from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    # Fixed: multi=True (no quotes)
    dcc.Dropdown(df.country.unique(), ['Canada'], id='dropdown-selection', multi=True),
    dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='axis-x'),
    dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='axis-y'),
    dcc.Dropdown(['lifeExp', 'pop', 'gdpPercap'], 'pop', id='axis-s'),

    
    dcc.Graph(id='graph-content'),
    dcc.Graph(id='scatter-content')

]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('axis-y', 'value')
)
def update_graph(value, y_column, countries):
    # Use .isin() because 'countries' is now a list
    dff = df[df.country.isin(countries)]
    
    # Use the y_column variable to make the chart dynamic
    return px.line(dff, x='year', y=y_column, color='country', 
                   title = f'Динамика изменения показателя {y_column} для стран {", ".join(value)}')

@callback(
    Output('scatter-content', 'figure'),
    Input('axis-x', 'value'),
    Input('axis-y', 'value'),
    Input('axis-s', 'value'),
    Input('graph-content', 'hoverData'),
    prevent_initial_call = True

)
def update_scatter(x_column, y_column, s_column, hover_data):
    
    if not hover_data:
        year = 2007
    else:
        year = hover_data['points'][0]['x']
    dff = df[df.year == year]
    # Use the y_column variable to make the chart dynamic
    return px.scatter(df, x=x_column, y=y_column, size=s_column, color='continent',
                      opacity = 0.5,
                      title = f"Зависимость показателей {x_column}  от {y_column} для стран за {year} год")

if __name__ == '__main__':
    app.run(debug=True)