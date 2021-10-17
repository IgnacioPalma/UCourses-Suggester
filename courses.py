import pandas as pd
import concurrent.futures

def Request(course):
    """ Request and return the properties of a given course """
 
    # Extract information from "Catalogo UC" into data frames
    data_frames = pd.read_html(f"http://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla={course}")
    first_table = data_frames[0].to_dict(orient='records') # Convert the first table into a dictionary

    # Initialization of dictionary
    properties = {}

    # Loop through every row in the first table given by "Catalogo UC"
    for row in first_table:

        # Convert row values into a list
        items = list(row.values())

        # Assign values in dictionary of properties
        properties[items[0]] = items[1]
    
    print(properties)
    # Return statement
    return properties

MAX_THREADS = 30

class Properties():

    def __init__(self, course):
        """ Define a course with his properties """

        with concurrent.futures.ThreadPoolExecutor(3) as executor:
            properties = executor.submit(Request, course)

        self.properties = properties
        
    def prerequisites(self):
        """ Return the values of the prerequisites of the course """
        return self.properties["Prerrequisitos"]