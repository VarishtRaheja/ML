# Importing requried libraries
import requests
from io import StringIO
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Loading the dataset
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
text = StringIO(requests.get(url).text)
df = pd.read_csv(text)

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a year list
year = [yr for yr in np.arange(min(df["Year"]),max(df["Year"])+2,1)]

# Creating the web app
app.layout = html.Div([
    # Creating title of dashboard
    html.H1("Automobile Sales Statistics Dashboard",style={"fontSize":24,"color":"#503D36","textAlign":"center"}),
    html.Br(),
    # Creating the dropdown boxes
    html.Div([
        html.Label("Select Statistics: ",style={"fontSize":20,"color":"#2D1503","width":"80%","margin-right":"2em"}),
        html.Br(),
        dcc.Dropdown(id="dropdown-statistics",
                     options=[{"label":"Yearly Statistics","value":"Yearly-Statistics"},
                              {"label":"Recession Period Statistics","value":"Recession-Period-Statistics"}],
                     placeholder="Select a report type",
                     value="Select-Statistics",
                     style={"textSize":16,"color":"#4E2315","width":"60%","textAlignLast": "center"})
    ]),
    html.Div([
        dcc.Dropdown(id="select-year",
                     options=[{'label': i, 'value': i} for i in year],
                     placeholder="Select a year",
                     value="Select-year",
                     style={"textSize":12,"color":"#4E2315","width":"35%","textAlignLast": "center"})
    ]),
    html.Hr(),
    html.Div([
        html.Div(id="output-container",className="chart-grid",
                 style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
    ]), 
])
# {"display": "grid",
#                                                                      "gridTemplateColumns": "repeat(2, 1fr)",
#                                                                      "gridGap": "20px",
#                                                                      "padding": "10px"
#                                                                      }

# Creating the callbacks
# Callback function to enable/disable the year selection.
@app.callback(Output(component_id="select-year",component_property="disabled"),
              Input(component_id="dropdown-statistics",component_property="value"))
def update_input_container(value):
    if value == "Yearly-Statistics":
        return False
    else:
        return True
    
# Define the callback function to update the input container based on the selected statistics
@app.callback(Output(component_id="output-container",component_property="children"),
              [Input(component_id="dropdown-statistics",component_property="value"),
               Input(component_id="select-year",component_property="value")])
def update_output_containter(value,entered_year):
    """
    Generates and returns the appropriate charts based on the selected report type and year.
    """
    if df.empty:
        return html.Div("Data could not be loaded.", style={'textAlign': 'center', 'fontSize': 20})
    # For recession period
    if value == "Recession-Period-Statistics":
        recession_data = df[df["Recession"]==1]
        
        # Create and display graphs for Recession Report Statistics
        #Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
         # grouping data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        
        # Plotting the graph
        R1_chart = dcc.Graph(
            figure=go.Figure(px.line(yearly_rec,x="Year",y="Automobile_Sales",
                                          markers=True,
                                          title="Average Automobile Sales fluctuation over Recession Period",
                                          labels={"Automobile_Sales":"Avg. Automobile Sales"}
                                          )
                             ),style={'width': '100%', 'height': '100%'}
        )
        
        #Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_vehicle_types = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        R2_chart = dcc.Graph(
            figure=go.Figure(
                px.bar(avg_vehicle_types,x="Vehicle_Type",y="Automobile_Sales",
                       color="Vehicle_Type",
                       title="Average number of vehicles sold by Vehicle Type",
                       labels={"Automobile_Sales":"Automobile Sales","Vehicle_Type":"Vehicle Type"})
                ),style={'width': '100%', 'height': '100%'}
        ) 
        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        total_expenditure_recc = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        R3_chart = dcc.Graph(
            figure=go.Figure(
                px.pie(total_expenditure_recc,
                       names="Vehicle_Type",
                       values="Advertising_Expenditure",
                       title="Total expenditure share by vehicle type during the Recession period",
                       labels={"Advertising_Expenditure":"Total Advertising Expenditure","Vehicle_Type":"Vehicle Type"}
                       )
            ),style={'width': '100%', 'height': '100%'}
        )
        # Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemploment_recc = recession_data.groupby(["unemployment_rate","Vehicle_Type"])["Automobile_Sales"].mean().reset_index()
        R4_chart = dcc.Graph(
            figure=go.Figure(
                px.bar(unemploment_recc,
                       x="unemployment_rate",
                       y="Automobile_Sales",
                       color="Vehicle_Type",
                       title="Effect of Unemployment Rate on Vehicle Type and Sales",
                       labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'}
                       )
            ),style={'width': '100%', 'height': '100%'}
        )
        
        # Output all the chart values
        return [
            html.Div(className="chart-item",children=[
            html.Div(R1_chart),html.Div(R2_chart)],style={"display":"flex",'width': '100%'}),
            
            html.Div(className="chart-item",children=[
            html.Div(R3_chart),html.Div(R4_chart)],style={"display":"flex",'width': '100%'})
            ]
            
            # html.Div(R3_chart, style={"width":"100%"}),
            # html.Div(R4_chart, style={"width":"100%"})
            # ]

        
    # Create and display graphs for Yearly Report Statistics
    elif value == "Yearly-Statistics":
        if isinstance(entered_year,int):
            yearly_data = df[df["Year"]==entered_year]
            
            # Plot 1: Monthly Consumer Confidence Fluctuation for the selected year
            monthly_confidence = yearly_data.groupby('Month')['Consumer_Confidence'].mean().reset_index()
            Y1_chart = dcc.Graph(
                figure=px.line(monthly_confidence,
                               x='Month',
                               y='Consumer_Confidence',
                               markers=True,
                               title=f"Consumer Confidence Fluctuation in {entered_year}",
                               labels={'Consumer_Confidence': 'Consumer Confidence', 'Month': 'Month'})
            )
            
            # Plot 2 :Total Monthly Automobile sales using line chart.
            monthly_automobile_sales = yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
            Y2_chart = dcc.Graph(
                figure=go.Figure(
                    px.line(monthly_automobile_sales,x="Month",y="Automobile_Sales",
                            title="Total Monthly Automobile Sales for the year {}".format(entered_year),
                            labels={"Automobile_Sales":"Total Automobile Sales"},
                            markers=True
                            )
                ),style={'width': '100%', 'height': '100%'}
            )
            # Plot 3: bar chart for average number of vehicles sold during the given year
            no_of_vehicles = yearly_data.groupby(["Vehicle_Type"])["Automobile_Sales"].mean().reset_index()
            Y3_chart = dcc.Graph(
                figure=go.Figure(
                    px.bar(no_of_vehicles,x="Vehicle_Type",y="Automobile_Sales",
                        color="Vehicle_Type",
                            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(entered_year),
                            labels={"Automobile_Sales":"Average Vehicle Sales","Vehicle_Type":"Type of Vehicle"}
                            )
                ),style={'width': '100%', 'height': '100%'}
            )
            # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
            expenditure_data = yearly_data.groupby('Vehicle_Type')["Advertising_Expenditure"].sum().reset_index()
            Y4_chart = dcc.Graph(
                figure=go.Figure(
                    px.pie(expenditure_data,
                        names="Vehicle_Type",
                        values="Advertising_Expenditure",
                        title="Total Advertisement Expenditure for each Type of Vehicle in the year {}".format(entered_year),
                        labels={"Vehicle_Type":"Types of Vehicles", 
                                "Advertising_Expenditure":"Expenditure Spent on Advertisement"}
                        )
                ),style={'width': '100%', 'height': '100%'}
            )
            
            return [
                html.Div(className="chart-item",children=[
                    html.Div(Y1_chart),html.Div(Y2_chart)],style={"display":"flex",'width': '100%'}),
                
                html.Div(className="chart-item",children=[
                    html.Div(Y3_chart),html.Div(Y4_chart)],style={"display":"flex",'width': '100%'})
            ]
        else:
            # Group data by year for the whole period
            yearly_sales_all = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
            # Create the line chart
            Y_chart_overall = dcc.Graph(
                figure=px.line(
                    yearly_sales_all,
                    x='Year',
                    y='Automobile_Sales',
                    markers=True,
                    title="Average Yearly Automobile Sales (Overall Period)",
                    labels={'Automobile_Sales': 'Average Automobile Sales', 'Year': 'Year'}
                )
            )
            # Return the single chart
            return [html.Div(Y_chart_overall, style={'width': '100%'})]
    
    
    else:
        return None
 
       
# Running the app
if __name__=="__main__":
    app.run(debug=True)