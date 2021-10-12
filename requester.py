import pandas as pd

class Request():

    def __init__(self, course_name):
        """ Define and assign the properties of the course """

        # Extract information from "Catalogo UC" into data frames
        data_frames = pd.read_html("http://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla=MAT1620")
        first_table = data_frames[0].to_dict(orient='records') # Convert the first table into a dictionary
        
        # Initialization of dictionary
        properties = {}
 
        # Loop through every row in the first table
        for row in first_table:

            # Extract the row values and convert into a list
            items = list(row.values())

            # Assign values in dictionary of properties
            properties[items[0]] = items[1]

        # Assignment
        self.course_name = course_name
        self.properties = properties

    def prerequisites(self):
        """ Return the values of the prerequisites of the course """
        return self.properties["Prerrequisitos"]