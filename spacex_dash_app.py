# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Get the unique launch sites for the dropdown options
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
                    # Dropdown for Launch Site selection
                    dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'}
                                ] + [{'label': site, 'value': site} for site in launch_sites],
                                value='ALL',  # default value
                                placeholder="Select a Launch Site",
                                searchable=True
                                ),
                    
                    html.Br(),

                                # TASK 2: Pie chart for success counts
                    html.Div(dcc.Graph(id='success-pie-chart')),
                    html.Br(),

                    html.P("Payload range (Kg):"),
                    
                    # TASK 3: Slider to select payload range
                    dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value=[0, 10000]),
                    html.Br(),

                    # TASK 4: Scatter chart for payload vs success
                    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                ])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Create a pie chart showing the total success launches by all sites
        fig = px.pie(spacex_df, names='Launch Site', values='class', 
                     title='Total Success Launches by All Sites')
    else:
        # Filter the dataframe based on the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Create a pie chart for the success vs failed count for the selected site
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failure for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    
    if selected_site == 'ALL':
        # If 'ALL' sites are selected, show the scatter plot for all sites
        filtered_df = spacex_df[mask]
    else:
        # Filter based on the selected site and payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & mask]
    
    # Create a scatter plot with Payload Mass (kg) vs. class (launch success)
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', 
                     title=f'Payload vs. Success for {selected_site}' if selected_site != 'ALL' else 'Payload vs. Success for All Sites')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
