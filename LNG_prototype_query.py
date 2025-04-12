import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import psycopg2
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import os
import re

def year_timestamps(year):
    try:
        start_of_year = datetime(year, 1, 1, 0, 0, 0)
        end_of_year = datetime(year, 12, 31, 23, 59, 59, 999999)
        return start_of_year, end_of_year
    except ValueError as e:
        print(f"Error: Invalid year provided: {e}")
        return None, None
    
def format_duration_hover(minutes):
    if minutes is None:
        return "0h 0m"
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    return f"{hours} hours {remaining_minutes} minutes"

def plot_bunkering_comparison_explicit(year1, year2,
                                        prebunker_year1_minutes, prebunker_year2_minutes,
                                        postbunker_year1_minutes, postbunker_year2_minutes):
    
    title = title = f"{ship_name} {year1} vs {year2}"
    activities = ["Prebunker", "Postbunker"]
    years = [year1, year2]
    colors = ['forestgreen', 'dodgerblue']

    values_minutes = {
        year1: {"Prebunker": prebunker_year1_minutes, "Postbunker": postbunker_year1_minutes},
        year2: {"Prebunker": prebunker_year2_minutes, "Postbunker": postbunker_year2_minutes},
    }

    fig = go.Figure()

    for i, year in enumerate(years):
        durations_minutes = [values_minutes[year][activity] for activity in activities]
        hover_texts = [format_duration_hover(duration) for duration in durations_minutes]

        fig.add_trace(go.Bar(x=activities,
                             y=durations_minutes,
                             name=str(year),
                             marker_color=colors[i],
                             hovertemplate='%{x}: %{y:.2f} minutes (%{text})<extra></extra>',
                             text=hover_texts))

    fig.update_layout(title=title,
                      yaxis_title="Duration (Minutes)",
                      barmode='group')

    return fig
    
def main_query(start_date, end_date, activities, ship_name, cur):
    placeholders = ', '.join(['%s'] * len(activities))

    sql = f"""
            SELECT COUNT(*), SUM(duration)
            FROM ship_operations
            WHERE ship_name = %s
                AND activity IN ({placeholders})
                AND operation_date >= %s
                AND operation_date < %s;
        """

    cur.execute(sql, [ship_name] + activities + [start_date, end_date])
    number_of_entries, total_sum = cur.fetchone()

    if number_of_entries and total_sum is not None and number_of_entries > 0:
        number_of_operations = number_of_entries / len(activities)
        average_duration = total_sum / number_of_operations
        print(average_duration)
        average_duration = average_duration.total_seconds() / 60
        return average_duration
    else:
        return None

def yearly_average(ship_name, year1, year2, dbname, user, password, host, port):
    start_date1, end_date1 = year_timestamps(year1)
    start_date2, end_date2 = year_timestamps(year2)

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        pre_bunkering_year1 = main_query(start_date1, end_date1,pre_bunkering, ship_name, cur)
        post_bunkering_year1 = main_query(start_date1, end_date1, post_bunkering, ship_name, cur)
        pre_bunkering_year2 = main_query(start_date2, end_date2,pre_bunkering, ship_name, cur)
        post_bunkering_year2 = main_query(start_date2, end_date2, post_bunkering, ship_name, cur)
        cur.close()
        conn.close()

        fig = plot_bunkering_comparison_explicit(year1, year2,
                                        pre_bunkering_year1, pre_bunkering_year2,
                                        post_bunkering_year1, post_bunkering_year2)
        
        return fig

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
        return None
    
pre_bunkering = ['NOR tendered by LBV','NOR tendered by RV','Mooring','Gangway landed','Hose(s) or arm connection','Hose(s) or arm pressure tested','Hose(s) or arm purged with N2','Pre-operations meeting', 'WarmESD','Opening CTS', 'Hose(s) or arm and lines cool-dow', 'Cold ESD tests', 'Open BOG valve to shore', 'Ramp-up bunker transfer']
post_bunkering = ['Draining of hose(s) or arm', 'Close BOG valve to shore', 'Hose(s) or arm purged','Closing CTS', 'Post operation meeting', 'Hose(s) or arm disconnected', 'Documentation completed', 'IAPH checklist part E','Pilot on board', 'Unmooring']
    
dbname = "FueLNG"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"

ship_name = 'VENOSA'
year1 = 2025
year2 = 2024
    
fig = yearly_average(ship_name, year1, year2, dbname, user, password, host, port)
fig.show()