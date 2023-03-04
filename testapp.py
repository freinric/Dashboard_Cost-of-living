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

### PLOT 1 FUNCTION ###
def plot_altair1(dff):
    barchart = alt.Chart(dff[-pd.isnull(dff['milk_1L'])]).mark_bar().encode(
    alt.X('milk_1L', title='Cost', axis=alt.Axis(orient='top',format='$')),
    alt.Y('city', sort='x', title=""),
    tooltip=['milk_1L','province'])
    return barchart.to_html()

### PLOT 2 FUNCTION ###
"""@app.callback(
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
    return chart.to_html()"""

app = dash.Dash(__name__)
#------------------------------------------------------------------------------
app.layout = html.Div([

        html.Div([
            html.Pre(children= "Checklist",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
        
        html.Div([
            ### CHECKLIST ### 
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
            ### SLIDER ###
            dcc.RangeSlider(id="population", min=0, max=4000000, value=[0,4000000])
        ]),
### GRAPH ### 
        html.Div([
            html.Iframe(
                id='plot1',
                srcDoc=plot_altair1(df),
                style={'border-width':'0', 'width':'100%','height':'400px'}
            )
    ]),
])

#------------------------------------------------------------------------------

### CALLBACK GRAPHS AND CHECKBOXES ###
@app.callback(
    Output(component_id='plot1', component_property='srcDoc'),
    Output('prov_checklist', 'value'),
    [Input(component_id='prov_checklist', component_property='value'),
     Input('population', 'value')]
)
def update_df(options_chosen, population_chosen):
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]

    if "all" in options_chosen and len(options_chosen) == 13: # want 'all' only highlighted when len = 14
        #only time everything is highlighted is when 'all', so if not, 'all' not highlighted
        options_chosen.remove('all') # remove 'all' from list, unhighlight
        dff = dff[dff['province'].isin(options_chosen)] # new df of filtered list
    elif "all" in options_chosen: # if 'all' is selected
        options_chosen = ["all"] + provs # make all highlight when 'all' is chosen
        dff = dff # have all dataframe
    elif "all" not in options_chosen and len(options_chosen) == 13: # if all provs are chosen, highlight 'all'
        options_chosen = ["all"] + provs # highlight 'all' if everything else is highlighted
        dff = dff
    else: # in all other cases where not 'all'
        dff = dff[dff['province'].isin(options_chosen)]
    
    return plot_altair1(dff), options_chosen


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)