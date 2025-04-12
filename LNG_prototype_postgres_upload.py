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

def format_duration(minutes):
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        return f"{hours}h {remaining_minutes}m"


def upload_excel_to_postgres(excel_file_path, table_name, dbname, user, password, host, port):

    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)
        df.loc[1, 'Completed'] = pd.to_datetime(df.loc[1, 'Completed'])
        operation_date = df.loc[1, 'Completed']
        df['operation_date'] = operation_date

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Iterate through the DataFrame rows and insert into the table
        for index, row in df.iterrows():
            ship_type = row['ship_type']
            operation_date = row['operation_date']
            activity = row['Activity']
            duration_str = row['Duration']

            # Check if duration is not empty
            if pd.notna(duration_str):
                try:
                    # Convert duration string to INTERVAL format
                    hours, minutes, seconds = map(int, duration_str.split(':'))
                    duration = f'{hours:02d}:{minutes:02d}:{seconds:02d}'

                    # Create the SQL INSERT statement
                    sql = """
                        INSERT INTO ship_operations (ship_name, operation_date, activity, duration)
                        VALUES (%s, %s, %s, %s::INTERVAL)
                    """

                    # Execute the SQL statement with the row values
                    cur.execute(sql, (ship_type, operation_date, activity, duration))

                except ValueError:
                    print(f"Skipping row {index + 1} due to invalid duration format: {duration_str}")
            else:
                print(f"Skipping row {index + 1} due to missing or zero duration.")

        conn.commit()

        print(f"Data from '{excel_file_path}' uploaded successfully to table '{table_name}' for ship '{ship_type}' and date '{operation_date}'.")
        
        pre_bunkering = ['NOR tendered by LBV','NOR tendered by RV','Mooring','Gangway landed','Hose(s) or arm connection','Hose(s) or arm pressure tested','Hose(s) or arm purged with N2','Pre-operations meeting', 'WarmESD','Opening CTS', 'Hose(s) or arm and lines cool-dow', 'Cold ESD tests', 'Open BOG valve to shore', 'Ramp-up bunker transfer']
        post_bunkering = ['Draining of hose(s) or arm', 'Close BOG valve to shore', 'Hose(s) or arm purged','Closing CTS', 'Post operation meeting', 'Hose(s) or arm disconnected', 'Documentation completed', 'IAPH checklist part E','Pilot on board', 'Unmooring']

        pre_bunkering_placeholders = ', '.join(['%s'] * len(pre_bunkering))
        post_bunkering_placeholders = ', '.join(['%s'] * len(post_bunkering))
        sql = f"""
            SELECT SUM(duration)
            FROM ship_operations
            WHERE ship_name = %s
                AND operation_date = %s
                AND activity IN ({pre_bunkering_placeholders});
        """

        # Prepare the values for the query
        values = [ship_type, operation_date ] + pre_bunkering

        # Execute the SQL query
        cur.execute(sql, values)
        pre_bunkering_time = cur.fetchone()
        pre_bunkering_time = pre_bunkering_time[0] if pre_bunkering_time and pre_bunkering_time[0] is not None else timedelta(seconds=0)
        pre_bunkering_time = pre_bunkering_time.total_seconds() / 60

        sql = f"""
            SELECT SUM(duration)
            FROM ship_operations
            WHERE ship_name = %s
                AND operation_date = %s
                AND activity IN ({post_bunkering_placeholders});
        """

        # Prepare the values for the query
        values = [ship_type, operation_date ] + post_bunkering

        # Execute the SQL query
        cur.execute(sql, values)
        post_bunkering_time = cur.fetchone()
        post_bunkering_time = post_bunkering_time[0] if post_bunkering_time and post_bunkering_time[0] is not None else timedelta(seconds=0)
        post_bunkering_time = post_bunkering_time.total_seconds() / 60
        cur.close()
        conn.close()

        labels = ["Pre-Bunkering", "Post-Bunkering"]
        values = [pre_bunkering_time, post_bunkering_time]
        colors = ['skyblue', 'lightcoral']
        hover_texts = [format_duration(val) for val in values]

        fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=colors,
                                 hovertemplate='%{x}: %{y:.2f} minutes (%{text})<extra></extra>',
                                 text=hover_texts)])

        fig.update_layout(title="Pre-VS-Post",
                      yaxis_title="Duration (Minutes)")

        return fig
               
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

table_name = "ship_operations"  # Replace with your table name
dbname = "FueLNG"  # Replace with your database name
user = "postgres"        # Replace with your PostgreSQL username
password = "postgres"    # Replace with your PostgreSQL password
host = "localhost"            # Replace with your PostgreSQL host
port = "5432"                # Replace with your PostgreSQL port
excel_path = "./SOF_excel/SOF_Document_1/SOF_Document_1.xlsx"

fig = upload_excel_to_postgres(excel_path, table_name, dbname, user, password, host, port)
