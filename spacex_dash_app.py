# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(max_payload)
print(min_payload)

df_scatter = spacex_df[["Launch Site","Payload Mass (kg)","Booster Version","class"]]
sites = spacex_df["Launch Site"].unique()
df_pie_all = spacex_df[["Launch Site","class"]].groupby("Launch Site").mean().reset_index()
df_pie = spacex_df[["Launch Site","class"]]



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 
                                               'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                            options = [{'label': 'All Sites', 'value': 'ALL'}]
                                                        +[{'label': site, 'value': site} for site in sites],
                                            placeholder = "Select a Launch Site",
                                            searchable = True)),
                                
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0,max=10000, step=1000,
                                                marks = {number:str(number) for number in range(0,11000,1000)},
                                                value = [min_payload, max_payload],id='payload-slider',
                                                allowCross=False),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == None:
        return "Select a site"
    elif entered_site == 'ALL':
        fig = px.pie(df_pie_all, 
                       values = 'class',
                       names = "Launch Site", 
                       title = "Total Success Launches By Site")
        return fig
    else:
        data = df_pie[df_pie["Launch Site"]==str(entered_site)]
        data = data.groupby("class").count().reset_index()
        print(data)
        fig = px.pie(data, 
                    values = 'Launch Site',
                    names = "class", 
                    title = f'Total Success for site {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id = 'site-dropdown', component_property='value'),
              [Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site,payload_range):
    if entered_site == None:
        return "Select a site"
    elif entered_site == 'ALL':
        fig = px.scatter(df_scatter, 
                       x = 'Payload Mass (kg)',
                       y = 'class',
                       hover_name ="Booster Version",
                       color ="Booster Version",
                       title = "Total Success Launches By Site",
                       range_x=payload_range)
        return fig
    
    else:
        data = df_scatter[df_scatter["Launch Site"]==str(entered_site)]
        fig = px.scatter(data, 
                       x = 'Payload Mass (kg)',
                       y = 'class',
                       hover_name ="Booster Version",
                       color ="Booster Version",
                       title = f"Total Success Launches By Site - {entered_site}",
                       range_x=payload_range)

        return fig
#Function decorator to specify function input and output


# Run the app
if __name__ == '__main__':
    app.run_server()