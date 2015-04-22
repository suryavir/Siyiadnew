import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains	# to move mouse over

# Google ad settings page class declarations

GENDER_DIV = "EA yP"
AGE_DIV = "EA mP"
LANGUAGES_DIV = "EA EP"
INTERESTS_DIV = "EA rQ"

OPTIN_DIV = "hl Dh uP"
OPTOUT_DIV = "hl LC Dh"
EDIT_DIV = "hl Dh c-Ha-qd c-Ha-Md"
RADIO_DIV = "a-u FA mQ"
SUBMIT_DIV = "c-T-S a-b a-b-A js"
ATTR_SPAN = "mk"

LANG_DROPDOWN = "c-T-S c-g-f-b a-oa Cr"
LANG_DIV = "c-l"

PREF_INPUT = "tQ a-la CK"
PREF_INPUT_FIRST = "zK wK va"
PREF_TR = "BK yr pQ"
PREF_TD = "Yt qQ"
PREF_OK_DIV = "c-T-S a-b a-b-A GJ IC"

SIGNIN_A = "gb_70"

# strip html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def log(msg, id, LOG_FILE):													# Maintains a log of visitations
	fo = open(LOG_FILE, "a")
	fo.write(str(datetime.now())+"||"+msg+"||"+str(id) + '\n')
	fo.close()   
	
def optIn(driver, id, treatmentid, LOG_FILE):													# Opt in to behavioral advertising on Google
	driver.set_page_load_timeout(60)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='"+OPTIN_DIV+"']").click()
	if(id != -1):
		log("optedIn||"+str(treatmentid), id, LOG_FILE)

def optOut(driver, id, treatmentid, LOG_FILE):													# Opt out of behavioral advertising on Google
	driver.set_page_load_timeout(60)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='"+OPTOUT_DIV+"']").click()
	time.sleep(2)
	driver.execute_script("document.getElementsByName('ok')[1].click();")	
	if(id != -1):
		log("optedOut||"+str(treatmentid), id, LOG_FILE)

def login(username, password, driver, id, treatmentid, LOG_FILE):
	driver.set_page_load_timeout(60)
	driver.get("https://www.google.com")
	driver.find_element_by_xpath(".//a[@id='"+SIGNIN_A+"']").click()
	driver.find_element_by_id("Email").send_keys(username)
	driver.find_element_by_id("Passwd").send_keys(password)
	driver.find_element_by_id("signIn").click()
	log("loggedIn="+"@".join(username)+"||"+str(treatmentid), id, LOG_FILE)

def get_gender(driver):												# Read gender from Google Ad Settings
	try:
		driver.get("https://www.google.com/settings/ads")
		gdiv = driver.find_element_by_xpath(".//div[@class='"+GENDER_DIV+"']")
		inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
		return inn
	except:
		print "Error collecting gender. Skipping."
		return "Error reading"
	
def get_age(driver):												# Read age from Google Ad Settings
	try:
		driver.get("https://www.google.com/settings/ads")
		gdiv = driver.find_element_by_xpath(".//div[@class='"+AGE_DIV+"']")
		inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
		return inn
	except:
		print "Error collecting age. Skipping."
		return "Error reading"
		
def get_language(driver):												# Read language from Google Ad Settings
	try:
		driver.get("https://www.google.com/settings/ads")
		gdiv = driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
		inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
		return inn
	except:
		print "Error collecting languages. Skipping."
		return "Error reading"
		
def get_ad_pref(driver, id, treatmentid, LOG_FILE):									# Returns list of Ad preferences
	pref = []
	try:
		driver.get("https://www.google.com/settings/ads")
	# 	if (choice == 1):
	# 		driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
	# 	elif (choice == 2):
		driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
	
		ints = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']/td[@class='"+PREF_TD+"']")
		for interest in ints:
			pref.append(str(interest.get_attribute('innerHTML')))
			#raw_input("Waiting...")
	except:
		print "Error collecting ad preferences. Skipping." %(pref)
		pass
	log("pref"+"||"+str(treatmentid)+"||"+"@".join(pref), id, LOG_FILE)

def set_gender(gender, driver, id, treatmentid, LOG_FILE):										# Set gender on Google Ad Settings page
	driver.set_page_load_timeout(40)
	driver.get("https://www.google.com/settings/ads")
	gdiv = driver.find_element_by_xpath(".//div[@class='"+GENDER_DIV+"']")
# 	print div.get_attribute("innerHTML")
	gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
	if(gender == 'm'):
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")		# MALE			
	elif(gender == 'f'):
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")			# FEMALE
	box.click()
	gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
	log("setGender="+gender+"||"+str(treatmentid), id, LOG_FILE)
	
def set_age(age, driver, id, treatmentid, LOG_FILE):										# Set age on Google Ad Settings page
	driver.set_page_load_timeout(40)
	driver.get("https://www.google.com/settings/ads")
	gdiv = driver.find_element_by_xpath(".//div[@class='"+AGE_DIV+"']")
# 	print gdiv.get_attribute("innerHTML")
	gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
	time.sleep(3)
	if(age>=18 and age<=24):
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")
	elif(age>=25 and age<=34):	
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")
	elif(age>=35 and age<=44):	
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='3']/span")
	elif(age>=45 and age<=54):	
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='4']/span")
	elif(age>=55 and age<=64):
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='5']/span")
	elif(age>=65):
		box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='6']/span")
	box.click()
	gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
	log("setAge="+str(age)+"||"+str(treatmentid), id, LOG_FILE)
	
def set_language(language, driver, id, treatmentid, LOG_FILE):										# Set age on Google Ad Settings page
	driver.set_page_load_timeout(40)
	driver.get("https://www.google.com/settings/ads")
	gdiv = driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
# 	print gdiv.get_attribute("innerHTML")
	gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
	gdiv.find_element_by_xpath(".//div[@class='"+LANG_DROPDOWN+"']").click()
	time.sleep(3)
	gdiv.find_element_by_xpath(".//div[@class='"+LANG_DIV+"'][contains(.,'"+language+"')]").click()
	gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
	log("setLanguage="+str(language)+"||"+str(treatmentid), id, LOG_FILE)


def remove_ad_pref(pref, driver, id, treatmentid, LOG_FILE):
	try:
		driver.get("https://www.google.com/settings/ads")
		prefs = get_ad_pref(driver)
		log("prepref"+"||"+str(treatmentid)+"||"+"@".join(prefs), id)
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
# 		if (choice == 1):
# 			driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
# 		elif (choice == 2):
		driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
		
		rem = []
		while(1):
			trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
			flag=0
			for tr in trs:
				td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']")
				div = tr.find_element_by_xpath(".//td[@class='Wq']/div")
				int = td.get_attribute('innerHTML')
				if pref.lower() in div.get_attribute('aria-label').lower():
					flag=1
					hover = ActionChains(driver).move_to_element(td)
					hover.perform()
					time.sleep(1)
					td.click()
					div.click()
					rem.append(int)
					time.sleep(2)
					break
			if(flag == 0):
				break
		driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
		log("remInterest="+"@".join(rem)+"||"+str(treatmentid), id, LOG_FILE)
	except:
		print "No interests matched '%s'. Skipping." %(pref)

def set_ad_pref(pref, driver, id, treatmentid, LOG_FILE):									# Set an ad pref
	try:
		driver.get("https://www.google.com/settings/ads")
# 		if (choice == 1):
# 			driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
# 		elif (choice == 2):
		driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
		
		driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
		driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
		time.sleep(1)
		trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
		for tr in trs:
			td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
			print td
			log("setInterests="+td+"||"+str(treatmentid), id)
		driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
	except:
		print "Error setting interests containing '%s'. Skipping." %(pref)

def collect_ads(reloads, delay, LOG_FILE, driver, id, treatmentid, site):
	rel = 0
	while (rel < reloads):	# number of reloads on sites to capture all ads
		time.sleep(delay)
		try:
			for i in range(0,1):
				s = datetime.now()
				if(site == 'toi'):
					save_ads_toi(LOG_FILE, driver, id, treatmentid)
				elif(site == 'bbc'):
					save_ads_bbc(LOG_FILE, driver, id, treatmentid)
				elif(site == 'google'):
					save_ads_google(LOG_FILE, driver, id, treatmentid)
				elif(site == 'guardian'):
					save_ads_guardian(LOG_FILE, driver, id, treatmentid)
				elif(site == 'reuters'):
					save_ads_reuters(LOG_FILE, driver, id, treatmentid)
				elif(site == 'bloomberg'):
					save_ads_bloomberg(LOG_FILE, driver, id, treatmentid)
				elif(site == 'fox'):
					save_ads_fox(LOG_FILE, driver, id, treatmentid)
				else:
					raw_input("No such site found: %s!" % site)
				e = datetime.now()
				log('loadtime||'+str(e-s), id, LOG_FILE)
				log('reload', id, LOG_FILE)
		except:
			log('errorcollecting', id, LOG_FILE)
			pass
		rel = rel + 1

def save_ads_fox(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.foxnews.com/us/index.html")
	tim = str(datetime.now())
	frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	driver.switch_to_frame(frame1)
	frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	driver.switch_to_frame(frame2)
	lis = driver.find_elements_by_css_selector("div#ads ul li")
	print len(lis)
	for li in lis:
		t = li.find_element_by_css_selector("td.rh000c div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh010c div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh0111c div span").get_attribute('innerHTML')
# 		f = (str(id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		f = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		print f
		fo = open(file, "a")
		fo.write(f + '\n')
		fo.close()
	driver.switch_to_default_content()
	driver.switch_to_default_content()
		
def save_ads_bloomberg(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.bloomberg.com/")	
	tim = str(datetime.now())
	frame0 = driver.find_element_by_xpath(".//iframe[@src='/bcom/home/iframe/google-adwords']")
	driver.switch_to.frame(frame0)
	frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	driver.switch_to.frame(frame2)
	lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(f + '\n')
		fo.close()
	driver.switch_to.default_content()
	driver.switch_to.default_content()
	driver.switch_to.default_content()

def save_ads_reuters(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.reuters.com/news/us")	
	tim = str(datetime.now())
	frame0 = driver.find_element_by_xpath(".//iframe[@id='pmad-rt-frame']")
	driver.switch_to.frame(frame0)
	frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	driver.switch_to.frame(frame2)
	lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(f + '\n')
		fo.close()
	driver.switch_to.default_content()
	driver.switch_to.default_content()
	driver.switch_to.default_content()

def save_ads_guardian(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.theguardian.com/us")	
	time = str(datetime.now())
	els = driver.find_elements_by_css_selector("div#google-ads-container div.bd ul li")
	for el in els:
		t = el.find_element_by_css_selector("p.t6 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[1].get_attribute('innerHTML')
		l = ps[2].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
		

def save_ads_google(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.google.com/#q=jobs")	
	time = str(datetime.now())
	els = driver.find_elements_by_css_selector("li.ads-ad")
	for el in els:
		t = el.find_element_by_css_selector("h3").get_attribute('innerHTML')
		print "inside google"
		print t
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()

def save_ads_toi(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://timesofindia.indiatimes.com/international-home")
	time.sleep(10)
	tm = str(datetime.now())
	frame = driver.find_element_by_xpath(".//iframe[@id='ad-left-timeswidget']")
	
	def scroll_element_into_view(driver, element):
		"""Scroll element into view"""
		y = element.location['y']
		driver.execute_script('window.scrollTo(0, {0})'.format(y))
	
	scroll_element_into_view(driver, frame)
# 	time.sleep(5)
# 	frame.click()
# 	ActionChains(driver).move_to_element(frame).perform()
# 	time.sleep(200)
	print frame
	driver.switch_to.frame(frame)
	ads = driver.find_elements_by_css_selector("html body table tbody tr td table")
# 	print len(ads)
# 	print ads[0].get_attribute("innerHTML")
# 	time.sleep(2000)
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tm+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		print t
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to.default_content()	
# 	driver.switch_to.frame(frames[1])
# 	frames = driver.find_elements_by_xpath(".//iframe[@id='adhomepage']")
# 	driver.switch_to.frame(frames[0])
# 	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
# 	for ad in ads:
# 		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
# 		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
# 		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tm+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		fo = open(file, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 	driver.switch_to.default_content()
# 	frames = driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_bottom.html']")
# 	driver.switch_to.frame(frames[0])
# 	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
# 	for ad in ads:
# 		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
# 		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
# 		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tm+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		fo = open(file, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 	driver.switch_to.default_content()

def save_ads_bbc(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
# 		global ad_int
	driver.set_page_load_timeout(60)
	driver.get("http://www.bbc.com/news/")
	time = str(datetime.now())
	els = driver.find_elements_by_css_selector("div#bbccom_adsense_mpu div ul li")
	for el in els:
		t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[0].get_attribute('innerHTML')
		l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
