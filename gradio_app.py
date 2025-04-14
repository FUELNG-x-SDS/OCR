import gradio as gr
import os
import pandas as pd
import plotly.express as px
import random

# previous OCR function
# from LNG_functions import OCR_table
from OCR_pdf import pdf_to_png, OCR_table


############################################################################
# helper functions
def read_textfile(filename):
    with open(filename, 'r') as file:
        file_contents = file.read()

    # print(file_contents)
    return file_contents


############################################################################
# main functions
def handle_upload(file):
    report_summary = """Report Summary
                    Operation xxxx was overall a success.\n
                    LNG Bunker: xxxx\n
                    Receiving Vessel: xxxx\n
                    Date: dd/mm/yyyy\n
                    Port: xxxx\n
                    Delivery Location: xxxx"""
    
    remarks = """Remarks"""

    default_columns = ["Activity", "Started", "Completed", "Duration (in minutes)"]
    
    # Case 1: No file uploaded
    if file is None:
        return """No files uploaded/ Wrong file processed.""", gr.update(visible=False), gr.update(visible=False), pd.DataFrame(columns=default_columns)
    
    # Case 2: File uploaded but need to handle png, pdf and csv cases separately
    root, extension = os.path.splitext(file)
        
    # Perform OCR on PNG and PDF files
    if extension == ".png":
        # Call OCR function
        excel_path, df = OCR_table(file)
        report_summary = report_summary

    elif extension == ".pdf":
        # Call OCR function
        png_path = pdf_to_png(file)
        if png_path != None:
            excel_path, df = OCR_table(png_path)
            report_summary = report_summary
        else:
            df = None

        # df = None

    # Process CSV files
    elif extension == ".csv":
        pass

    else:
        return """Unsupported file type.\n 
                Cannot process file.""", gr.update(visible=False), gr.update(visible=False), pd.DataFrame(columns=default_columns)
    

    # if there are errors thrown from OCR (excel_path == None) and (df == None)
    # bring default values for demo
    if df is None or df.empty:
        excel_path = os.path.abspath("./default/example2.xlsx")
        df = pd.read_excel(excel_path, skiprows=[0,1]) # omit first row
        df.columns = default_columns
    
    return report_summary, gr.update(value=excel_path, visible=True) , gr.update(visible=True), df


def save_db(excel_path):
    print("Save to db clicked")
    ## Save db here

############################################################################
# UI elements
with gr.Blocks() as demo:
    with gr.Tab("Individual Report"):
        gr.Markdown("# Individual Report")

        # Define the outputs for individual report
        report_summary = gr.Textbox(label="Report Summary")
        excel_path = gr.File(label="Statement of Facts", visible=False)
        save_to_db = gr.Button("Save to Database", visible=False)
                
        # Define the inputs for individual report
        gr.Interface(fn=handle_upload,
                     inputs="file",
                     outputs=[report_summary, 
                              excel_path, 
                              save_to_db, 
                              gr.DataFrame(label="Download Statement of Facts", headers=["Activity", "Started", "Completed", "Duration"])],
                     flagging_mode="never")
        
        # export_excel.click(get_excel, excel_path, gr.File())
        save_to_db.click(save_db, excel_path)
        

    with gr.Tab("Yearly Review"):
        gr.Markdown("# Yearly Review")

        # Define the inputs for yearly review
        dropdown_count = gr.State(2)
        with gr.Row():
            with gr.Column():
                add_query = gr.Button("Add Query")
                add_query.click(lambda x: x + 1, dropdown_count, dropdown_count)
            with gr.Column():
                remove_query = gr.Button("Remove Query")
                remove_query.click(lambda x: x - 1, dropdown_count, dropdown_count)

        @gr.render(inputs=dropdown_count)
        def render_count(count):
            vessels = []
            years = []
            for i in range(count):
                vessel_radio = gr.Radio(["Bellina", "Venosa"], key=f"vessel-{i}", label="Comparing")
                year_radio = gr.Radio(["2021", "2022", "2023", "2024"], key=f"year-{i}", label="of year")
                vessels.append(vessel_radio)
                years.append(year_radio)

            def submit_query(data):
                # Format it into [{vessel 1: year}, {vessel 2: year}]
                query_input = []

                for vessel, year in zip(vessels, years):
                    # Pass the query to database
                    print(data[vessel], data[year])
                    query_input.append({data[vessel]: data[year]})
                    
                ### postgress query here

                # Then output the graphs for each query input
                


            submit_btn.click(fn=submit_query, 
                             inputs=set(vessels+years), 
                             outputs=[gr.Plot()])

        submit_btn = gr.Button("Submit Query")
        
demo.launch()