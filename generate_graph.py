import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

def get_graph_title(data):
    subplot_titles = {}
    main_title = ""
    for element in data:
        vessel_name = list(element.keys())[0]
        year = element[vessel_name]
        # Format the main title
        main_title += f"{vessel_name}, {year} & "
    
    # Remove "& " at the end
    main_title = main_title[:-3]

    return main_title

def generate_overall_graph(data, category=["pre-bunkering", "post-bunkering", "post-bunkering with waiting time"]):
    # Analyse data for title
    main_title = get_graph_title(data)

    # Create subplots
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        # Create a legend name where it's Vessel year
        vessel_name = list(element.keys())[0]
        year = element[vessel_name]
        legend = str(vessel_name) + " " + str(year)
        fig.add_trace(go.Bar(x=category, y=element["Value_Overall"], name=legend, 
                             text=element["Value_Overall"], textposition="auto"), # Adds display value
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Overall (average) performance for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig


def generate_totaltime_graph(data, category=["pre-bunkering", "post-bunkering", "post-bunkering with waiting time"]):
    # Analyse data for title
    main_title = get_graph_title(data)

    # Create subplots
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        # Create a legend name where it's Vessel year
        vessel_name = list(element.keys())[0]
        year = element[vessel_name]
        legend = str(vessel_name) + " " + str(year)
        fig.add_trace(go.Bar(x=[element[vessel_name]], y=element["Value_Totaltime"], name=legend, 
                             text=element["Value_Totaltime"], textposition="auto"), # Adds display value
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Average time taken for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig


def generate_tasktime_graph(data, category=["Berthing & Mooring", "Hose Connection", "Purging, Warm ESD", "Line cool down, Cold ESD", "Ramping down", "Draining", "Purging", "Hose disconnection", "Documentation", "Unmooring"]):
    # Analyse data for title
    main_title = get_graph_title(data)

    # Create subplots
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        # Create a legend name where it's Vessel year
        vessel_name = list(element.keys())[0]
        year = element[vessel_name]
        legend = str(vessel_name) + " " + str(year)
        fig.add_trace(go.Bar(x=category, y=element["Value_Tasktime"], name=legend, 
                             text=element["Value_Tasktime"], textposition="auto"), # Adds display value
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Average time taken for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig