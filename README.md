13 April Update
3 Files added to codebase
- LNG_prototype.py
- LNG_prototype_postgress_upload.py
- LNG_prototype_query.py

MAKE SURE TO DOWNLOAD IMAGEMAGICK FOR PDF CONVERSION

LNG_prototype.py
-Only takes a PDF (use mock data from turag)
>Takes in PDF, OCR operation, Output as excel

LNG_prototype_postgress_upload.py
>Uses path from excel to upload to postgres database
>Once uploaded provides a summary bar chart of the pre and post bunkering timings

LNG_prototype_query.py
-Takes in ship_type(VENOSA/BELINA), year1 and year2 as inputs.
-Produces a bar chart for the ship at those years comparison
