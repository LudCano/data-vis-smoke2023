        dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': '3x3 Grid', 'value': '3x3'},
            {'label': '2x2 Grid', 'value': '2x2'}
        ],
        value='3x3'
    )



app.layout = html.Div([
    sidebar,
    html.Div(id='plots-container'),
    html.Button(className='dropdwn_button',
                children=['Generar'],
                id = 'generar_boton'),
])

@app.callback(
        [Output('drpdwn_var', 'options'),
         Output('drpdwn_place', 'options'),
         Output('drpdwn_orig', 'options')],
        [Input('drpdwn_var', 'value'),
         Input('drpdwn_place', 'value'),
         Input('drpdwn_orig', 'value')]  
)
def change_options(var_picked, place_picked, orig_picked):
    tabb = tab.copy()
    



@app.callback(
        [Output('drpdwn_place', 'options'),
         Output('drpdwn_orig', 'options')],
        [Input('drpdwn_var', 'value')]  
)
def change_op1(var_picked):
    tabb = tab.copy()
    tabb = tabb[tabb.variable == var_picked]
    nw_place = tabb.place.unique()
    nw_orig = tabb.origin.unique()
    return nw_place, nw_orig



###

@app.callback(
        Output('drpdwn_place', 'options'),
         Output('drpdwn_orig', 'options'),
        Input('drpdwn_var', 'value') 
)
def change_op1(var_picked):
    tabb = tab.copy()
    tabb = tabb[tabb.variable == var_picked]
    nw_place = tabb.place.unique()
    nw_orig = tabb.origin.unique()
    return nw_place, nw_orig



@app.callback(
        Output('drpdwn_place', 'options'),
         Output('drpdwn_var', 'options'),
        Input('drpdwn_orig', 'value')  
)
def change_op2(var_picked):
    tabb = tab.copy()
    tabb = tabb[tabb.origin == var_picked]
    nw_place = tabb.place.unique()
    nw_orig = tabb.variable.unique()
    return nw_place, nw_orig

###

@callback(
        Output('drpdwn_place', 'options'),
        Output('drpdwn_orig', 'options'),
        Input('drpdwn_var', 'value')  
)
def change_op2(var_picked2):
    tabb = tab.copy()
    tabb = tabb[tabb.variable == var_picked2]
    nw_place = [{'label': i, 'value': i} for i in tabb.place.unique()]
    nw_orig = [{'label': i, 'value': i} for i in tabb.orig.unique()]
    return nw_place, nw_orig

