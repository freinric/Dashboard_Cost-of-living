import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import pandas as pd
from altair import datum

data = pd.read_csv("data_extra.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


### STYLING ###
colors = {
    'background': 'dark',
    'background_dropdown': '#DDDDDD',
    'H1':'#00BBFF',
    'H3': '#7FDBFF'
}

style_dropdown = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", "background-color": colors['background_dropdown'], 'font-weight': 'bold'}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([html.H1('Where do you want to live?', style={
        'textAlign': 'center', 'color': colors['H1']}), html.H3('Cost of Living Dashboard', style={
        'textAlign': 'center', 'color': colors['H3']}),
        

        ### SLIDER ###
        html.P("Select your maxiumum population: ", style={'textAlign': 'center', 'color': colors['H3']}),
        dcc.Slider(id="population", min=0, max=4000000, value=4000000)
        ]), color = colors['background']), 
            md = 3, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),

        ### PLOT 1 LAYOUT###    
        dbc.Col([
            dbc.Col([
                html.H3('Rank Cities by', style = {'width': '100%'}), 
                ### DROPDOWN 1 ###
                dcc.Dropdown(
                    id='drop1',
                    placeholder="Variables",
                    value='meal_cheap',  # REQUIRED to show the plot on the first page load
                    options=[{'label': col, 'value': col} for col in data.columns], 
                    style = style_dropdown)], 
                    style = {'display': 'flex'}),
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '970px'})], style={"height": "10%"}),

        ### PLOT 2  LAYOUT ###
        dbc.Col([
            dbc.Col([html.H3('Compare'),
                     dcc.Dropdown(
                                id='drop2_a',
                                value='meal_cheap',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in data.columns], 
                         style = style_dropdown),
                     html.H3('and'),
                    dcc.Dropdown(
                        id='drop2_b',
                        value='meal_cheap',  # REQUIRED to show the plot on the first page load
                        options=[{'label': col, 'value': col} for col in data.columns], 
                        style =style_dropdown)], 
            style={'display':'flex'}),
            html.Iframe(
                id='scatter2',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}),
            html.Br(),

            ### PLOT 3 LAYOUT ###
            dbc.Col([html.H3('Compare'),
                     dcc.Dropdown(
                                id='drop3_a',
                                value='meal_mid',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in data.columns], 
                                style=style_dropdown),
                     html.H3('among cities'),
                    dcc.Dropdown(
                        id='drop3_b',
                        value=['Vancouver', 'Toronto'],  # REQUIRED to show the plot on the first page load
                        options=[{'label': cities, 'value': cities} for cities in data['city']], multi = True)],
                        style={'width': '100%', 'font-family': 'arial', "font-size": "1.1em", 'font-weight': 'bold'}),
            html.Iframe(
                id='scatter3',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
            
        ])
        ])
])

### PLOT 1 ###
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('drop1', 'value'),
    Input("population", "value"))
def plot_altair1(drop_a, value):
    dataf = data.query(f"population <= {value}")
    chart = alt.Chart(dataf, ).mark_bar().encode(
            x = alt.X(drop_a, axis=alt.Axis(format='$', title=None, orient= 'top')),
            y = alt.Y('city', axis=alt.Axis(title = None), sort='x'),
            tooltip=drop_a).properties(title = f"Cities with population up to {value}").configure_axis(labelFontSize = 16)
    return chart.to_html()

### PLOT 2 ###
@app.callback(
    Output('scatter2', 'srcDoc'),
    Input('drop2_a', 'value'),
    Input('drop2_b', 'value'),
    Input("population", "value"))
def plot_altair2(drop_a, drop_b, value):
    dataf = data.query(f"population <= {value}")
    chart = alt.Chart(dataf).mark_circle().encode(
        x= alt.X(drop_a, axis=alt.Axis(format='$')),
        y=alt.Y(drop_b, axis=alt.Axis(format='$')),
        tooltip=['city', drop_a, drop_b]
    ).configure_axis(labelFontSize = 16, titleFontSize=20)
    return chart.to_html()

### PLOT 3 ###
@app.callback(
    Output('scatter3', 'srcDoc'),
    Input('drop3_a', 'value'),
    Input('drop3_b', 'value'),
    Input("population", "value")
)
def plot_altair3(drop_a, drop_b, value):  
    dataf = data.query(f"population <= {value}")
    chart = alt.Chart(dataf).mark_bar().encode(
        x = alt.X(drop_a, axis=alt.Axis(format='$', title = None)),
        y = alt.Y('city', axis=alt.Axis(title = None))).transform_filter(alt.FieldOneOfPredicate(field='city', oneOf=drop_b)).configure_axis(
    labelFontSize = 16
)

    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)