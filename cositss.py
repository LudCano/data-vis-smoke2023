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