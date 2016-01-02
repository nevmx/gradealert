import mechanicalsoup
import re
import shutil

def getTranscript(browser, us, ps):
	# Request login page
	login_page = browser.get("https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin")
	
	# Grab the form
	login_form = login_page.soup.select('form[name="loginform1"]')[0]
	
	# Set the fields
	login_form.select("#mcg_un")[0]['value'] = us
	login_form.select("#mcg_pw")[0]['value'] = ps

	# Submit the form
	formSubmit  = browser.submit(login_form, login_page.url)
	
	# Verify whether we are logged in
	# The error message has an img with a name attribute of
	# "web_stop"
	assert not formSubmit.soup.select('img[name="web_stop"]')

	# Goto the transcript page
	t_pg = browser.get("https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S")

	# Return the transcript page
	return t_pg 

def parseCourses(page):
	pass

# Get the username and password
with open("ignore/data.txt", "r") as data:
	# Exclude the last character - it is a '\n'
	username = data.readline()[:-1]
	password = data.readline()[:-1]
data.close()

# Main program
browser = mechanicalsoup.Browser()
t_page = getTranscript(browser, username, password)

# Verify correct response
if (t_page.status_code != 200):
	print("ERROR: Cannot access the transcript page")
	exit(1)

courses = []

# All the relevant data is stored in span tags with
# attribute fieldmediumtext
spans = t_page.soup.select("span.fieldmediumtext")

# Extract the text without the tags and replace \xa0 character with ''
textlist = [x.getText().replace('\xa0', '') for x in spans] 

# Copy old file
try:
	shutil.copyfile('grades.txt', 'grades_old.txt')
except IOError:
	print("No old grade file found")

# Open file to save all the grades
grade_file = open("grades.txt", "w")

# Loop through all the lines of data
for i in range(len(textlist)):
	if re.search(r'\b[A-Z]{4}\s[0-9]{3}\b', textlist[i]):
		gradestring = textlist[i] + " " + textlist[i+4]
		grade_file.write(gradestring + "\n")

grade_file.close()
