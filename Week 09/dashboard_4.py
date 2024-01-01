# STEP 1: import libraries
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
import joblib
import dash_auth


# STEP 2: create a Dash app
app = Dash(__name__)

# add authentication
USERNAME_PASSWORD_PAIRS = {
    'user1': '1234',
    'user2': '5678',
}
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


# STEP 3: load & process data
data = pd.read_csv("CO2_Emissions_Canada.csv")

# load trained model
model = joblib.load('tree.joblib')

# create a list of numerical features
features_num = data.select_dtypes(include=['int64', 'float64']).columns

# create a list of categorical features
features_cat = data.select_dtypes(include=['object']).columns

# create a list of fuel types
fuel_types = [
    {'label': 'Diesel', 'value': 'D'}, 
    {'label': 'Ethanol', 'value': 'E'}, 
    {'label': 'Gasoline', 'value': 'X'}, 
    {'label': 'Premium Gasoline', 'value': 'Z'}
]


# STEP 4: create a Dash layout that contains a Dropdown component
html_title = html.H1("CO2 Emissions in Canada", style={
    'text-align': 'center',
    'margin': '10px',
    'padding': '20px',
    'background-color': 'white',
    'box-shadow': '0px 0px 5px 5px lightgrey',
    'border-radius': '10px',
})

html_card_num = html.Div([
    html.H3("Numerical Features"),
    dcc.Dropdown(
        id='feature-num',
        options=[{'label': i, 'value': i} for i in features_num],
        value='Engine Size [L]'
    ),
    dcc.Graph(id='plot-num')
], style={
    'background-color': 'white', 
    'padding': '10px', 
    'box-shadow': '0px 0px 5px 5px lightgrey',
    'border-radius': '10px',
    'flex-basis': '50%',
})

html_card_cat = html.Div([
    html.H3("Categorical Features"),
    dcc.Dropdown(
        id='feature-cat',
        options=[{'label': i, 'value': i} for i in features_cat],
        value='Fuel Type'
    ),
    dcc.Graph(id='plot-cat')
], style={
    'background-color': 'white', 
    'padding': '10px', 
    'box-shadow': '0px 0px 5px 5px lightgrey',
    'border-radius': '10px',
    'flex-basis': '50%',
})

html_input_form = html.Div([
    html.H3("Predict CO2 Emissions"),
    html.Div([
        html.H5("Fuel Type"),
        dcc.Dropdown(
            id='fuel-type',
            options=fuel_types,
            value='Z'
        )
    ]),
    html.Div([
        html.H5("Engine Size [L]"),
        dcc.Input(id='engine-size', value=2.0, type='number', style={
            'width': 'calc(100% - 20px)',
            'padding': '10px',
            'border': '1px solid #cccccc',
            'outline': 'none',
            'border-radius': '4px',
        })
    ]),
    html.Div([
        html.H5("Fuel Consumption Comb [L/100 km]"),
        dcc.Input(id='fuel-consumption-comb', value=10, type='number', style={
            'width': 'calc(100% - 20px)',
            'padding': '10px',
            'border': '1px solid #cccccc',
            'outline': 'none',
            'border-radius': '4px',
        })
    ]),
], style={
    'padding': '10px',
    'margin-top': '20px',
    'flex-basis': '50%',
})

html_prediction = html.Div([
    html.Div([
        html.P("Prediction", style={'font-size': '20px'}),
        html.P(id='prediction', style={
            'font-size': '50px',
            'font-weight': 'bold',
            'text-align': 'center',
            'width': '100%',
            'color': '#636efa',
        })
    ], style={
        'padding': '20px',
        'font-size': '30px',
        'background-color': '#e5ecf6',
        'border-radius': '5px',
    })
], style={
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'padding': '10px',
    'margin-top': '20px',
    'flex-basis': '50%',
})


# add components to the app layout
app.layout = html.Div([
    # title
    html_title,

    # graphs container
    html.Div([
        # numerical features CARD
        html_card_num,

        # categorical features CARD
        html_card_cat,
    ], style={
        'padding': '10px',
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'stretch',
        'gap': '20px',
    }),

    # prediction container
    html.Div([
        # input form
        html_input_form,

        # prediction
        html_prediction,
    ], style={
        'margin': '10px',
        'padding': '10px',
        'border-radius': '10px',
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'stretch',
        'box-shadow': '0px 0px 5px 5px lightgrey',
        'gap': '20px',
    }),
])


# STEP 5: add callbacks for interactive components
@app.callback(
    Output(component_id='plot-num', component_property='figure'),
    [Input(component_id='feature-num', component_property='value')]
)
def update_graph_num(selected_feature):
    fig = px.scatter(data, x=selected_feature, y='CO2 Emissions [g/km]')
    return fig



# add a callback to update the CAT graph
@app.callback(
    Output(component_id='plot-cat', component_property='figure'),
    [Input(component_id='feature-cat', component_property='value')]
)
def update_graph_cat(selected_feature):
    fig = px.box(data, x=selected_feature, y='CO2 Emissions [g/km]')
    return fig


# add a callback to update the prediction
@app.callback(
    Output(component_id='prediction', component_property='children'),
    [Input(component_id='fuel-type', component_property='value'),
     Input(component_id='engine-size', component_property='value'),
     Input(component_id='fuel-consumption-comb', component_property='value')]
)
def update_prediction(fuel_type, engine_size, fuel_consumption_comb):
    df = pd.DataFrame({
        'Engine Size [L]': [engine_size],
        'Fuel Consumption Comb [L/100 km]': [fuel_consumption_comb],
        'Fuel Type_D': [1 if fuel_type == 'D' else 0],
        'Fuel Type_E': [1 if fuel_type == 'E' else 0],
        'Fuel Type_X': [1 if fuel_type == 'X' else 0],
        'Fuel Type_Z': [1 if fuel_type == 'Z' else 0],
    })
    pred = model.predict(df)[0]
    return f'{pred:.2f} g/km'


# STEP 6: run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)