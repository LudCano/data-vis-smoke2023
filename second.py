import matplotlib.pyplot as plt
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from read_modules_antiguo import *
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
        dcc.Dropdown(
            id='drpdwn_orig',
            options=[{'label': i, 'value': i} for i in origin],
            value = ""
            ),
        dcc.Dropdown(
            id='drpdwn_var',
            options=[{'label': i, 'value': i} for i in varss],
            value = ""
            ),
        dcc.Dropdown(
            id='drpdwn_place',
            options=[{'label': i, 'value': i} for i in places],
            value = ""
            ),
        
        html.Button(className='dropdown-button',
                children=['Generar'],
                id = 'generar_boton'),
        html.P('hola', id='textoprueba')
        ],
    style=SIDEBAR_STYLE,
)



@callback(
    Output('plots-container', 'children'),
    Input('drpdwn_filas', 'value'),
     Input('drpdwn_cols', 'value')
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
    

@callback(
        Output('drpdwn_place', 'options'),
        Output('drpdwn_var', 'options'),
        Input('drpdwn_orig', 'value')  
)
def change_op2(var_picked2):
    tabb = tab.copy()
    tabb = tabb[tabb.origin == var_picked2]
    nw_place = [{'label': i, 'value': i} for i in tabb.place.unique()]
    nw_orig = [{'label': i, 'value': i} for i in tabb.variable.unique()]
    return nw_place, nw_orig


@callback(
    Output('textoprueba', 'children'),
    Input('drpdwn_place', 'value'),
    Input('drpdwn_var', 'value'),
    Input('drpdwn_orig', 'value'),
    Input('generar_boton', 'n_clicks')
)
def print_picked(place, var, orig, n_clicks):
    if n_clicks>0:
        tabb = tab.copy()
        pii = tabb[(tabb.place == place) & (tabb.origin == orig) & (tabb.variable == var)]
        print(pii.path)

        

        return str(pii.path[0])


app.layout = html.Div([
    sidebar,
    html.Div(id='plots-container', style=CONTENT_STYLE)
])

if __name__ == '__main__':
    app.run_server(port=8051)

