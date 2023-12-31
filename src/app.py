import pandas as pd
import altair as alt
import json

import dash                                     
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

#------------------------------------------------------------------------------

### TABLE OF CONTENTS ###
# DEFINING 'GLOBAL' VARIABLES
# APP LAYOUT
# CALLBACKS
## CHECKBOXES
## PLOT FUNCTIONS

#------------------------------------------------------------------------------
# DEFINING
#------------------------------------------------------------------------------
df = pd.read_csv("../data/processed/data.csv")  
provs = sorted([x for x in df['province'].unique()])

## data for map
canada_province = json.load(open("../data/processed/georef-canada-province@public.geojson", 'r'))

# modify geojson issue
for feature in canada_province["features"]:
    feature["properties"]["prov_name_en"] = feature["properties"]["prov_name_en"][0]
data_geojson = alt.InlineData(values=canada_province, format=alt.DataFormat(property='features',type='json'))

# import new names
new_names = pd.read_csv("../data/processed/data_new_names.csv", header = 0)
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

# dropdown options
newoptions = [{'label': new_name_dic[col], 'value': col} for col in df.columns[2:57]]


### CHECKBOX CATEGORY FUNCTION
def col_filter(cat_value):
    cols = ['city', 'data_quality','province', 'population']
    for i in cat_value:
        if i == 'restaurant':
            cols = cols + list(df.columns[2:10])
        if i == 'market':
            cols = cols + list(df.columns[10:29])
        if i == 'transportation':
            cols = cols + list(df.columns[29:37])
        if i == 'utilities':
            cols = cols + list(df.columns[37:40])
        if i == 'leisure':
            cols = cols + list(df.columns[40:43])
        if i == 'childcare':
            cols = cols + list(df.columns[43:45])
        if i == 'clothing':
            cols = cols + list(df.columns[45:49])
        if i == 'home':
            cols = cols + list(df.columns[49:57])
    return cols
#------------------------------------------------------------------------------
### STYLES
#------------------------------------------------------------------------------
colors = {
    'background': '#fff3d9',
    'background_dropdown': '#fff3d9',
    'H1':'#bd0005',
    'H2':'#dd431f',
    'H3':'#bd0005',
    'light':'#FF8B68',
    'teal':'#00bdb8'
}

style_dropdown = {'width': '230px', 'font-family': 'arial', 
                  "font-size": "1.1em", "background-color": colors['background_dropdown'], 
                  'font-weight': 'bold', 'border':'0px'}
style_dropdown_c = {'width': '100%', 'font-family': 'arial', 
                  "font-size": "1.1em", "background-color": colors['background_dropdown'], 
                  'font-weight': 'bold', 'border':'0px'}

# Title
style_H1 = {'textAlign': 'center', 'color': colors['H1']}
# Subtitle
style_H2 = {'textAlign': 'center', 'color': colors['H2']} 
# For card
style_H3_c = {'textAlign': 'center', 'color': colors['H3'], 'width': '100%'} 
# For Charts Title
style_H3 = {'color': colors['H3'], 'width': '100%'} 
# description box
style_descbox = {'border':'1px solid #d3d3d3', 'background-color':colors['background']}
# filters box
style_filterbox = {'border': '1px solid #d3d3d3'}

# For notes
style_Note = {'textAlign': 'left', 'color': colors['H2']} 

# style={'overflowY': 'scroll', 'height': 500}
style_plot1 = {'border-width': '0', 'width': '100%', 'height': '800px'}
style_plot2 = {'border-width': '0', 'width': '100%', 'height': '400px'}
style_plot3 = {'border-width': '0', 'width': '100%', 'height': '350px'}

style_card = {'border': '1px solid #d3d3d3'}

#------------------------------------------------------------------------------
### APP LAYOUT ###
#------------------------------------------------------------------------------
app = dash.Dash(__name__, title='Cost of Living Dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
       dbc.Row([
        dbc.Col([
            html.Div([html.H1('Where do you want to live?', style = style_H1), 
#                     html.H3('Cost of Living Dashboard', style = style_H2),
                    html.P('Selecting different provinces, population ranges, and categories of interest to explore the costs of living in Canada can guide you to places within your budget.', style=style_H2)],
                    style=style_descbox),

            html.Div([
            html.Br(),
            ### CHECKLIST PROVINCES###
            html.H3("Select Provinces: ", style = style_H3_c),
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
                            value=[0,2800000],
                            tooltip={"placement": "bottom", "always_visible": False}),
                       html.Div(id='slider-output-container'),
           html.Br(),
           
           ### CATEGORY CHECKLIST ###
            html.H3("Select Dropdown Variable Categories: ", style = style_H3_c),
            dcc.Checklist(
                    id='category_checklist',                
                    options=[{'label': 'Restaurant', 'value': 'restaurant'},
                             {'label': 'Grocery', 'value': 'market'},
                             {'label': 'Transportation', 'value': 'transportation'},
                             {'label': 'Utilities', 'value': 'utilities'},
                             {'label': 'Leisure', 'value': 'leisure'},
                             {'label': 'Childcare', 'value': 'childcare'},
                             {'label': 'Clothing', 'value': 'clothing'},
                             {'label': 'Living', 'value': 'home'},
                       ],
                       value=['restaurant'],    # values chosen by default

                    ### STYLES IN CHECKLIST ###
                    className='my_box_container', 
                    inputClassName='my_box_input',         
                    labelClassName='my_box_label', 
                    inputStyle={"margin-right": "3px", "margin-left":"20px"},         
                )],
                style=style_filterbox),
            
            ### Mention the sources
            html.Br(),
            html.Br(),
            html.Br(),
            html.P('The data was collected in Dec 2022.', style=style_Note),
            html.P('The original costs are in USD, we use the FX rate 1.38 to convert them to CAD.', style=style_Note),
            html.P('Our data resource is Kaggle, please find the link bellow.', style=style_Note),
            dbc.NavItem(dbc.NavLink("Kaggle Link", href="https://www.kaggle.com/datasets/mvieira101/global-cost-of-living?select=cost-of-living_v2.csv")),
            html.P('The original data is crowdsourced from Numbeo, please find the link bellow.', style=style_Note),
            dbc.NavItem(dbc.NavLink("Numbeo Link", href="https://www.numbeo.com/, terms of use are to link back to them"))
            ],
                            md = 3),
        
        dbc.Col([
            ### PLOT 3 LAYOUT ###
            dbc.Col([html.H3('Map of Canada: Province Region', style = style_H3)],

                    style={'width': '100%', 'font-family': 'arial', "font-size": "1.1em", 'font-weight': 'bold'}),
            html.Iframe(
                id='plot_map',
                style=style_plot3),
            html.Br(),
            ### PLOT 2 LAYOUT###  
            dbc.Col([html.H3('Compare: ', style = {'color': colors['H3']})], 
                    style={'display':'flex'}),
            dbc.Col([
                     dcc.Dropdown(
                                id='drop2_a',
                                options=newoptions, # only including actual variables
                                value=newoptions[0]['value'],  # set default as first in array 
                         style = style_dropdown),
                    html.H3('and ', style  = {'color': colors['H3']}),
                     dcc.Dropdown(
                        id='drop2_b',
                        options=newoptions, # only including actual variables
                        value=newoptions[1]['value'],  # set default as second in array 
                        style =style_dropdown)], 
                    style={'display':'flex'}),
            html.Iframe(
                id='plot2',
                style = style_plot2)
        ]),  
        ### PLOT 1 LAYOUT ###
        dbc.Col([
            dbc.Col([
                html.H3('Rank Cities by:', style = style_H3), 
                ### DROPDOWN 1 ###
                dcc.Dropdown(
                    id='drop1',
                    placeholder="Variables",
                    options=newoptions, # only including actual variables
                    value=newoptions[0]['value'],  # set default as first in array
                    style = style_dropdown),
                    ], 
                style = {'display': 'flex'}),
            html.H3('Cities to Highlight:', style = style_H3),
            dcc.Dropdown(
                        id='drop3_b',
                        value=['Vancouver', 'Toronto'], 
                        options=[{'label': cities, 'value': cities} for cities in df['city']], multi = True,
                        style=style_dropdown_c),
            html.Iframe(
                    id='plot1',
                    style = style_plot1)], 
            style={"height": "10%", 'border': '1px solid #d3d3d3'})
        ])
        
], 
    fluid=True)

#------------------------------------------------------------------------------
### CALLBACK GRAPHS AND CHECKBOXES ###
#------------------------------------------------------------------------------
### PROVINCE CHECKBOXES ###
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

### CATEGORY CHECKBOXES ###
@app.callback(
        Output("drop1", "value"),
        Output("drop2_a", "value"),
        Output("drop2_b", "value"),
        Output("drop1", "options"),
        Output("drop2_a", "options"),
        Output("drop2_b", "options"),
        Input("category_checklist", "value"),
)
def update_dropdowns(categories):
    newoptions = [{'label': new_name_dic[col], 'value': col} for col in col_filter(categories)[4:]]
    return newoptions[0]['value'],newoptions[0]['value'],newoptions[1]['value'], newoptions, newoptions, newoptions


### PLOT 1: BARGRAPH ###
@app.callback(
        Output('plot1', 'srcDoc'),
        Output('drop3_b', 'options'),
        Input('prov_checklist', 'value'),
        Input('population','value'),
        Input('drop1','value'),
        Input('drop3_b', 'value'),
)
def plot_altair1(prov_chosen, population_chosen, drop1_chosen, drop_b):
    # filtering df
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    dff = dff[dff['province'].isin(prov_chosen)]

    # setting filtered dropdown options
    prov_cities = [{'label': cities, 'value': cities} for cities in dff['city']]

    barchart = alt.Chart(dff[dff[drop1_chosen]>0]).mark_bar().encode(
    alt.X(drop1_chosen, title='Cost of '+new_name_dic[drop1_chosen], axis=alt.Axis(orient='top',format='$.0f')),
    alt.Y('city', sort='x', title=""),
    color = alt.condition(alt.FieldOneOfPredicate(field='city', oneOf=drop_b),
                              alt.value(colors['teal']),
                              alt.value(colors['H2'])),
    tooltip=[drop1_chosen,'province']).configure_axis(labelFontSize = 16, titleFontSize=20)
    return barchart.to_html(), prov_cities


### PLOT 2: SCATTERPLOT ###
@app.callback(
        Output('plot2', 'srcDoc'),
        Input('prov_checklist', 'value'),
        Input('population','value'),
        Input('drop2_a', 'value'),
        Input('drop2_b', 'value'),
        Input('drop3_b', 'value'),
)
def plot_altair2(prov_chosen, population_chosen, drop_a, drop_b, drop_c):
    # filtering df
    popmin = population_chosen[0]
    popmax = population_chosen[1]
    dff = df[df['population'].between(popmin, popmax)]
    dff = dff[dff['province'].isin(prov_chosen)]


    # plot chart
    chart = alt.Chart(dff[(dff[drop_a]>0)&dff[drop_b]>0]).mark_circle(size=75).encode(
        x= alt.X(drop_a, axis=alt.Axis(format='$.0f'), title=new_name_dic[drop_a]),
        y=alt.Y(drop_b, axis=alt.Axis(format='$.0f'), title=new_name_dic[drop_b]),
        color = alt.condition(alt.FieldOneOfPredicate(field='city', oneOf=drop_c),
                              alt.value('teal'),
                              alt.value(colors['H2'])),
        tooltip=['city','province', drop_a, drop_b]
    ).configure_axis(labelFontSize = 16, titleFontSize=20)
    return chart.to_html()


### PLOT 3: Canada Map ###
@app.callback(
        Output('plot_map', 'srcDoc'),
        Input('prov_checklist', 'value')
)
def plot_altair_map(prov_chosen):
    chosen_province_data = {}
    json_list = []

    for feature in canada_province["features"]:

        if feature["properties"]["prov_name_en"] in prov_chosen:
            #print(feature["properties"]["prov_name_en"])
            json_list.append(feature)
        else:
            pass

    chosen_province_data["features"] = json_list
    data_geojson_chosen = alt.InlineData(values=chosen_province_data, format=alt.DataFormat(property='features',type='json'))
    
    color=alt.Color('properties.prov_name_en:N',
                       scale=alt.Scale(
                domain=['Alberta',
                         'Yukon',
                         'Manitoba',
                         'Saskatchewan',
                         'Northwest Territories',
                         'Prince Edward Island',
                         'Nova Scotia',
                         'Quebec',
                         'Nunavut',
                         'Ontario',
                         'British Columbia',
                         'Newfoundland and Labrador',
                         'New Brunswick'],
                range=['#FF6666',
                         '#FF9966',
                         '#FFFF00',
                         '#99CC99',
                         '#339999',
                         '#003366',
                         '#990066',
                         '#CCCC99',
                         '#FFCCCC',
                         '#FFCC99',
                         '#CC99CC',
                         '#CCFF99',
                         '#CC9933']))
    
    c_map = alt.Chart(data_geojson).mark_geoshape(
                ).encode(
                    color = alt.value('lightgray'),
                    tooltip = 'properties.prov_name_en:N'
                ).project(
                    type='identity', reflectY=True)#.add_selection(selection) #.transform_filter(selection)

    filter_p = alt.Chart(data_geojson_chosen).mark_geoshape(
                ).encode(
                    color = color,
                    tooltip = 'properties.prov_name_en:N'
                ).project(
                    type='identity', reflectY=True)
    
    chart = c_map + filter_p
    chart.configure_legend(titleFontSize=26)  # not working

#     # plot chart
#     selection = alt.selection_multi(fields=['properties.prov_name_en'])
#     color = alt.condition(selection,
#                       alt.Color('properties.prov_name_en:N', legend=None),
#                       alt.value('lightgray'))
    
#     base = alt.Chart(data_geojson).mark_geoshape(
#     ).encode(
#     color = color,
#     tooltip = 'properties.prov_name_en:N'
#     ).project(
#     type='identity', reflectY=True)

#     filter_p = alt.Chart(data_geojson).mark_geoshape(
#     ).encode(
#     color = color,
#     tooltip = 'properties.prov_name_en:N'
#     ).project(
#     type='identity', reflectY=True).add_selection(selection).transform_filter(selection)


#     chart = base + filter_p
    
    return chart.to_html()



#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)