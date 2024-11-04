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

# Create a dash application
app = dash.Dash(__name__)


# Define dropdown options
option_values = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
]


#app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Record Dashboards',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Div([
        "Launch Sites: ",
        dcc.Dropdown(
            id='site-dropdown',
            options=option_values,
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        ),
    ], style={'font-size': 15}),
    dcc.Graph(id="success-pie-chart"),
    html.Div([
        "Payload Range (kg): ",
        #Task 3
        dcc.RangeSlider(
            id='payload-slider',
            min=spacex_df['Payload Mass (kg)'].min(),
            max=spacex_df['Payload Mass (kg)'].max(),
            step=1000,
            value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
            marks={i: str(i) for i in range(0, 10001, 1000)}  # Adjust this as necessary for your data
        )
    ], style={'margin-top': '20px', 'font-size': 20}),
    dcc.Graph(id='success-payload-scatter-chart')  # Placeholder for the scatter plot
])


# TASK 2:
# Define callback to update pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                     names='site', title=f'Launch Success Rate for {entered_site}')
    else:
        filtered_df = filtered_df[filtered_df['site'] == entered_site]
        fig = px.pie(filtered_df, values='class', 
                     names='site', title=f'Launch Success Rate for {entered_site}')

    return fig


# TASK 4:
# Define callback to update scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_plot(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                             (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Outcome for All Sites',
            labels={'class': 'Launch Outcome (1 = Success, 0 = Failure)', 'payload_mass_kg': 'Payload Mass (kg)'}
        )
    else:
        filtered_df = filtered_df[filtered_df['site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Outcome for {selected_site}',
            labels={'class': 'Launch Outcome (1 = Success, 0 = Failure)', 'payload_mass_kg': 'Payload Mass (kg)'}
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
