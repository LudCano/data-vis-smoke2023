import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Read the CSV data
df = pd.read_csv("data.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Data Selection Dashboard"),
    html.Div([
        html.Label("Origin:"),
        dcc.Dropdown(
            id='origin-dropdown',
            options=[{'label': i, 'value': i} for i in df['origin'].unique()],
            value=df['origin'].unique()[0]
        ),
    ]),
    html.Div([
        html.Label("Place:"),
        dcc.Dropdown(id='place-dropdown'),
    ]),
    html.Div([
        html.Label("Variable:"),
        dcc.Dropdown(id='variable-dropdown'),
    ]),
    html.Div(id='output-data')
])

# Define callback to update 'place-dropdown' options based on selected origin
@app.callback(
    Output('place-dropdown', 'options'),
    Input('origin-dropdown', 'value')
)
def update_place_options(selected_origin):
    filtered_df = df[df['origin'] == selected_origin]
    return [{'label': i, 'value': i} for i in filtered_df['place'].unique()]

# Define callback to update 'variable-dropdown' options based on selected place
@app.callback(
    Output('variable-dropdown', 'options'),
    Input('place-dropdown', 'value')
)
def update_variable_options(selected_place):
    filtered_df = df[df['place'] == selected_place]
    return [{'label': i, 'value': i} for i in filtered_df['variable'].unique()]

# Define callback to display selected data
@app.callback(
    Output('output-data', 'children'),
    Input('origin-dropdown', 'value'),
    Input('place-dropdown', 'value'),
    Input('variable-dropdown', 'value')
)
def display_selected_data(selected_origin, selected_place, selected_variable):
    filtered_df = df[(df['origin'] == selected_origin) & (df['place'] == selected_place) & (df['variable'] == selected_variable)]
    if filtered_df.empty:
        return "No data available."
    else:
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in filtered_df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns
                ]) for i in range(len(filtered_df))
            ])
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
