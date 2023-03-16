from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('data_extra.csv')

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Cost of Living"),
        html.P("Select your maxiumum population: "),
        dcc.Slider(id="population", min=0, max=4000000, value=0),
        dcc.Graph(id="graph"),
        html.H3(f"Cities with population up to {value}")
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("population", "value"),
)
def display_graph(value):
    dff = df.query(f"population <= {value}")
    fig = px.scatter(dff, 
                    x="meal_cheap", 
                    y="meal_mid",
                    color="province", 
                    hover_name="city",
                    log_x=True, size_max=55
                        )
    fig.update_layout(
        {
            "title": f"Cities with population up to {value}",
            "yaxis": {"title": "Average Meal Price"},
            "xaxis": {"title": "Cheap Meal Price"},
        }
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)