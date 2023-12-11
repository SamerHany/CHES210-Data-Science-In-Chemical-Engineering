# import libraries
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly import express as px

# create a Dash app
app = Dash(__name__)

# load data
data = pd.read_csv("CO2_Emissions_Canada.csv")

# create a list of numerical features
features_num = data.select_dtypes(include=['int64', 'float64']).columns

# create a list of categorical features
features_cat = data.select_dtypes(include=['object']).columns



# create a Dash layout that contains a Dropdown component
# and a Plotly graph
app.layout = html.Div([
    # title
    html.H1("CO2 Emissions in Canada", style={
        'text-align': 'center', 
        'margin': '20px',
        'padding': '20px', 
        'background-color': 'white',
        'box-shadow': '0px 0px 5px 5px lightgrey',
        'border-radius': '10px',
    }),

    # graphs
    html.Div([
        # numerical features CARD
        html.Div([
            html.H3("Numerical Features"),
            dcc.Dropdown(
                id='feature-num',
                options=[{'label': i, 'value': i} for i in features_num],
                value='Engine Size [L]'
            ),
            html.Hr(style={'margin-top': '20px', 'border-color': 'lightgrey'}),
            dcc.Graph(id='plot-num')
        ], style={
            'background-color': 'white', 
            'padding': '10px', 
            'box-shadow': '0px 0px 5px 5px lightgrey',
            'border-radius': '10px',
            'flex': '1 1 auto',
        }),

        # categorical features CARD
        html.Div([
            html.H3("Categorical Features"),
            dcc.Dropdown(
                id='feature-cat',
                options=[{'label': i, 'value': i} for i in features_cat],
                value='Fuel Type'
            ),
            html.Hr(style={'margin-top': '20px', 'border-color': 'lightgrey'}),
            dcc.Graph(id='plot-cat')
        ], style={
            'background-color': 'white', 
            'padding': '10px', 
            'box-shadow': '0px 0px 5px 5px lightgrey',
            'border-radius': '10px',
            'width': '50%',
            # 'flex': '1 1 auto',
        })
    ], style={
        'padding': '20px',
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'stretch',
        'flex-wrap': 'wrap',
        'gap': '20px',
    }),
], style={'margin': '0px', 'padding': '0px', 'background-color': 'white'})


# add a callback to update the NUM graph
@app.callback(
    Output(component_id='plot-num', component_property='figure'),
    [Input(component_id='feature-num', component_property='value')]
)
def update_graph_num(selected_feature):
    fig = px.scatter(data, x=selected_feature, y='CO2 Emissions [g/km]', trendline='ols', trendline_color_override='red')
    return fig



# add a callback to update the CAT graph
@app.callback(
    Output(component_id='plot-cat', component_property='figure'),
    [Input(component_id='feature-cat', component_property='value')]
)
def update_graph_cat(selected_feature):
    fig = px.box(data, x=selected_feature, y='CO2 Emissions [g/km]')
    return fig


# run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)