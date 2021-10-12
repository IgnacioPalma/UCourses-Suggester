import pandas as pd

# Information in JSON
# Helper https://jsonlint.com/
import json

# Import the data from the JSON
with open("data.json") as f:
    data = json.load(f)

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


class Alumni():

    def __init__(self, degree, courses_taken):
        """ Define an alumni with his degree and courses taken """
        self.degree = degree
        self.courses_taken = courses_taken

    def check_requisites(self, course, requisites):
        """
        Check if the course has any requisite or co-requisite, if it has, 
        append the requisite or co-requisite to the requisites list. 
        Returns the requisites list.
        """

        # Loop through the constraints of the degree
        for constraint in data[self.degree]["constraints"]:
            
            # Check if the course is in the node of a requisite or co-requisite
            if course in constraint[1]:
                
                requisite = constraint[0]

                # If isn't in the list, add the requisite to the requisites list 
                if requisite not in requisites:
                    requisites.append(requisite)

                # Iterate over the requisite in order to know if has requisites too
                self.check_requisites(requisite, requisites)

        # Return statement
        return requisites

    def check_follow_up_courses(self, course):
        """
        Check if the course has any follow-up course, if it has,
        check if the requisites are met and, if they are, assign it a value of True, otherwise assign it a value of False.
        It only needs to return the possible next courses that are set to True in the form of a list.
        """

        # Initialization of possible next courses dictionary
        possible_next_courses = {}

        # Loop through the constraints of the degree
        for constraint in data[self.degree]["constraints"]:
            
            # Check if the course is the node of a follow-up course
            if course in constraint[0]:
                
                follow_up_course = constraint[1]

                # Check if the follow up course isn't already in the courses_taken list
                if follow_up_course not in self.courses_taken:
                    
                    # Check the requisites of the follow-up course
                    requisites = self.check_requisites(follow_up_course, requisites=[])

                    # Check if the requisites of the follow-up course are met by the courses taken by the alumni
                    if set(requisites).issubset(self.courses_taken):
                        possible_next_courses[follow_up_course] = True
                        
                    else: # The conditions aren't met
                        possible_next_courses[follow_up_course] = False
                    
                else: # The conditions aren't met
                    possible_next_courses[follow_up_course] = False

        # Initialization of follow up courses list
        follow_up_courses = []

        # Check for possible next courses equal to true and append it to the
        for possible_next_course in possible_next_courses.keys():
            if possible_next_courses[possible_next_course] is True:
                follow_up_courses.append(possible_next_course)
            
        # Return statement
        return follow_up_courses

    def suggestion(self):
        """ 
        Give a suggestion of the series of courses that the alumni should take next
        based in the courses that him already made.
        """

        # Initialization of list
        follow_up_courses = []

        " Case for courses with requisites "

        # Loop through every course taken by the alumni
        for course in self.courses_taken:

            # Check for follow-up courses and append this courses to the general list
            follow_up_courses.extend(self.check_follow_up_courses(course))
        
        " Case for courses with co-requisites "

        # Initialization of follow-up courses by co-requisite list
        follow_up_courses_by_corequisite = []

        # Loop through the constraints of the degree
        for constraint in data[self.degree]["constraints"]:

            # Check if the constraint is in the form of a co-requisite
            if len(constraint) == 3:

                # Check if the course in the node is in the follow_up_courses list
                if constraint[0] in follow_up_courses:
                    
                    # Append the course that follow-up the course in the node
                    follow_up_courses_by_corequisite.append(constraint[1])
        
        # Add the follow-up courses by corequisite to the general list
        follow_up_courses.extend(follow_up_courses_by_corequisite)

        " Case for courses with no requisites nor co-requisites "

        # Initialization of no-requisites courses list
        no_requisites_courses = []
                
        # Return statement
        return follow_up_courses

    def courses_made(self):
        
        # List
        lst = []
        for course in self.courses_taken.copy():
            requisites = self.check_requisites(course, requisites=[])
            lst.extend(requisites)
        
        self.courses_taken.extend(list(set(lst)))
        print(self.courses_taken)