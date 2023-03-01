import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import pandas as pd

data = pd.read_csv("data_extra.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([html.H1('Where do you want to live?'), html.H3('Cost of Living Dashboard')])), 
            md = 4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),
        dbc.Col([
            dbc.Col([html.H3('Rank Cities by'), dcc.Dropdown(
                id='xcol-widget',
                value='meal_cheap',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in data.columns])]),
            html.Div(id='mean-x-div'),
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})]),
        dbc.Col([
            dbc.Col([html.H3('Compare Variables'),
                     dcc.Dropdown(
                                id='xcol-widget2',
                                value='meal_cheap',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in data.columns]),
                    dcc.Dropdown(
                        id='ycol-widget2',
                        value='meal_cheap',  # REQUIRED to show the plot on the first page load
                        options=[{'label': col, 'value': col} for col in data.columns])], 
            md = 4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),
            html.Iframe(
                id='scatter2',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}),
            html.Br(),
            
            dbc.Col([html.H3('Compare Variable for Cities'),
                     dcc.Dropdown(
                                id='xcol-widget3',
                                value='meal_cheap',  # REQUIRED to show the plot on the first page load
                                options=[{'label': col, 'value': col} for col in data.columns])],
#                     dcc.Dropdown(
#                         id='ycol-widget3',
#                         value='Vancouver',  # REQUIRED to show the plot on the first page load
#                         options=[{'label': cities, 'value': cities} for cities in data['city']], multi = True)], 
            md = 4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),
            html.Iframe(
                id='scatter3',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
            
        ])
        ])
])
@app.callback(
    Output('scatter', 'srcDoc'),
    Output('mean-x-div', 'children'),
    Input('xcol-widget', 'value'))
def plot_altair2(xcol):
    chart = alt.Chart(data).mark_bar().encode(
            x = alt.X(xcol, axis=alt.Axis(format='$', title=None, orient= 'top')),
            y = alt.Y('city', axis=alt.Axis(title = None), sort='x'),
            tooltip=xcol)
    return chart.to_html(), f'The mean of {xcol} is {round(data[xcol].mean(), 1)}'

@app.callback(
    Output('scatter2', 'srcDoc'),
    Input('xcol-widget2', 'value'),
    Input('ycol-widget2', 'value'))
def plot_altair2(xcol, ycol):
    chart = alt.Chart(data).mark_circle().encode(
        x=xcol,
        y=ycol,
        tooltip=['city', xcol, ycol]
    )
    return chart.to_html()

@app.callback(
    Output('scatter3', 'srcDoc'),
    Input('xcol-widget3', 'value'))
def plot_altair3(xcol):  # Still thinking how to select multiple ones from binding_select
    dropdown_city = alt.binding_select(options=[None] + list(data['city'].unique()), labels = ['All'] + list(data['city'].unique()), name = "Cities")
    selection_city = alt.selection_single(fields=['city'], bind=dropdown_city)

    chart = alt.Chart(data).mark_bar().encode(
        x = alt.X(xcol, axis=alt.Axis(format='$')),
        y = alt.Y('city', axis=alt.Axis(title = None))
    ).add_selection(selection_city).transform_filter(
        selection_city
    )
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)