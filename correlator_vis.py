import matplotlib.pyplot as plt
from dash import Dash, dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from read_modules import goes, cimel
import plotly.graph_objs as go
from plotly.subplots import make_subplots
#from read_modules_antiguo import *

types = ['Correlation', 'Time Series']

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
txt = dcc.Markdown(children='Holi, esta es la aplicacion inicial')

tab = pd.read_csv('data.csv')
varss = tab.variable.unique()
places = tab.place.unique()
origin = tab.origin.unique()


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
        html.H6("Variable1", className='display-7'),
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
        html.Br(),
        html.H6("Variable2", className='display-7'),
        dcc.Dropdown(
            id='drpdwn_orig2',
            options=[{'label': i, 'value': i} for i in origin],
            value = ""
            ),
        dcc.Dropdown(
            id='drpdwn_var2',
            options=[{'label': i, 'value': i} for i in varss],
            value = ""
            ),
        dcc.Dropdown(
            id='drpdwn_place2',
            options=[{'label': i, 'value': i} for i in places],
            value = ""
            ),
        html.Br(),
        html.H5("Opciones", className='display-7'),
        dcc.Dropdown(
            id = 'drpdwn_type',
            options=[{'label': i, 'value': i} for i in types],
            value = 0
        ),
        html.Button(className='dropdown-button',
                children=['Generar'],
                id = 'generar_boton'),
        html.P('hola', id='textoprueba'),
        html.P('hola', id='textoprueba2')
        ],
    style=SIDEBAR_STYLE,
)




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
        Output('drpdwn_place2', 'options'),
        Output('drpdwn_var2', 'options'),
        Input('drpdwn_orig2', 'value')  
)
def change_op2(var_picked2):
    tabb = tab.copy()
    tabb = tabb[tabb.origin == var_picked2]
    nw_place = [{'label': i, 'value': i} for i in tabb.place.unique()]
    nw_orig = [{'label': i, 'value': i} for i in tabb.variable.unique()]
    return nw_place, nw_orig

## GENERAL APP LAYOUT
app.layout = html.Div([
    sidebar,
    html.Div(id='plots-container', style=CONTENT_STYLE)
])




@callback(
    [Output('textoprueba', 'children'),
    Output('textoprueba2', 'children'),
    Output('plots-container', 'children')],
    [Input('generar_boton', 'n_clicks')],
    [State('drpdwn_place', 'value'),
    State('drpdwn_var', 'value'),
    State('drpdwn_orig', 'value'),
    State('drpdwn_place2', 'value'),
    State('drpdwn_var2', 'value'),
    State('drpdwn_orig2', 'value'),
    State('drpdwn_type','value')
    ]
)
def print_picked(n_clicks,place, var, orig, place2, var2, orig2,tipo):

    tabb = tab.copy()
    pii = tabb[(tabb.place == place) & (tabb.origin == orig) & (tabb.variable == var)]
    pii2 = tabb[(tabb.place == place2) & (tabb.origin == orig2) & (tabb.variable == var2)]
    if len(pii) == 0 or len(pii2) == 0 or orig == 'GOESVertProf' or orig2 == 'GOESVertProf':
        ret3 = 'The plot could not be created'
        ret2 = 'Sorry'
        ret1 = 'Sorry'
    else:
        ret1 = 'Data succesful'
        ret2 = 'Data succesful'
        var1 = pii.code.to_list()[0]
        var2 = pii2.code.to_list()[0]
        if orig == 'GOES':
            x = goes(place)
        elif orig == 'CIMEL':
            x = cimel(place)
        if orig2 == 'GOES':
            y = goes(place2)
        elif orig2 == 'CIMEL':
            y = cimel(place2)
        
        dat_x = getattr(x,var1)
        dat_y = getattr(y,var2)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if tipo == 'Correlation':
            
            fig.add_trace(go.Scatter(x=dat_x.data, y=dat_y.data,mode='markers'))
            fig.update_layout(
                xaxis_title=f"{var1} [{dat_x.units}]",
                yaxis_title=f"{var2} [{dat_y.units}]"
            )
            
        elif tipo == 'Time Series':
            fig.add_trace(go.Scatter(x=dat_x.times, y=dat_x.data,mode='lines+markers',name=dat_x.full_name, showlegend=True), secondary_y = False)
            fig.add_trace(go.Scatter(x=dat_y.times, y=dat_y.data, mode='lines+markers',name=dat_y.full_name, showlegend=True), secondary_y = True)
            fig.update_layout(
                xaxis_title='Local Time'
            )
            fig.update_yaxes(title_text=f"{var1} [{dat_x.units}]", secondary_y=False)
            fig.update_yaxes(title_text=f"{var2} [{dat_y.units}]", secondary_y=True)



        ret3 = dcc.Graph(id='myplot', figure=fig)



    return (ret1, ret2, ret3)




if __name__ == '__main__':
    app.run_server(port=8051)

