import gradio as gr
import os
import pandas as pd


from LNG_functions import OCR_table


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

    default_columns = ["Activity EOSP", "Started", "Completed", "Duration"]
    
    # Case 1: No file uploaded
    if file is None:
        return """No files uploaded/ Wrong file processed.""", gr.update(visible=False), gr.update(visible=False), pd.DataFrame(columns=default_columns)
    
    # Case 2: File uploaded but need to handle png, pdf and csv cases separately
    root, extension = os.path.splitext(file)
        
    # Perform OCR on PNG and PDF files
    if extension in [".png", ".pdf"]:
        # Call OCR function
        excel_path, df = OCR_table(file)

        report_summary = report_summary

    # Process CSV files
    elif extension == ".csv":
        pass

    else:
        return """Unsupported file type.\n 
                Cannot process file.""", gr.update(visible=False), gr.update(visible=False), pd.DataFrame(columns=default_columns)
    
    return report_summary, gr.update(visible=True), gr.update(visible=True), df


def get_excel():
    print("Export to excel clicked")


def save_db():
    print("Save to db clicked")


def annual_query():
    pass

############################################################################
# UI elements
with gr.Blocks() as demo:
    with gr.Tab("Individual Report"):
        gr.Markdown("# Individual Report")

        # Define the outputs for individual report
        report_summary = gr.Textbox(label="Report Summary")
        export_excel = gr.Button("Export to Excel", visible=False)
        save_to_db = gr.Button("Save to Database", visible=False)
                
        # Define the inputs for individual report
        gr.Interface(fn=handle_upload,
                     inputs="file",
                     outputs=[report_summary, 
                              export_excel, 
                              save_to_db, 
                              gr.DataFrame(label="Statement of Facts", headers=["Activity EOSP", "Started", "Completed", "Duration"])],
                     flagging_mode="never")
        
        export_excel.click(get_excel)
        save_to_db.click(save_db)
        

    with gr.Tab("Yearly Review"):
        gr.Markdown("# Yearly Review")

        # Define the inputs for yearly review
        gr.Interface(fn=annual_query)

        
demo.launch()