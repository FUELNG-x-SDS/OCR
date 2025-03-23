import gradio as gr
import os

from LNG_functions import OCR_table

# helper functions
def read_textfile(filename):
    with open(filename, 'r') as file:
        file_contents = file.read()

    # print(file_contents)
    return file_contents

# main functions
def handle_upload(file):
    report_header = "## Report Summary"
    operation_msg, pre_bunkering_msg, bunkering_msg, post_bunkering_msg = '', '', '', ''
    
    # Case 1: No file uploaded
    if file is None:
        operation_msg = "No files uploaded."
        # return report_header, "No files uploaded."
    
    # Case 2: File uploaded but need to handle png, pdf and csv cases separately
    root, extension = os.path.splitext(file)
        
    # Perform OCR on PNG and PDF files
    if extension in [".png", ".pdf"]:
        excel_path = OCR_table(file)

        operation_msg = read_textfile("./results/operation_message.txt")

        # return "## Report Summary", operation_msg
        # Add your OCR processing code here

    # Process CSV files
    elif extension == ".csv":
        operation_msg = f"Processing CSV file: {file}"
        # return"## Report Summary", f"Processing CSV file: {file}"
        # Add your CSV processing code here

    else:
        operation_msg = f"Unsupported file type. Cannot process file."
        # return "## Report Summary", f"Unsupported file type"
    
    return report_header, operation_msg, pre_bunkering_msg, bunkering_msg, post_bunkering_msg


with gr.Blocks() as demo:
    with gr.Tab("Individual Report"):
        # UI elements
        gr.Markdown("# Individual Report")

        # Define the outputs for individual report
        report_header = gr.Markdown()
        operation_message = gr.Textbox(label="Operation Details")
        pre_bunkering_msg = gr.Textbox(label="Pre-bunkering Details")
        bunkering_msg = gr.Textbox(label="Bunkering Details")
        post_bunkering_msg = gr.Textbox(label="Post-bunkering Details")
                
        gr.Interface(fn=handle_upload,
                     inputs="file",
                     outputs=[report_header, operation_message, pre_bunkering_msg, bunkering_msg, post_bunkering_msg],
                     flagging_mode="never")

        # connect UI elements to functions

        
demo.launch()