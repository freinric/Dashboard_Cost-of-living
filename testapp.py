import pandas as pd     
import datetime as dt
import altair as alt

import dash                                     # pip install dash
from dash import dcc, html, Input, Output, html
import plotly.express as px

# provinces?
# https://gist.github.com/Saw-mon-and-Natalie/a11f058fc0dcce9343b02498a46b3d44?short_path=2b4dce3
# https://gist.github.com/jdylanmc/a3fd5ca8c960eaa4b4354445b4480dad?short_path=9a3cad4

df = pd.read_csv("data_extra.csv")  # https://drive.google.com/file/d/1m63TNoZdDUtH5XhK-mc4kDFzO9j97eWW/view?usp=sharing
provs = [x for x in df['province'].unique()]

### PLOT BARCHART FUNCTION ###
def plot_barchart(dff):
    barchart = alt.Chart(dff[-pd.isnull(dff['milk_1L'])]).mark_bar().encode(
    alt.X('milk_1L', title='Cost', axis=alt.Axis(orient='top',format='$')),
    alt.Y('city', sort='x', title=""),
    tooltip=['milk_1L','province'])
    return barchart.to_html()

app = dash.Dash(__name__)
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
                value=['all'],    # values chosen by default


                ### STYLES IN CHECKLIST ###
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
            html.Iframe(
                id='the_graph',
                srcDoc=plot_barchart(df),
                style={'border-width':'0', 'width':'100%','height':'400px'}
            )
    ]),

])

#------------------------------------------------------------------------------

### CALLBACK GRAPH AND CHECKBOXES ###
@app.callback(
    Output(component_id='the_graph', component_property='srcDoc'),
    Output('prov_checklist', 'value'),
    [Input(component_id='prov_checklist', component_property='value')]
)
def update_graph(options_chosen):

    if "all" in options_chosen and len(options_chosen) == 13: # want 'all' only highlighted when len = 14
        #only time everything is highlighted is when 'all', so if not, 'all' not highlighted
        options_chosen.remove('all') # remove 'all' from list, unhighlight
        dff = df[df['province'].isin(options_chosen)] # new df of filtered list
    elif "all" in options_chosen: # if 'all' is selected
        options_chosen = ["all"] + provs # make all highlight when 'all' is chosen
        dff = df # have all dataframe
    elif "all" not in options_chosen and len(options_chosen) == 13: # if all provs are chosen, highlight 'all'
        options_chosen = ["all"] + provs # highlight 'all' if everything else is highlighted
        dff = df
    else: # in all other cases where not 'all'
        dff = df[df['province'].isin(options_chosen)]
    
    return plot_barchart(dff), options_chosen


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)