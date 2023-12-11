# STEP 1: import libraries
import pandas as pd
from plotly import express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output



# STEP 2: create a Dash app
app = Dash(__name__)



# STEP 3: load & process data
df = pd.read_csv("CO2_Emissions_Canada.csv")

# create a list of available features
features = df.columns



# STEP 4: create a Dash layout that contains a Dropdown component
# and a Plotly graph
app.layout = html.Div([
    html.Div('CO2 Emissions in Canada'),
    dcc.Dropdown(
        id='feature',
        options=[{'label': feature, 'value': feature} for feature in features],
        value='Engine Size [L]'
    ),
    dcc.Graph(id='plot')
])



# STEP 5: add a callback to update the graph
@app.callback(
    Output(component_id='plot', component_property='figure'),
    [Input(component_id='feature', component_property='value')]
)
def update_graph(selected_feature):
    fig = px.scatter(df, x=selected_feature, y='CO2 Emissions [g/km]', trendline='ols', trendline_color_override='red')
    return fig



# STEP 6: run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)