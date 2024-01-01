# STEP 1: import libraries
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly import express as px


# STEP 2: create a Dash app
app = Dash(__name__)


# STEP 3: load & process data
data = pd.read_csv("CO2_Emissions_Canada.csv")

# create a list of numerical features
features_num = data.select_dtypes(include=['int64', 'float64']).columns

# create a list of categorical features
features_cat = data.select_dtypes(include=['object']).columns


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

# and a Plotly graph
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
])


# STEP 5: add callbacks for interactive components
# add a callback to update the NUM graph
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


# STEP 6: run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)