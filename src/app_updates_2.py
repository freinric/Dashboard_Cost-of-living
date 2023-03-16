import pandas as pd
import altair as alt

import dash                                     
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# POSSIBLE LINKS FOR TOPJSON MAP
# https://gist.github.com/Saw-mon-and-Natalie/a11f058fc0dcce9343b02498a46b3d44?short_path=2b4dce3
# https://gist.github.com/jdylanmc/a3fd5ca8c960eaa4b4354445b4480dad?short_path=9a3cad4

#------------------------------------------------------------------------------

### TABLE OF CONTENTS ###
# DEFINING 'GLOBAL' VARIABLES
# APP LAYOUT
# CALLBACKS
## CHECKBOXES
## PLOT FUNCTIONS

#------------------------------------------------------------------------------
# DEFINING
df = pd.read_csv("data/processed/data.csv")  
provs = sorted([x for x in df['province'].unique()])

# import new names
new_names = pd.read_csv("data/processed/data_new_names.csv", header = 0)
# df to list
old = new_names.old_name.values.tolist()
new  = new_names.new_name.values.tolist()
# lists to dictionary
new_name_dic = {}
for key in old:
    for value in new:
        new_name_dic[key] = value
        new.remove(value)
        break
# now the new names are stored in the dictionary titled new_name_dict

colors = {
    'background': 'dark',
    'background_dropdown': '#DDDDDD',
    'H1':'#00BBFF',
    'H2':'#7FDBFF',
    'H3':'#005AB5'
}


style_dropdown = {'width': '100%', 'font-family': 'arial', "font-size": "1.1em", "background-color": colors['background_dropdown'], 'font-weight': 'bold'}

style_H1 = {'textAlign': 'center', 'color': colors['H1']} # Title
style_H2 = {'textAlign': 'center', 'color': colors['H2']} # Subtitle
style_H3_c = {'textAlign': 'center', 'color': colors['H3'], 'width': '100%'} # For card
style_H3 = {'color': colors['H3'], 'width': '100%'} # For Charts Title

style_plot1 = {'border-width': '0', 'width': '100%', 'height': '970px'}
style_plot2 = {'border-width': '0', 'width': '100%', 'height': '400px'}
style_plot3 = {'border-width': '0', 'width': '100%', 'height': '400px'}

style_card = {'border': '1px solid #d3d3d3', 'border-radius': '10px'}

#------------------------------------------------------------------------------






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
            dcc.Checklist(['Select All'],['Select All'],id="all_checklist"),
            dcc.Checklist(
                    id='prov_checklist',                
                    options=
                             [{'label': x, 'value': x, 'disabled':False}
                             for x in provs],    # values chosen by default

                    ### STYLES IN CHECKLIST ###
                    className='my_box_container', 
                    inputClassName='my_box_input',         
                    labelClassName='my_box_label', 
                    inputStyle={"margin-right": "3px", "margin-left":"20px"},         
                ),
            html.Br(),
            
            ### SLIDER ###
            html.H3("Select City Population: ", style = style_H3_c),
            dcc.RangeSlider(id="population", min=0, max=2800000, step = 1000, 
                            marks={100000: '100k',
                                   500000: '500k',
                                   1000000: '1M',
                                   1500000: '1.5M',
                                   2000000: '2M',
                                   2500000: '2.5M',
                                   3000000: '3M'},
                            value=[0,2800000]),
                       html.Div(id='slider-output-container')], 
                            md = 3, style = style_card),
           html.Br(),
             
        ### PLOT 1 LAYOUT###    
        dbc.Col([
            dbc.Col([
                html.H3('Rank Cities by', style = style_H3), 
                ### DROPDOWN 1 ###
                dcc.Dropdown(
                    id='drop1',
                    placeholder="Variables",
                    value='meal_cheap',  
                    options=[{'label': new_name_dic[col], 'value': col} for col in df.columns[2:55]], # only including actual variables
                    style = style_dropdown)], 
                    style = {'display': 'flex'}),
                html.Iframe(
                    id='plot1',
                    style = style_plot1)], 
            style={"height": "10%"}),

        ### PLOT 2  LAYOUT ###
        dbc.Col([
            dbc.Col([html.H3('Compare ', style = {'color': colors['H3']}),
                     dcc.Dropdown(
                                id='drop2_a',
                                value='meal_cheap', 
                                options=[{'label': new_name_dic[col], 'value': col} for col in df.columns[2:55]], 
                         style = style_dropdown),
                     html.H3('and ', style  = {'color': colors['H3']}),
                    dcc.Dropdown(
                        id='drop2_b',
                        value='meal_mid', 
                        options=[{'label': new_name_dic[col], 'value': col} for col in df.columns[2:55]], 
                        style =style_dropdown)], 
            style={'display':'flex'}),
            html.Iframe(
                id='plot2',
                style = style_plot2),
            html.Br(),
            
            ### PLOT 3 LAYOUT ###
            dbc.Col([html.H3('Compare', style = style_H3),
                     dcc.Dropdown(
                                id='drop3_a',
                                value='meal_mid', 
                                options=[{'label': new_name_dic[col], 'value': col} for col in df.columns[2:55]], 
                                style=style_dropdown),
                     html.H3('among Cities', style = style_H3),
                     dcc.Dropdown(
                        id='drop3_b',
                        value=['Vancouver', 'Toronto'], 
                        options=[{'label': cities, 'value': cities} for cities in df['city']], multi = True)],
                    style={'width': '100%', 'font-family': 'arial', "font-size": "1.1em", 'font-weight': 'bold'}),
            html.Iframe(
                id='plot3',
                style=style_plot3)
        ])
        ])
])

#------------------------------------------------------------------------------

### CALLBACK GRAPHS AND CHECKBOXES ###


### CHECKBOXES ###
@app.callback(
        Output("prov_checklist", "value"),
        Output("all_checklist", "value"),
        Input("prov_checklist", "value"),
        Input("all_checklist", "value"),
)
def sync_checklists(prov_chosen, all_chosen):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "prov_checklist":
        all_chosen = ["Select all"] if set(prov_chosen) == set(provs) else []
    else:
        prov_chosen = provs if all_chosen else []
    return prov_chosen, all_chosen  

### SLIDER
@app.callback(
    Output('slider-output-container', 'children'),
    Input('population', 'value'))
def update_output(value):
    return 'You have selected cities with population between {} and {}'.format(value[0], value[1])


### PLOT 1 ###
@app.callback(
        Output('plot1', 'srcDoc'),
        Input('prov_checklist', 'value'),
        Input('population','value'),
        Input('drop1','value'),
)
def plot_altair1(prov_chosen, population_chosen, drop1_chosen):
    # filtering df
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    dff = dff[dff['province'].isin(prov_chosen)]

    barchart = alt.Chart(dff[-pd.isnull(dff[drop1_chosen])]).mark_bar().encode(
    alt.X(drop1_chosen, title='Cost of '+drop1_chosen, axis=alt.Axis(orient='top',format='$.0f')),
    alt.Y('city', sort='x', title=""),
    tooltip=[drop1_chosen,'province']).configure_axis(labelFontSize = 16, titleFontSize=20)
    return barchart.to_html()

### PLOT 2 ###
@app.callback(
        Output('plot2', 'srcDoc'),
        Input('prov_checklist', 'value'),
        Input('population','value'),
        Input('drop2_a', 'value'),
        Input('drop2_b', 'value'),
)
def plot_altair2(prov_chosen, population_chosen, drop_a, drop_b,):
    # filtering df
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    dff = dff[dff['province'].isin(prov_chosen)]

    # plot chart
    chart = alt.Chart(dff).mark_circle().encode(
        x= alt.X(drop_a, axis=alt.Axis(format='$.0f')),
        y=alt.Y(drop_b, axis=alt.Axis(format='$.0f')),
        tooltip=['city', drop_a, drop_b]
    ).configure_axis(labelFontSize = 16, titleFontSize=20)
    return chart.to_html()

### PLOT 3 ###
@app.callback(
        Output('plot3', 'srcDoc'),
        Output('drop3_b', 'options'),
        Input('prov_checklist', 'value'),
        Input('population','value'),
        Input('drop3_a', 'value'),
        Input('drop3_b', 'value'),
)
def plot_altair3(prov_chosen, population_chosen, drop_a, drop_b,):
    # filtering df
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    dff = dff[dff['province'].isin(prov_chosen)]

    prov_cities = [{'label': cities, 'value': cities} for cities in dff['city']]

    # plot chart
    chart = alt.Chart(dff).mark_bar().encode(
        x = alt.X(drop_a, axis=alt.Axis(format='$.0f', title = None)),
        y = alt.Y('city',sort='x', axis=alt.Axis(title = None))
        ).transform_filter(alt.FieldOneOfPredicate(field='city', oneOf=drop_b)
                           ).configure_axis(labelFontSize = 16)
    return chart.to_html(), prov_cities


#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)