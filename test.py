from courses import Properties
from recommend import Alumni
import time
startTime = time.time()

"""INFORMATION PROVIDED BY USER"""
# Degree given by the user
degree = "Ingeneria Comercial"

# Courses already taken by the user
courses = ["MAT1620"]

"""PROGRAM"""
Properties("MAT1630")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))