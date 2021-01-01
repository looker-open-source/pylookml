Purpose:
This utility provides a workflow for updating the property map of pyLookML.
The excel workbook has the hierarchical relationships in Lookml.
Each row represents a parent > property relationship and the settings of the prop in that
context.

The workflow for updating the language map:
Step 1) Update or create a new property row ensuring to follow the conventions for each 
column, exhibited in the rows above

Step 2) The workbook has a column (Column L "copy this python"). Ensure that the formula is working and has filled
values for each aspect of your new row (it builds based on several columns to the right)

Step 3) Copy the contents of Column L "copy this python" into lang_map_generator.py
between the #generated code# and #end generated code# delimeters (replacing any existing contents there)

Step 4) run `python lang_map_generator.py` which will use the excel generated python to replace the language data
files in lookml/lib/language_data

Step 5) run suite of unit tests to confirm that pyLookML is working as intended