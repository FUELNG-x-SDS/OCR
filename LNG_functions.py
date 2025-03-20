import json
from paddlex import create_pipeline
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import re

def clean_time(time_str):
    if isinstance(time_str, str):
        time_str = time_str.replace(" LT", "").replace("LT", "")
        if len(time_str.split()[1]) == 5:
            return time_str
        else:
            return time_str.split()[0] + " " + time_str.split()[1][:2] + ":" + time_str.split()[1][2:]
    return time_str

def clean_time1(time_str):
    if not isinstance(time_str, str):
        return "0000-00-00 00:00"

    time_str = time_str.replace(" LT", "").replace("LT", "").strip()

    if len(time_str) >= 10 and not time_str[4] == '-':
        time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]

    time_str = re.sub(r'\s+', ' ', time_str)

    if len(time_str) > 10 and not time_str[10] == " ":
        time_str = time_str[:10] + " " + time_str[10:]

    parts = time_str.split()

    if len(parts) >= 2:
        date_part = parts[0]
        time_part = parts[1].replace(" : ", ":").replace(" :", ":").replace(": ", ":")

        if ":" not in time_part and len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return date_part + " " + time_part
        else:
            return date_part + " " + time_part[:2] + ":" + time_part[2:]

    elif len(parts) == 1:
        time_part = parts[0]
        if len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]
        if len(time_part) == 5 and ":" not in time_part:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return "0000-01-01 " + time_part
        else:
            return "0000-01-01 00:00"

    else:
        return "0000-01-01 00:00"
    
def clean_time2(time_str):
    if not isinstance(time_str, str):
        return "0000-00-00 00:00"

    time_str = time_str.replace(" LT", "").replace("LT", "").strip()
    #print("test1",time_str)

    # Correct date format if needed
    if len(time_str) >= 8 and not time_str[4] == '-' and not time_str[7] == '-'and time_str[6] == '-':
        time_str = time_str[:4] + '-' + time_str[4:6] + time_str[6:]
    #print("test2",time_str)
    
    if len(time_str) >= 8 and not time_str[4] == '-' and not time_str[7] == '-':
        time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]
    #print("test3",time_str)

    # Normalize spacing
    time_str = re.sub(r'\s+', ' ', time_str)
    #print("test4",time_str)

    # Add space between date and time if missing.
    if len(time_str) > 10 and not time_str[10] == " ":
        time_str = time_str[:10] + " " + time_str[10:]
    #print(time_str)

    parts = time_str.split()

    if len(parts) >= 2:
        date_part = parts[0]
        time_part = parts[1].replace(" : ", ":").replace(" :", ":").replace(": ", ":")

        if ":" not in time_part and len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return date_part + " " + time_part
        else:
            return date_part + " " + time_part[:2] + ":" + time_part[2:]

    elif len(parts) == 1:
        time_part = parts[0]
        if len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]
        if len(time_part) == 5 and ":" not in time_part:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return "0000-01-01 " + time_part
        else:
            return "0000-01-01 00:00"

    else:
        return "0000-01-01 00:00"
    
def clean_time3(time_str):
    if not isinstance(time_str, str):
        return ""  # Return blank for non-string values

    original_time_str = time_str.strip()  # Store original trimmed string

    if not original_time_str:
        return ""  # Return blank if originally blank

    # Handle missing values and special characters
    if original_time_str == "-" or re.search(r"[^\x00-\x7F]", original_time_str):
        return ""  # Return blank for missing values and special chars

    time_str = time_str.replace(" LT", "").replace("LT", "").strip()

    # Correct date format if needed
    if len(time_str) >= 8 and not time_str[4] == '-' and not time_str[7] == '-' and time_str[6] == '-':
        time_str = time_str[:4] + '-' + time_str[4:6] + time_str[6:]

    if len(time_str) >= 8 and not time_str[4] == '-' and not time_str[7] == '-':
        time_str = time_str[:4] + '-' + time_str[4:6] + '-' + time_str[6:]

    # Normalize spacing
    time_str = re.sub(r'\s+', ' ', time_str)

    # Add space between date and time if missing.
    if len(time_str) > 10 and not time_str[10] == " ":
        time_str = time_str[:10] + " " + time_str[10:]

    parts = time_str.split()

    if len(parts) >= 2:
        date_part = parts[0]
        time_part = parts[1].replace(" : ", ":").replace(" :", ":").replace(": ", ":")

        if ":" not in time_part and len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return date_part + " " + time_part
        else:
            return date_part + " " + time_part[:2] + ":" + time_part[2:]

    elif len(parts) == 1:
        time_part = parts[0]
        if len(time_part) == 4:
            time_part = time_part[:2] + ":" + time_part[2:]
        if len(time_part) == 5 and ":" not in time_part:
            time_part = time_part[:2] + ":" + time_part[2:]

        if len(time_part) == 5:
            return "0000-01-01 " + time_part
        else:
            return "0000-01-01 00:00"

    else:
        return "0000-01-01 00:00"
    
def calculate_difference(df, started_col, completed_col, duration_col):

    df[duration_col] = "" 

    for index, row in df.iterrows():
        started_str = row[started_col]
        completed_str = row[completed_col]

        if started_str and completed_str:  
            try:
                started_datetime = datetime.strptime(started_str, "%Y-%m-%d %H:%M")
                completed_datetime = datetime.strptime(completed_str, "%Y-%m-%d %H:%M")
                duration = completed_datetime - started_datetime
                df.loc[index, duration_col] = str(duration)
            except ValueError:
                df.loc[index, duration_col] = "Invalid Date/Time"
        else:
          df.loc[index, duration_col] = ""
    return df

def duration_to_minutes(duration_str):
            if pd.isna(duration_str):
                return 0
            h, m, s = map(int, duration_str.split(':'))
            return h * 60 + m + s / 60

def generic_vertical_graph(filepath):

    try:
        df = pd.read_excel(filepath)  # Use read_excel for Excel files

        df['Duration_minutes'] = df['Duration'].apply(duration_to_minutes)

        # Plotting
        plt.figure(figsize=(10, 8))
        plt.bar(df['Activity'], df['Duration_minutes'], color='skyblue')
        plt.ylabel('Duration (minutes)')
        plt.xlabel('Activity')
        plt.title('Activity Duration')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generic_horizontal_graph(filepath):

    try:
        df = pd.read_excel(filepath)

        df['Duration_minutes'] = df['Duration'].apply(duration_to_minutes)

        # Plotting
        plt.figure(figsize=(10, 8))
        plt.barh(df['Activity'], df['Duration_minutes'], color='skyblue')
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Activity')
        plt.title('Activity Duration')
        plt.gca().invert_yaxis() 
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def OCR_table(file_path):
    pipeline = create_pipeline(pipeline="table_recognition")

    output = pipeline.predict(
        input=file_path)
    
    excel_path = "./output/" + os.path.splitext(os.path.basename(file_path))[0] +"/" + os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"

    for res in output:
        res.save_to_xlsx("./output/")
        res.save_to_json("./output/", ensure_ascii=True)

    df = pd.read_excel(excel_path)
    print(df)
    df['Completod'] = df['Completod'].apply(clean_time3)
    df['Started'] = df['Started'].apply(clean_time3)
    df = calculate_difference(df, 'Started', 'Completod', 'Duration')
    print(df)
    df.to_excel(excel_path, index=False)
    return excel_path
    
outputfile = "example2.png"
excel_path = OCR_table(outputfile)
generic_vertical_graph(excel_path)
generic_horizontal_graph(excel_path)
