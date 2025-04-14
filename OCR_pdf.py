import json
import pandas as pd
import matplotlib.pyplot as plt
from paddlex import create_pipeline
from datetime import datetime
# import psycopg2
import os
import re
import subprocess

def pdf_to_png(pdf_path, dpi=300):

    output_dir = os.path.abspath("./SOF_Images/")
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    # if not os.path.exists('SOF_Images'):
    #     os.makedirs('SOF_Images')

    if pdf_path.lower().endswith(".png"):
        base_name = pdf_path
        print(pdf_path)
    elif '.' in pdf_path:
        base_name = pdf_path.rsplit('.', 1)[0] + ".png"
    else:
        base_name = pdf_path + ".png"
    base_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".png"
    # output_png = os.path.join('SOF_Images', base_name)
    output_png = os.path.join(output_dir, base_name)
    # print(output_png)

    
    try:
        command = [
            "magick", # or "convert" depending on your ImageMagick version.
            "-density",
            str(dpi),
            pdf_path + "[0]", # [0] selects the first page
            output_png,
        ]

        # Execute the command
        subprocess.run(command, check=True)

        print(f"First page of PDF '{pdf_path}' converted to '{output_png}'")

    except subprocess.CalledProcessError as e:
        print(f"Error during PDF to PNG conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: ImageMagick not found. Make sure it's installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    return output_png

def clean_time(time_str):
    if not isinstance(time_str, str):
        return ""

    original_time_str = time_str.strip() 

    if not original_time_str:
        return "" 
    
    if "LT" not in original_time_str:
        return ""

    # Handle missing values and special characters
    if original_time_str == "-" or re.search(r"[^\x00-\x7F]", original_time_str):
        return ""  
    

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
          df.loc[index, duration_col] = "00:00:00"
    return df


def OCR_table(file_path):
    pipeline = create_pipeline(pipeline="table_recognition")

    output = pipeline.predict(
        input=file_path)
    
    output_dir = os.path.abspath("./output/")
    excel_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + ".xlsx")
    json_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + ".json")
    # excel_path = "./SOF_excel/" + os.path.splitext(os.path.basename(file_path))[0] +"/" + os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"
    # json_path = "./SOF_json/" + os.path.splitext(os.path.basename(file_path))[0] + ".json"

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    for res in output:
        res.save_to_xlsx(excel_path)
        res.save_to_json(json_path, ensure_ascii=True)
    
    rec_text = None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:  # Handle potential encoding issues
            data = json.load(f)
            print(data)

            # Check if 'rec_text' exists and handle cases where it might not
            rec_text = data["ocr_result"]["rec_text"]
                
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        return None, None
    except Exception as e: # Catching general exceptions for debugging
        print(f"An error occurred: {e}")
        return None, None
    
    ship_type = None

    for text in rec_text:
        if "LNG Bunker Vessel" in text:
            index = text.find("LNG Bunker Vessel")
            remaining_text = text[index + len("LNG Bunker Vessel"):].strip()

            if ":" in remaining_text:
                ship_type = remaining_text.split(":")[-1].strip().split()[-1]
            elif "-" in remaining_text:
                ship_type = remaining_text.split("-")[-1].strip().split()[-1]
            elif " " in remaining_text:
                ship_type = remaining_text.split()[-1]
            else:
                ship_type = remaining_text

            print(f"Found a ship type: {ship_type}")
            break 

    if ship_type:
        print(f"The captured ship type is: {ship_type}")
    else:
        print("No 'LNG Bunker Vessel' found in the list.")

    df = pd.read_excel(excel_path)
    print(df)
    df['Completed'] = df['Completed'].apply(clean_time)
    df['Started'] = df['Started'].apply(clean_time)
    df = calculate_difference(df, 'Started', 'Completed', 'Duration')
    print(df)
    df['ship_type'] = ship_type
    print(df)
    df.to_excel(excel_path, index=False)

    return excel_path, df

# pdf_path = "FueLNG_SOF_PDFs/SOF_Document_1.pdf"
# png_path = pdf_to_png(pdf_path)
# excel_path = OCR_table(png_path)