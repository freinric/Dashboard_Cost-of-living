import pandas as pd     
import datetime as dt
import altair as alt

import dash                                     
from dash import dcc, html, Input, Output, html
import plotly.express as px
import dash_bootstrap_components as dbc

# POSSIBLE LINKS FOR TOPJSON MAP
# https://gist.github.com/Saw-mon-and-Natalie/a11f058fc0dcce9343b02498a46b3d44?short_path=2b4dce3
# https://gist.github.com/jdylanmc/a3fd5ca8c960eaa4b4354445b4480dad?short_path=9a3cad4

#------------------------------------------------------------------------------

### TABLE OF CONTENTS ###
# DEFINING 'GLOBAL' VARIABLES
# PLOT FUNCTIONS
# APP LAYOUT
# CALLBACK

#------------------------------------------------------------------------------
# DEFINING
df = pd.read_csv("data_extra.csv")  
provs = [x for x in df['province'].unique()]

colors = {
    'background': 'dark',
    'background_dropdown': '#DDDDDD',
    'H1':'#00BBFF',
    'H2':'#7FDBFF',
    'H3':'#005AB5'
}
style_dropdown = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", "background-color": colors['background_dropdown'], 'font-weight': 'bold', 'textAlign': 'left'}

style_dropdown_multi = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", 'font-weight': 'bold'}

style_H1 = {'textAlign': 'center', 'color': colors['H1']} # Title
style_H2 = {'textAlign': 'center', 'color': colors['H2']} # Subtitle
style_H3_c = {'textAlign': 'center', 'color': colors['H3'], 'width': '100%', 'margin-right': '0'} # Position: Center
style_H3 = {'color': colors['H3'], 'width': '100%', 'margin-right': '0'} # Position: left

style_plot1 = {'border-width': '0', 'width': '100%', 'height': '970px'}
style_plot2 = {'border-width': '0', 'width': '100%', 'height': '400px'}
style_plot3 = {'border-width': '0', 'width': '100%', 'height': '400px'}

style_card = {'border': '1px solid #d3d3d3', 'border-radius': '10px'}

#------------------------------------------------------------------------------
### PLOT 1 FUNCTION ###
def plot_altair1(dff, drop1_chosen):
    barchart = alt.Chart(dff[-pd.isnull(dff[drop1_chosen])]).mark_bar().encode(
    alt.X(drop1_chosen, title = 'Cost of '+ drop1_chosen, axis = alt.Axis(orient='top',format='$')),
    alt.Y('city', sort = 'x', title = ""),
    tooltip = [drop1_chosen,'province']).configure_axis(labelFontSize = 16, titleFontSize=20)
    return barchart.to_html()

### PLOT 2 FUNCTION ###
def plot_altair2(dff, drop_a, drop_b):
    chart = alt.Chart(dff).mark_circle().encode(
        x = alt.X(drop_a, axis = alt.Axis(format = '$')),
        y = alt.Y(drop_b, axis = alt.Axis(format = '$')),
        tooltip = ['city', drop_a, drop_b]
    ).configure_axis(labelFontSize = 16, titleFontSize = 20)
    return chart.to_html()

### PLOT 3 FUNCTION ###
def plot_altair3(dff, drop_a, drop_b):  
    chart = alt.Chart(dff).mark_bar().encode(
        x = alt.X(drop_a, axis = alt.Axis(format ='$', title = None)),
        y = alt.Y('city', axis = alt.Axis(title = None))
        ).transform_filter(alt.FieldOneOfPredicate(field ='city', oneOf=drop_b)
                           ).configure_axis(labelFontSize = 16)
    return chart.to_html()

#------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
       dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([html.H1('Where do you want to live?', style = style_H1), 
                              html.H3('Cost of Living Dashboard', style = style_H2)]),
                color = colors['background']),
            html.Br(),
            
            ### CHECKLIST ###
            html.H3("Select the Province: ", style = style_H3_c),
            dcc.Checklist(
                    id = 'prov_checklist',                
                    options = [{'label': 'Select all', 'value': 'all', 'disabled':False}] +
                             [{'label': x, 'value': x, 'disabled':False}
                             for x in df['province'].unique()],
                    value = ['all'],    # values chosen by default

                    ### STYLES IN CHECKLIST ###
                    className = 'my_box_container', 
                    inputClassName = 'my_box_input',         
                    labelClassName = 'my_box_label',          
                ),
            html.Br(),
            
            ### SLIDER ###
            html.H3("Select City Population: ", style = style_H3_c),
            dcc.RangeSlider(id="population", min=0, max=4000000, value=[0,4000000])], 
            md = 3, style = style_card),
             
        ### PLOT 1 LAYOUT###    
        dbc.Col([
            dbc.Col([
                html.H3('Rank Cities by', style = style_H3_c), 
                ### DROPDOWN 1 ###
                dcc.Dropdown(
                    id = 'drop1',
                    placeholder = "Variables",
                    value = 'meal_cheap',  
                    options = [{'label': col, 'value': col} for col in df.columns], 
                    style = style_dropdown)], 
                    style = {'display': 'flex'}),
                html.Iframe(
                    id = 'plot1',
                    style = style_plot1)], 
            style = {"height": "10%"}),

        ### PLOT 2  LAYOUT ###
        dbc.Col([
            dbc.Col([html.H3('Compare', style = style_H3),
                     dcc.Dropdown(
                                id = 'drop2_a',
                                value = 'meal_cheap',  # REQUIRED to show the plot on the first page load
                                options = [{'label': col, 'value': col} for col in df.columns], 
                         style = style_dropdown),
                     html.H3('and', style = style_H3_c),
                    dcc.Dropdown(
                        id = 'drop2_b',
                        value = 'meal_cheap',  # REQUIRED to show the plot on the first page load
                        options = [{'label': col, 'value': col} for col in df.columns], 
                        style = style_dropdown)], 
            style = {'display':'flex'}),
            html.Iframe(
                id = 'plot2',
                style = style_plot2),
            html.Br(),
            
            ### PLOT 3 LAYOUT ###
            dbc.Col([html.H3('Compare', style = style_H3),
                     dcc.Dropdown(
                                id = 'drop3_a',
                                value = 'meal_mid',  # REQUIRED to show the plot on the first page load
                                options = [{'label': col, 'value': col} for col in df.columns], 
                                style = style_dropdown),
                     html.H3('among Cities', style = style_H3),
                    dcc.Dropdown(
                        id = 'drop3_b',
                        value = ['Vancouver', 'Toronto'],  # REQUIRED to show the plot on the first page load
                        options = [{'label': cities, 'value': cities} for cities in df['city']], multi = True)],
                        style = style_dropdown_multi),
            html.Iframe(
                id='plot3',
                style=style_plot3)
            
        ])
        ])
])

#------------------------------------------------------------------------------

### CALLBACK GRAPHS AND CHECKBOXES ###
@app.callback(
    Output(component_id='plot1', component_property='srcDoc'),
    Output(component_id='plot2', component_property='srcDoc'),
    Output(component_id='plot3', component_property='srcDoc'),
    Output('prov_checklist', 'value'),
    [Input(component_id='prov_checklist', component_property='value'),
     Input('population', 'value'),
     Input('drop1', 'value'),
     Input('drop2_a', 'value'),
     Input('drop2_b', 'value'),
     Input('drop3_a', 'value'),
     Input('drop3_b', 'value'),
     ]
)
def update_df(options_chosen, population_chosen, 
              drop1_chosen, 
              drop2a_chosen, drop2b_chosen, 
              drop3a_chosen, drop3b_chosen):

    # filter by population
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    
    # filtering by provinces chosen + updating the checkboxes with 'select all'
    if "all" in options_chosen and len(options_chosen) == 13: # want 'all' only highlighted when len = 14
        options_chosen.remove('all') # remove 'all' from list, unhighlight
        dff = dff[dff['province'].isin(options_chosen)] # new df of filtered list

    elif "all" in options_chosen: # if 'all' is selected
        options_chosen = ["all"] + provs # make all highlight when 'all' is chosen
        #dff = dff # have all dataframe

    elif "all" not in options_chosen and len(options_chosen) == 13: # if all provs are chosen, highlight 'all'
        options_chosen = ["all"] + provs # highlight 'all' if everything else is highlighted
        #dff = dff

    else: # in all other cases where not 'all'
        dff = dff[dff['province'].isin(options_chosen)]

    return (plot_altair1(dff, drop1_chosen), 
            plot_altair2(dff, drop2a_chosen, drop2b_chosen), 
            plot_altair3(dff, drop3a_chosen, drop3b_chosen),
            options_chosen)


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)