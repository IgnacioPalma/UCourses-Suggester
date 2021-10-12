# Information in JSON
# Helper https://jsonlint.com/
import json

# Import the data from the JSON
with open("data.json") as f:
    data = json.load(f)

class Course():

    def __init__(self, name, degree):
        """ Define a course with his name and the degree in which takes place """
        self.name = name

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