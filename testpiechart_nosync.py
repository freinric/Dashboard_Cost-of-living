import pandas as pd     
import datetime as dt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px

df = pd.read_csv("data_extra.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing

app = dash.Dash(__name__)
#options = [{'label': x, 'value': x, 'disabled':False} for x in df['province'].unique()]
#------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "Checklist",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
### CHECKLIST ### 
        html.Div([
            dcc.Checklist(
                id='prov_checklist',                      # used to identify component in callback
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['province'].unique()] + [{'label': 'Select all', 'value': 'all', 'disabled':False}],
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
### GRAPH ### 
        html.Div([
            dcc.Graph(id='the_graph')
    ]),

])

#------------------------------------------------------------------------------


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='prov_checklist', component_property='value')]
)
def update_graph(options_chosen):
    #print (dff['province'].unique()) # i think this prints in the terminal which are used, not useful
    if "all" in options_chosen:
        dff = df
    else:
        dff = df[df['province'].isin(options_chosen)] # new df of filtered by checklist
        
    piechart=px.pie(
            data_frame=dff,
            values='population',
            names='province',
            )

    return (piechart)



#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)