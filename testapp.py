#import dash
#import dash_html_components as html
#import dash_core_components as dcc
#from dash.dependencies import Input, Output, State

import altair as alt
from vega_datasets import data

import pandas as pd     
import datetime as dt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output, State
import plotly.express as px

df = pd.read_csv("data_extra.csv")  

app = dash.Dash(__name__)

#------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            dcc.Checklist(
                id='my_checklist',                      # used to identify component in callback
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['province'].unique()
                ],
                value=['Alberta'],    # values chosen by default

                className='my_box_container',           # class of the container (div)
                # style={'display':'flex'},             # style of the container (div)

                inputClassName='my_box_input',          # class of the <input> checkbox element
                # inputStyle={'cursor':'pointer'},      # style of the <input> checkbox element

                labelClassName='my_box_label',          # class of the <label> that wraps the checkbox input and the option's label
                # labelStyle={'background':'#A5D6A7',   # style of the <label> that wraps the checkbox input and the option's label
                #             'padding':'0.5rem 1rem',
                #             'border-radius':'0.5rem'},

                #persistence='',                        # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
                #persistence_type='',                   # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
            ),
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
    ]),

])

#------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_checklist', component_property='value')]
)
def select_all_none(all_selected, options):
    all = []
    all = [option["value"] for option in options if all_selected]
    return all

def update_graph(options_chosen):

    dff = df[df['province'].isin(options_chosen)]
    print (dff['province'].unique())

    piechart=px.pie(
            data_frame=dff,
            values='population',
            names='province',
            )
    bar_population = alt.Chart(dff).mark_bar().encode(
        alt.X('province'),
        alt.Y('population')
    )
    return (bar_population)

#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)