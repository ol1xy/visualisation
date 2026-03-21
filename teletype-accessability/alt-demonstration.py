from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px

# 1. Подготовка данных и безопасного графика (используем датасет iris для наглядности)
df = px.data.iris()
fig_good = px.scatter(
    df, x="sepal_width", y="sepal_length", color="species",
    color_discrete_sequence=px.colors.qualitative.Safe,
    symbol="species",
    title="Инклюзивный дизайн: Safe-палитра + Кодирование формой"
)
fig_good.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))

# 2. Инициализация приложения Dash
app = Dash(__name__)

# 3. Ваша структура интерфейса (Layout)
app.layout = html.Div([
    html.H2("Анализ данных: Альтернативные форматы (a11y)"),
    
    # График для визуального анализа
    dcc.Graph(id='main-scatter-plot', figure=fig_good),
    
    html.Br(), # Отступ для красоты
    
    # Скрытая таблица для скринридеров и детального изучения
    html.Details([
        html.Summary("Показать данные в виде таблицы (Альтернативный формат)", style={'fontSize': '16px', 'cursor': 'pointer', 'fontWeight': 'bold'}),
        html.Br(),
        dash_table.DataTable(
            id='raw-data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'} 
        )
    ]),
    
    html.Br(),
    html.Br(),
    
    # Кнопка скачивания и невидимый компонент загрузки
    html.Button("Скачать данные (CSV)", id="btn-download-csv", style={'padding': '10px', 'fontSize': '14px', 'cursor': 'pointer'}),
    dcc.Download(id="download-dataframe-csv")
    
], style={'maxWidth': '900px', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif'}) # Центрируем интерфейс


# 4. Логика работы кнопки скачивания (Callback)
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_data_as_csv(n_clicks):
    # Эта функция конвертирует DataFrame в CSV и отправляет пользователю при клике
    return dcc.send_data_frame(df.to_csv, "accessible_dataset.csv", index=False)

# 5. Запуск сервера
if __name__ == '__main__':
    # Если запускаете в Google Colab, интерфейс может открыться прямо под ячейкой 
    # или выдаст синюю ссылку вида http://127.0.0.1:8050/ (перейдите по ней)
    app.run(debug=True)