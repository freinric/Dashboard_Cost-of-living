import pandas as pd     
import datetime as dt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px

df = pd.read_csv("data_extra.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing

app = dash.Dash(__name__)
options = [{'label': x, 'value': x, 'disabled':False} for x in df['province'].unique()]
#------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "My Checklist",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
### CHECKLIST ### 
        html.Div([
            dcc.Checklist(["all"], [], id="all-checklist", inline=True),
            dcc.Checklist(
                id='prov_checklist',                      # used to identify component in callback
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['province'].unique()],
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
    Output("prov-checklist", "value"),
    Output("all-checklist", "value"),
    [Input("prov-checklist", "value"),
    Input("all-checklist", "value")],
)
def sync_checklists(cities_selected, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "prov-checklist":
        all_selected = ["All"] if set(cities_selected) == set(options) else []
    else:
        cities_selected = options if all_selected else []
    return cities_selected, all_selected

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='prov_checklist', component_property='value')]
)
def update_graph(options_chosen):

    dff = df[df['province'].isin(options_chosen)] # new df of filtered by checklist
    #print (dff['province'].unique()) # i think this prints in the terminal which are used, not useful

    piechart=px.pie(
            data_frame=dff,
            values='population',
            names='province',
            )

    return (piechart)



#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)