import pandas as pd     
import datetime as dt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px

# provinces?
# https://gist.github.com/Saw-mon-and-Natalie/a11f058fc0dcce9343b02498a46b3d44?short_path=2b4dce3
# https://gist.github.com/jdylanmc/a3fd5ca8c960eaa4b4354445b4480dad?short_path=9a3cad4

df = pd.read_csv("data_extra.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing
provs = [x for x in df['province'].unique()]


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
                options=[{'label': 'Select all', 'value': 'all', 'disabled':False}] +
                         [{'label': x, 'value': x, 'disabled':False}
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

### CALLBACK GRAPH AND CHECKBOXES ###
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    Output('prov_checklist', 'value'),
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
    
    if "all" in options_chosen and len(options_chosen) == 13: # only time everything is highlighted is when 'all', so if not, 'all' not highlighted
        options_chosen.remove('all') # remove 'all' from list
    elif "all" in options_chosen: # if 'all' is selected when
        options_chosen = ["all"] + provs # make all highlight when 'all' is chosen
    elif "all" not in options_chosen and len(options_chosen) == 13:
        options_chosen = ["all"] + provs # highlight 'all' if everything else is highlighted
    return (piechart), options_chosen


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)