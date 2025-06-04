# Import required libraries

import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('./airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

# Creating the dash application frontend
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Flight Details Statistics Dashboard",style={"textAlign":"center","color":"#503D36","fontSize":30}),
    html.Div(["Input year: ",dcc.Input(id="input-yr",value=2010,type="number",min=2010,max=2020,
                                       style={"height":"35px","fontSize":20})],
             style={"fontSize":26}),
    html.Br(),
    html.Br(),
    html.Div([html.Div(dcc.Graph(id="carrier-plot")),html.Div(dcc.Graph(id="weather-plot"))],
             style={"display":"flex"}),
    html.Br(),
    html.Br(),
    html.Div([html.Div(dcc.Graph(id="nas-plot")), html.Div(dcc.Graph(id="security-plot"))], style={"display": "flex"}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id="late-plot"), style={'width':'70%'}),
])

def carrier_info(airline_data, entered_year):
    """
    This function takes in airline data and selected year as an input and performs computation for creating charts and plots.
    :param airline_data:
    :param entered_year:
    :return: Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.
    """
    df = airline_data[airline_data["Year"]==int(entered_year)]
    carrier_plot = df.groupby(["Month","Reporting_Airline"])["CarrierDelay"].mean().reset_index()
    weather_plot = df.groupby(["Month", "Reporting_Airline"])["WeatherDelay"].mean().reset_index()
    nas_plot = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    sec_plot = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    late_plot = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    # returning the avg dataframes.
    return carrier_plot,weather_plot,nas_plot,sec_plot,late_plot

# Add the callback decorator for interactivity.
@app.callback([Output(component_id="carrier-plot",component_property="figure"),
               Output(component_id="weather-plot",component_property="figure"),
               Output(component_id="nas-plot",component_property="figure"),
               Output(component_id="security-plot",component_property="figure"),
               Output(component_id="late-plot",component_property="figure")],
              Input(component_id="input-yr",component_property="value"))
def get_graph(entered_year):
    # Compute required information for creating graph from the data
    carrier_plot,weather_plot,nas_plot,sec_plot,late_plot = carrier_info(airline_data, entered_year)
    # Line plot for carrier delay
    carrier_fig = go.Figure(px.line(data_frame=carrier_plot,x="Month",y="CarrierDelay",color="Reporting_Airline",markers=True,
                            title="Average carrier delay time (minutes) by airline",
                            labels={"CarrierDelay":"Carrier Delay","Reporting_Airline":"Airline"},width=750))
    # Line plot for weather delay
    weather_fig = go.Figure(px.line(data_frame=weather_plot,x="Month",y="WeatherDelay",color="Reporting_Airline",markers=True,
                            title="Average weather delay time (minutes) by airline",
                            labels={"WeatherDelay":"Weather Delay","Reporting_Airline":"Airline"},width=750))
    # Line plot for nas delay
    nas_fig = go.Figure(px.line(data_frame=nas_plot,x="Month",y="NASDelay",color="Reporting_Airline",markers=True,
                            title="Average NAS delay time (minutes) by airline",
                            labels={"NASDelay":"NAS Delay","Reporting_Airline":"Airline"},width=750))
    # Line plot for security delay
    sec_fig = go.Figure(px.line(data_frame=sec_plot,x="Month",y="SecurityDelay",color="Reporting_Airline",markers=True,
                            title="Average security delay time (minutes) by airline",
                            labels={"SecurityDelay":"Security Delay","Reporting_Airline":"Airline"},width=750))
    # Line plot for late aircraft delay
    late_fig = go.Figure(px.line(data_frame=late_plot,x="Month",y="LateAircraftDelay",color="Reporting_Airline",markers=True,
                            title="Average late aircraft delay time (minutes) by airline",
                            labels={"LateAircraftDelay":"Late Aircraft Delay","Reporting_Airline":"Airline"}))

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]
if __name__=="__main__":
    app.run(debug=True)