from click import option
#import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df_nation = pd.read_csv("Data/state_data.csv", thousands = ",")
external_stylesheets = ["https://cdn.jsdelivr.net/npm/halfmoon@1.1.1/css/halfmoon-variables.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cols = ["Intake - Relinquished By Owner Total-Feline","Intake - Stray At Large Total-Feline","Intake - Transferred In Total-Feline","Intake - Owner Intended Euthanasia Total-Feline","Intakes - Other Intakes Total-Feline","Live Outcome - Adoption Total-Feline","Live Outcome - Returned To Owner Total-Feline","Live Outcome - Returned To Field Total-Feline","Live Outcome - Transferred Out Total-Feline","Live outcome - Other Live Outcome Total-Feline","Other Outcome - Died In Care Total-Feline","Other Outcome - Lost In Care Total-Feline","Other Outcome - Owner Intended Euthanasia Total-Feline","Other Outcome - Shelter Euthanasia Total-Feline","Intake - Relinquished By Owner Total-Canine","Intake - Stray At Large Total-Canine","Intake - Transferred In Total-Canine","Intake - Owner Intended Euthanasia Total-Canine","Intakes - Other Intakes Total-Canine","Live Outcome - Adoption Total-Canine","Live Outcome - Returned To Owner Total-Canine","Live Outcome - Returned To Field Total-Canine","Live Outcome - Transferred Out Total-Canine","Live outcome - Other Live Outcome Total-Canine","Other Outcome - Died In Care Total-Canine","Other Outcome - Lost In Care Total-Canine","Other Outcome - Owner Intended Euthanasia Total-Canine","Other Outcome - Shelter Euthanasia Total-Canine"]


#APP LAYOUT------------------------------------------

app.layout = html.Section([
    html.Div([
        html.H1("Data Shelter"),
        dcc.Dropdown(
            id="statistical-dropdown",
            options=[{"label":k, "value":k} for k in cols],
            value = cols[0]
        ),
        html.Div([
            html.Br(),
            dcc.Graph(id='choropleth-map', figure={}),
            dcc.Slider(
                min=2019,
                max=2021,
                step=1,
                value=2019,
                id="year-slider",
                marks={'2019': '2019', '2020': '2020', '2021': "2021"},
            )
        ], style={"width":"50%","float":"left"}),
        html.Div([    
            dcc.Graph(id="bar-graph", figure={})
        ], style={"width":"50%","float":"right"})
    ])
])

@app.callback(
    Output("bar-graph", "figure"),
    [Input("statistical-dropdown", "value"),
    Input("year-slider", "value")]
)
def bar_output(value, year):
    df = df_nation.copy()
    df = df[(df['Year'] == int(year))]
    f = px.bar(
        data_frame=df,
        x="State",
        y=value,
        color=value,
        color_continuous_scale=px.colors.sequential.GnBu,
        hover_data=["State", value],
        template="plotly_white"
    )
    f.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'},title=f"<b>States Ranked: {value}</b>", title_x=0.5)
    return f

@app.callback(
    #Output("container", "children"),
    Output("choropleth-map", "figure"),
    [Input("statistical-dropdown", "value"),
    Input("year-slider", "value")
    ]
)
def choropleth_output(value, year):
    #container = "selected-data: {}".format(value)
    df = df_nation.copy()
    df = df[(df['Year'] == int(year))]
    f = px.choropleth(
        data_frame=df,
        locationmode="USA-states",
        locations="State",
        scope="usa",
        color=value,
        hover_data=["State", value],
        color_continuous_scale=px.colors.sequential.GnBu,
        template="plotly_white"
    )
    f.update_layout(title=f"<b>{value}</b>", title_x=0.5)
    f.update_traces(marker_line_width=0)
    return f#container, f

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)