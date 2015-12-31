import mechanicalsoup

class Course(object):
	def __init__(self, name, grade):
		self.name = name
		self.grade = grade
	def __str__(self):
		return self.name + ": " + self.grade


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

# Main program
browser = mechanicalsoup.Browser()
t_page = getTranscript(browser, "username", "password")

print(t_page.status_code)
