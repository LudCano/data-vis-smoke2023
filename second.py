
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc


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


sidebar = html.Div(
    [
        #html.H6("Opciones", className='display-7'),
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
        ])
        ],
    style=SIDEBAR_STYLE,
)

#app.layout = dbc.Container([txt])
app.layout = html.Div([
    sidebar,
    html.Div(id='plots-container')
])

if __name__ == '__main__':
    app.run_server(port=8051)

