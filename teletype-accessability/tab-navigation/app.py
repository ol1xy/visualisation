from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()

app = Dash(__name__)
server = app.server 


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Клавиатурная навигация</title>
        {%favicon%}
        {%css%}
        <style>
            /* Стилизуем фокус для кнопок */
            button:focus {
                outline: 4px solid #FF5722 !important; /* Ярко-оранжевый */
                outline-offset: 2px;
                background-color: #FFF3E0;
            }
            
            /* Стилизуем фокус для ползунка Dash (RangeSlider) */
            .rc-slider-handle:focus {
                outline: 4px solid #FF5722 !important;
                border-color: #FF5722 !important;
                box-shadow: 0 0 0 5px rgba(255, 87, 34, 0.2) !important;
            }

            /* Стилизуем фокус для выпадающего списка Dash (Dropdown) */
            .dash-dropdown > div {
                transition: outline 0.1s ease-in-out;
            }
            .dash-dropdown:focus-within > div {
                outline: 4px solid #FF5722 !important;
                outline-offset: 2px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# 4. Построение интерфейса (Строгий DOM-порядок: Элементы управления -> График)
app.layout = html.Div([
    html.H2("Анализ населения", style={'fontFamily': 'sans-serif'}),
    
    # БЛОК 1: ЭЛЕМЕНТЫ УПРАВЛЕНИЯ (Получают фокус первыми)
    html.Div([
        html.Div([
            html.Label("1. Выберите континент", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': c, 'value': c} for c in df['continent'].unique()],
                value='Europe',
                clearable=False,
                className='dash-dropdown' # Привязка к нашему CSS
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("2. Выберите год:", style={'fontWeight': 'bold'}),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                step=5,
                value=2007,
                marks={str(year): str(year) for year in df['year'].unique()}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'border': '1px solid #ddd', 'marginBottom': '20px'}),
    
    # БЛОК 2: ГРАФИК (Результат действий)
    dcc.Graph(id='population-chart'),
    
    # БЛОК 3: КНОПКА (Получает фокус последней)
    html.Button("Скачать данные", id="btn-export", style={'padding': '15px', 'fontSize': '16px', 'cursor': 'pointer'})

], style={'maxWidth': '1000px', 'margin': '0 auto', 'padding': '20px', 'fontFamily': 'sans-serif'})


# 5. Логика обновления графика (Кросс-фильтр)
@app.callback(
    Output('population-chart', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_chart(selected_continent, selected_year):
    filtered_df = df[(df['continent'] == selected_continent) & (df['year'] == selected_year)]
    
    fig = px.bar(
        filtered_df.sort_values('pop', ascending=False).head(15), 
        x='country', y='pop',
        title=f"Топ-15 стран ({selected_continent}, {selected_year})",
        color_discrete_sequence=px.colors.qualitative.Safe # Используем безопасную палитру
    )
    return fig

# Запуск
if __name__ == '__main__':
    app.run(debug=True, port=8051)