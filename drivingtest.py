import smtplib
from mechanize import Browser
from datetime import datetime
import sys, random
from BeautifulSoup import BeautifulSoup

# the latest date you are interested in a driving test
currentBooking = datetime.strptime("2017-10-13", "%Y-%m-%d")

def find_links( browser, key, val ):
	links = []

	for link in browser.links():
		for k, v in link.attrs:
			if k == key and val in v:
				links.append( link )
				break

	return links

agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8','Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36']

browser = Browser()
browser.addheaders = [('User-agent', random.choice(agents))]
browser.set_handle_robots(False)

response = browser.open('https://www.gov.uk/change-driving-test')
print( response.code)

startLink = [ link for link in browser.links() if "start now" in link.text.lower() ][0]
response = browser.follow_link(startLink)

# log in, username is actually the licence number and password is
# the test reference
browser.select_form(nr=0)
browser.form["username"] = "THELICENCENUMBER"
browser.form["password"] = "PASSWORD"
response = browser.submit()

#print( response.get_data() )

# if you want to search multiple locations, but make sure that each string only returns
# a single venue when searched for
locations = ["Birmingham (Garretts Green)", "Brighton (Somewhere else)"]

dates = []

for location in locations:
	print "Checking %s" % location

	response = browser.open("https://driverpracticaltest.direct.gov.uk/manage?execution=e1s1")

	# change venue
	changeLink = find_links(browser, "id", "test-centre-change")[0]
	response = browser.follow_link(changeLink)

	# select venue
	browser.select_form(nr=0)
	browser.form["testCentreName"] = location
	response = browser.submit()

	#print( response.get_data() )

	# select the test centre
	selectLink = find_links(browser, "id", "centre-name")[0]
	response = browser.follow_link(selectLink)

	soup = BeautifulSoup(response.get_data())

	for td in soup.findAll('td', attrs={"class": "BookingCalendar-date--bookable "}):
		for a in td.findAll('a', attrs={"class": "BookingCalendar-dateLink "}):
			d = datetime.strptime(a["data-date"], "%Y-%m-%d")
			if d < currentBooking:
				dates.append((location,d))

if dates == []:
	sys.exit()


# send the actual email
msg = ""
for location, d in dates:
	print location, d
	msg += "%s %s\r\n" % (location,d)

toaddrs = ['someone@somewhere.com']

# Credentials (if needed)
username = 'EMAILADDRESS'
password = 'EMAILPASSWORD'

body = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}".format(username,toaddrs,"Driving tests",msg)

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
for addr in toaddrs:
	server.sendmail(username, addr, body)
server.quit()
