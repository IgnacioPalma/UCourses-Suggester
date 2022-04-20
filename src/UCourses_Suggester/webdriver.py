from time import sleep
from bs4 import BeautifulSoup
from uc_sso import get_ticket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager

name = input("Name: ")
password = input("Password: ")

""" 
First Step:
Access the URL and submit the form given the inputs
Problems: HTML ID's
"""

# Choose the webdriver
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# Get tickets from the SSO UC
ticket = get_ticket(name, password, "https://seguimientocurricular.uc.cl/")

# We need to check that the ticket returns a 200

# Access the URL
driver.get(ticket.service_url)

# Find the drop-down element by id and select the value of the option
select = Select(driver.find_element(By.ID, "j_idt49:_t52"))
select.select_by_value("050014")

# Submit the drop-down form
driver.find_element(By.ID, "j_idt49:_t55").click()

"""
Second Step:
Obtain the HTML from the page solving the problem of the nested Javascript
"""

# Wait for the page to load and execute the scripts in order to obtain the HTML
sleep(5)
html_text = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

"""
Third Step:
Find the courses taken by the student
"""

# Read the html text
soup = BeautifulSoup(html_text, "lxml")

# Initialization of variables
courses_taken = []
i = 0

# Loop until we can't find any more courses
while True:
    
    # Find the raw course
    raw_course = soup.find("span", id=f"j_idt49:_t253:{i}:_t257")

    # Break statement
    if raw_course is None:
        break
    
    course = raw_course.text
    courses_taken.append(course)
    i += 1

print(courses_taken)
