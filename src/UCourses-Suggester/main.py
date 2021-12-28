import pandas as pd

class Course:
    """ Define a course with his proper properties. """

    def __init__(self, id):

        # Extract information from "Catalogo UC" into data frames
        data_frames = pd.read_html(f"http://catalogo.uc.cl/index.php?tmpl=component&option=com_catalogo&view=requisitos&sigla={id}")
        
        # Convert the first table into a dictionary
        first_table = data_frames[0].to_dict(orient='records')

        # Initializations
        self.id = id
        self.properties = {}
        
        # Loop through every row in the first table given by "Catalogo UC" and 
        # assign values into the dictionary
        for row in first_table:

            items = list(row.values())
            self.properties[items[0]] = items[1]


    def prerequisites(self):
        """ 
        Fetches and returns the prerequisites of the course in a list of sets.
        The sets correspond to the inclusive courses.
         """
        
        # Check if there are prerequisites, if not, return None.
        if self.properties["Prerrequisitos"] == "No tiene":
            return None
        
        else:
            # Initializations
            init = 0
            exclusive_courses = []
            inclusive_courses = []
            prerrequisitos_length = len(self.properties["Prerrequisitos"])

            # Loop through every character in the "Prerequisitos" section in order to order the courses
            # in sets exclusive and inclusive.
            for ind, char in enumerate(self.properties["Prerrequisitos"]):

                # Check if the string has a separation of conditions
                if char == "y" or char == "o":
                    
                    if char == "y":

                        # Check for brackets; enforce the removal.
                        if self.properties["Prerrequisitos"][init] == "(":
                            inclusive_courses.append(self.properties["Prerrequisitos"][init+1:ind-1])
                        else:
                            inclusive_courses.append(self.properties["Prerrequisitos"][init:ind-1])

                    elif char == "o":

                        # Check for brackets; enforce the removal.
                        if self.properties["Prerrequisitos"][ind-2] == ")":
                            inclusive_courses.append(self.properties["Prerrequisitos"][init:ind-2])
                        else:
                            inclusive_courses.append(self.properties["Prerrequisitos"][init:ind-1])
                        
                        exclusive_courses.append(set(inclusive_courses))
                        inclusive_courses = []

                    # Correct the position
                    init = ind + 2

                # Check if we have got to the end of the string in order to append the final course
                elif ind == prerrequisitos_length - 1:

                    # Check for brackets; enforce the removal.
                    if self.properties["Prerrequisitos"][ind] == ")":
                        inclusive_courses.append(self.properties["Prerrequisitos"][init:ind])
                    else:
                        inclusive_courses.append(self.properties["Prerrequisitos"][init:ind+1])
                            
                    exclusive_courses.append(set(inclusive_courses))

            # Return statement
            return exclusive_courses

        
        

