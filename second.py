
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
txt = dcc.Markdown(children='Holi, esta es la aplicacion inicial')

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H6("Opciones", className='display-7'),
        dbc.Row([
            dbc.Col([
            html.P("Filas"),
                dcc.Dropdown(
                id='drpdwn_filas',
                options=[{'label': str(i), 'value': i} for i in range(1,5)],
                value=1
            )]),
            dbc.Col([
                html.P("Columnas"),
                dcc.Dropdown(
                id='drpdwn_cols',
                options=[{'label': str(i), 'value': i} for i in range(1,5)],
                value=1
            )])
        ]),
        html.Button(className='dropdown-button',
                children=['Generar'],
                id = 'generar_boton')
        ],
    style=SIDEBAR_STYLE,
)


@app.callback(
    Output('plots-container', 'children'),
    [Input('drpdwn_filas', 'value'),
     Input('drpdwn_cols', 'value')]
)
def generar_matriz(nrows, ncols):
    print(f"Se escogieron {nrows} x {ncols}")
    ch = []
    for j in range(nrows):
        rw = []
        for k in range(ncols):
            rw.append(dbc.Col(html.P("Hola")))
        ch.append(dbc.Row(rw))
    return ch
    

app.layout = html.Div([
    sidebar,
    html.Div(id='plots-container', style=CONTENT_STYLE)
])

if __name__ == '__main__':
    app.run_server(port=8051)

