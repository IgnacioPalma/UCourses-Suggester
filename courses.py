import pandas as pd

class Properties():

    def __init__(self, name):
        """ Define a course with his name and properties """

        # Extract information from "Catalogo UC" into data frames
        data_frames = pd.read_html(f"http://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla={name}")
        first_table = data_frames[0].to_dict(orient='records') # Convert the first table into a dictionary
        
        # Initialization of dictionary
        properties = {}
 
        # Loop through every row in the first table given by "Catalogo UC"
        for row in first_table:

            # Convert row values into a list
            items = list(row.values())

            # Assign values in dictionary of properties
            properties[items[0]] = items[1]

        # Assignment
        self.properties = properties

    def prerequisites(self):
        """ Return the values of the prerequisites of the course """
        return self.properties["Prerrequisitos"]