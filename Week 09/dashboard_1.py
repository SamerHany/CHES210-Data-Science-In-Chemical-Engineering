# STEP 1: import libraries
import pandas as pd
from plotly import express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


# STEP 2: create a Dash app
app = Dash(__name__)


# STEP 3: load & process data
df = pd.read_csv("CO2_Emissions_Canada.csv")

# create a list of numerical features
features_num = df.select_dtypes(include=['int64', 'float64']).columns


# STEP 4: create a Dash layout that contains a Dropdown component
# and a Plotly graph
app.layout = html.Div([
    html.H1('CO2 Emissions in Canada'),
    html.Div([
        dcc.Dropdown(
            id='feature-num',
            options=[{'label': feature, 'value': feature} for feature in features_num],
            value='Engine Size [L]'
        ),
        dcc.Graph(id='plot-num')
    ])
])


# STEP 5: add a callback to update the graph
@app.callback(
    Output(component_id='plot-num', component_property='figure'),
    [Input(component_id='feature-num', component_property='value')]
)
def update_graph(selected_feature):
    fig = px.scatter(df, x=selected_feature, y='CO2 Emissions [g/km]')
    return fig


# STEP 6: run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)