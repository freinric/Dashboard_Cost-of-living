from dash import Dash, dcc, html, Input, Output, State, callback_context
import pandas as pd


df = pd.read_csv("data_extra.csv") 

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
 
options = [x for x in df['province'].unique()]
#options = ["New York City", "Montréal", "San Francisco"]

app.layout = html.Div(
    [
        dcc.Checklist(["All"], [], id="all-checklist", inline=True),
        dcc.Checklist(options, [], id="prov-checklist", inline=True),
    ]
)
@app.callback(
    Output("prov-checklist", "value"),
    Output("all-checklist", "value"),
    Input("prov-checklist", "value"),
    Input("all-checklist", "value"),
)
def sync_checklists(cities_selected, all_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "prov-checklist":
        all_selected = ["All"] if set(cities_selected) == set(options) else []
    else:
        cities_selected = options if all_selected else []
    return cities_selected, all_selected

if __name__ == "__main__":
    app.run_server(debug=True)
