# Check all packages are successfully isntalled and can be used.
from check_packages_installed import module_check
packages = ["pandas","numpy","dash"]

# Calling the function from a py file
vals = module_check(packages).values()

if all(vals):
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import dash
    from dash import dcc
    from dash import html
    print("All packages are installed")
else:
    mod = [key for key, value in module_check(packages).items() if value is False][0]

    print(f"Module(s) {mod} need to be installed!")
    


# Read the airline data into pandas dataframe
from downloading_data import get_data
filename = get_data('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv')

airline_data =  pd.read_csv(filename,
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

print('Data downloaded and read into a dataframe!')


def create_plot():
    # Creating subplots to add scatter,line and bar plots
    fig = make_subplots(rows=3,cols=1,subplot_titles=("Distance vs Departure Time"
                                                    ,"Month vs Average Flight Delay Time"
                                                    ,"Total number of flights to the destination state split by reporting airline"))

    # Creating scatter plot to depict distance vs departure time.
    fig.add_trace(go.Scatter(x=airline_data.Distance,y=airline_data.DepTime,mode='markers',marker=dict(color="darkblue")),row=1,col=1)

    # Create a line plot to visualise average monthly arrival delay time and its trend.
    df = airline_data.groupby("Month")["ArrDelay"].mean().reset_index()
    fig.add_trace(go.Scatter(x=df["Month"],y=df["ArrDelay"],mode="lines",marker=dict(color="darkgreen")),row=2,col=1)

    # Creating a bar chart
    bar_data = airline_data.groupby("DestState")["Flights"].sum().reset_index()
    fig.add_trace(go.Bar(x=bar_data["DestState"],y=bar_data["Flights"]),row=3,col=1)

    # Creating the xaxis labels
    fig.update_xaxes(title_text="Distance",row=1,col=1)
    fig.update_xaxes(title_text="Month",row=2,col=1)
    fig.update_xaxes(title_text="Destination State",row=3,col=1)

    # Creating the yaxis labels
    fig.update_yaxes(title_text="Departure Time",row=1,col=1)
    fig.update_yaxes(title_text="Arrival Delay",row=2,col=1)
    fig.update_yaxes(title_text="Count",row=3,col=1)

    # Update main title and height
    fig.update_layout(title="Basic charts using plotly for univariate analysis.",height=1000)
    return fig
    # fig.show()

