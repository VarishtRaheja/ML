# Import required packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from airline_analysis import create_plot

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('./airlines-dash.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1("Airline Dashboard",style={"textAlign":"center","color":"#503D36","font-size":40}),
                                html.P("Proportion of distance group (250 mile distance interval group) by flights.",
                                       style={"textAlign":"center","color":"#F57241","font-size":"20"}),
                                dcc.Graph(figure=fig), dcc.Graph(figure=create_plot()),
                                html.Br(),
                                html.Br(),
                                html.H1("Flight Delay Time statistics ", style={"textAlign":"center","color":"#22120C"
                                                                                ,"font-size":35}),
                                html.Div(["Input Year: ",dcc.Input(id='input-yr',value=2010,type="number",
                                                                   style={'height':'50px', 'font-size': 16}),],
                                         style={'font-size': 20}),
                                html.Br(),       
                                html.Br(),
                                html.Div(dcc.Graph(id="line-plot")),
                                html.Br(),
                                html.Br(),
                                html.Div(["Input Year: ",dcc.Input(id='bar-input-yr',value=2010,type="number",
                                                                   style={'height':'50px', 'font-size': 18}),],
                                         style={'font-size': 20}),
                                html.Div(dcc.Graph(id="bar-plot")),
                                ])
# add the callback decorator
@app.callback(Output(component_id="line-plot",component_property="figure")
              ,Input(component_id="input-yr",component_property="value"))

# Add computation to callback and return graph
def interactive_graph(entered_year):
       df = airline_data[airline_data["Year"] == int(entered_year)]
       # Group the data based on mean
       line_data = df.groupby("Month")["ArrDelay"].mean().reset_index()
       # Create the figure
       fig = go.Figure()
       fig.add_trace(go.Scatter(x=line_data["Month"],y=line_data["ArrDelay"],mode="lines",marker=dict(color="darkblue")))
       # Update the axes and title
       fig.update_layout(title="Trend depicting delay in flight time over the years",xaxis_title="Month",yaxis_title="Arrival Delay Time")
       return fig

# Callback function for bar-plot id
@app.callback(Output(component_id="bar-plot",component_property="figure")
              ,Input(component_id="bar-input-yr",component_property="value"))
# Function returning figure for bar chart.
def bar_interactive_graph(entered_year):
       df = airline_data[airline_data["Year"] == int(entered_year)]
       # Group the data based on mean
       bar_data = df.groupby("DestState")["Flights"].sum().reset_index()
       # Create the figure
       fig = go.Figure()
       fig.add_trace(go.Bar(x=bar_data["DestState"],y=bar_data["Flights"],marker=dict(color="darkblue")))
       # Update the axes and title
       fig.update_layout(title="Total number of flights to the destination state",xaxis_title="Destination State",
                         yaxis_title="Number of Flights")
       return fig

# Run the application                   
if __name__ == '__main__':
    app.run()
    
