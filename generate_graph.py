import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

def get_graph_title(data):
    subplot_titles = []
    main_title = ""
    for element in data:
        vessel_name = list(element.keys())[0]
        year = element[vessel_name]
        subplot_titles.append(vessel_name)
        main_title += f"{vessel_name}, {year} & "
    
    # remove "&" at the end
    main_title = main_title[:-2]

    return subplot_titles, main_title

def generate_overall_graph(data, category=["pre-bunkering", "post-bunkering", "post-bunkering with waiting time"]):
    # Analyse data for title
    subplot_titles, main_title = get_graph_title(data)

    # Create subplots
    # fig = make_subplots(rows=1, cols=2, subplot_titles=tuple(subplot_titles)) # two subplot
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        fig.add_trace(go.Bar(x=category, y=element["Value_Overall"], name=subplot_titles[index]),
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Overall (average) performance for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig


def generate_totaltime_graph(data, category=["pre-bunkering", "post-bunkering", "post-bunkering with waiting time"]):
    # Analyse data for title
    subplot_titles, main_title = get_graph_title(data)

    # Create subplots
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        vessel_name = subplot_titles[index]
        fig.add_trace(go.Bar(x=[element[vessel_name]], y=element["Value_Totaltime"], name=vessel_name),
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Average time taken for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig


def generate_tasktime_graph(data, category=["Berthing & Mooring", "Hose Connection", "Purging, Warm ESD", "Line cool down, Cold ESD", "Ramping down", "Draining", "Purging", "Hose disconnection", "Documentation", "Unmooring"]):
    # Analyse data for title
    subplot_titles, main_title = get_graph_title(data)

    # Create subplots
    fig = make_subplots(rows=1, cols=1) # one subplot

    # Create individual graphs
    for index, element in enumerate(data):
        vessel_name = subplot_titles[index]
        fig.add_trace(go.Bar(x=category, y=element["Value_Tasktime"], name=vessel_name),
                    row=1, col=1
        )

    # Update layout
    fig.update_layout(title_text=f"Average time taken for {main_title} per operation")

    # Show the figure
    # fig.show()
    return fig