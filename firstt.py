
from dash import Dash, dcc
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
txt = dcc.Markdown(children='Holi, esta es la aplicacion inicial')

app.layout = dbc.Container([txt])

if __name__ == '__main__':
    app.run_server(port=8051)

