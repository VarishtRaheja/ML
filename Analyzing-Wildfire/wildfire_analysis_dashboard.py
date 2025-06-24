# Importing the required libs
from io import StringIO
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import datetime as dt

# Getting the csv data
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
data = StringIO(requests.get(URL).text)
df = pd.read_csv(data)

# Create a function rename the regions
def rename_regions():
    curr_regions = [r for r in df["Region"].unique()]
    region_remapping = [
                        {"label":"New South Wales","value": str(curr_regions[0])},
                        {"label":"Northern Territory","value": str(curr_regions[1])},
                        {"label":"Queensland","value": str(curr_regions[2])},
                        {"label":"South Australia","value": str(curr_regions[3])},
                        {"label":"Tasmania","value": str(curr_regions[4])},
                        {"label":"Victoria","value": str(curr_regions[5])},
                        {"label":"Western Australia","value": str(curr_regions[6])}
                        ]
    return region_remapping

region_items = rename_regions()

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Create the application
app = Dash(__name__)

app.layout = html.Div(children=[html.H1("Australia Wildlife Dashboard",style={"textAlign":"center","color":"black","fontSize":30}),
                                html.Br(),
                                html.Div([
                                    html.Div([
                                        html.H2("Select Region: ", style={"fontSize": 20, "fontWeight": "bold"}),  # Modify only this text
                                    dcc.RadioItems(region_items,region_items[0]["value"],
                                                   style={"fontSize": 15}, 
                                                   inline=True,id="region-id")])
                                    ]),
                                html.Div([
                                    html.Div([
                                        html.H2("Select year: ",style={"fontSize": 20, "fontWeight": "bold","margin-right":"2em"})
                                    ]),
                                    dcc.Dropdown(df.Year.unique(),id="input-yr",value=2005,style={"fontSize":15})],
                                    style={"fontSize":26}),
                                html.Br(),
                                html.Hr(),
                                html.Div([
                                    html.Div([ ],id="estimated_fire_area_plot"),
                                    html.Div([ ],id="count_bar_plot")],
                                         style={"display":"flex"}),
                                html.Hr()
                                ])

@app.callback([Output(component_id="estimated_fire_area_plot",component_property="children"),
               Output(component_id="count_bar_plot",component_property="children")],
              
              [Input(component_id="region-id",component_property="value"),
               Input(component_id="input-yr",component_property="value")]
              )
def create_plot(region,entered_year):
    """ This function creates and returns the plots from the dataframes filtred by year and region. """

    region_data = df[df["Region"]==region]
    y_r_data = region_data[region_data["Year"]==entered_year]
    
    # Get the average of the monthly fire area and count pixel vegetation fire
    est_data = y_r_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    veg_data = y_r_data.groupby("Month")["Count"].mean().reset_index()
    
    # Creating the visualisations
    estimated_fire_area_fig = go.Figure(px.pie(data_frame=est_data,values="Estimated_fire_area",names='Month',
                                               title="Region {}: Monthly Average Estimated Area in year {}".format(region,entered_year),
                                               ))

    count_of_vegetation_fire_fig = go.Figure(px.bar(data_frame=veg_data,x="Month",y="Count",
                                                    title="Region {}: Average Count of Pixels for presumed Vegetation Fires in year {}"\
                                                        .format(region,entered_year),
                                                    ))
    # Setting the xaxis tick formatting
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    count_of_vegetation_fire_fig.update_layout(
        xaxis=dict(tickmode="array",
                   tickvals=list(np.arange(0,12,1)),
                   ticktext=month_names
                   ),width=800

        )
    
    # returning the figures
    return [dcc.Graph(figure=estimated_fire_area_fig),
            dcc.Graph(figure=count_of_vegetation_fire_fig)]


# running the application
if __name__=="__main__":
    app.run(debug=True)
