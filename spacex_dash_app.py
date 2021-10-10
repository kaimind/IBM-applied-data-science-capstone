# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    dcc.Dropdown(id='site-dropdown',
                                                 # Update dropdown values using list comphrehension
                                                 options=[{'label': 'All Sites', 'value': 'All Sites'}, {
                                                     'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {
                                                     'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, {
                                                     'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, {
                                                     'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                                 value = "All Sites",
                                                 placeholder="Select a report type",
                                                 style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
                                ], style={'display': 'flex'}),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                dcc.Graph(id="success-pie-chart"),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min=0,
                                        max=10000,
                                        value=[10000],
                                        marks={
                                            0: {'label': '0'},
                                            2500: {'label': '2500'},
                                            5000: {'label': '5000'},
                                            7500: {'label': '7500'},
                                            10000: {'label': '10000'}
                                        }
                                    ),
                                ], style={'width': '80%'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                dcc.Graph(id="success-payload-scatter-chart"),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    [Output("success-pie-chart", "figure"),
     Output("success-payload-scatter-chart", "figure")],
    [Input("site-dropdown", "value"),
     Input("payload-slider", "value")])
def generate_chart(site, payload):
    s = {"CCAFS LC-40": 0, "VAFB SLC-4E": 0,
         "KSC LC-39A": 0, "CCAFS SLC-40": 0}
    f = {"CCAFS LC-40": 0, "VAFB SLC-4E": 0,
         "KSC LC-39A": 0, "CCAFS SLC-40": 0}
    for i, r in spacex_df.iterrows():
        if r["class"] == 0:
            f[r["Launch Site"]] += 1
        else:
            s[r["Launch Site"]] += 1

    print(site)
    if site is None or site == "All Sites":
        sites = []
        c = []
        for k, v in s.items():
            sites.append(k)
            c.append(v)

        d = {"sites": sites, "class": c}
        temp_df = pd.DataFrame(data=d)
        pie_fig = px.pie(temp_df, values='class', names="sites")
    else:
        v = []
        v.append(s[site])
        v.append(f[site])
        temp_df = pd.DataFrame(data={"v":v, "name":["Success","Fail"]})
        pie_fig = px.pie(temp_df, values='v', names="name")

    temp_df = spacex_df[spacex_df['Payload Mass (kg)'] < payload[0]]
    scatter_fig = px.scatter(temp_df, x="Payload Mass (kg)", y="class")

    return [pie_fig, scatter_fig]


# Run the app
if __name__ == '__main__':
    app.run_server()
