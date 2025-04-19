#########################LOAD UTILS###################################
import sys,os
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, '../utils/')
#sys.path.append(os.path.abspath('../utils/'))
from tools import UTILS as ut
UTILS = ut('en_us')
#########################LOAD UTILS###################################
import requests
import logging
from bs4 import BeautifulSoup as bs
import time,random,traceback,string
from datetime import datetime as dt
from faker import Faker
log = logging.getLogger(__name__)

def process(LINK,proxy,addy,email):
	t=None
	try:
		with requests.session() as s:
			s.proxies.update(proxy)
			s.headers.update({
				"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"accept-encoding": "gzip, deflate, br",
				"accept-language": "en-GB,en;q=0.9",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
				"sec-ch-ua": "\"Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
				"sec-ch-ua-mobile": "?0",
				"upgrade-insecure-requests": "1",
				"cache-control": "max-age=0"
				})
			try:
				r = s.get(LINK,timeout=20)
				if not r.status_code == 200:
					raise
			except Exception as e:
				log.error(f"[{email}] Error fetching page")
				log.warning(e)
				return None
			if "This survey is currently closed." in r.text:
				log.info("Survey is closed.")
				return None
			soup = bs(r.text,"html.parser")
			form = soup.find("form")
			if not form:
				log.info("form not found.")
				return None
			survey_data = form.find("input",id="survey_data").attrs["value"]
			# start_time = dt.now()
			start_time = int(time.time()*1000)
			# add1,add2 = UTILS.format_addy(addy)
			# city = addy["city"]
			# state = addy["state"]
			# postcode = addy["zip"]
			# phone = f"907{''.join(random.choices(string.digits,k=7))}"
			fake = Faker("en_us")
			add1,add2 = UTILS.format_addy({"address1":f"## {fake.street_address()} #suff#","address2":f"## #pre#{random.randint(10,19483)}"})
			city = fake.city()
			state = fake.state_abbr()
			postcode = fake.postcode()
			phone = f"9{''.join(random.choices(string.digits,k=9))}"
			fname = addy["fname"] if addy["fname"] != "RANDOM" else UTILS.get_fname()
			lname = addy["lname"] if addy["lname"] != "RANDOM" else UTILS.get_lname()
			t = {
			"email":email,
			"fname":fname,
			"lname":lname,
			"add1":add1,
			"add2":add2,
			"city":city,
			"state":state,
			"postcode":postcode,
			"phone":phone,
			"data":{
				"session":s,
				"proxy":proxy,
				"survey_data":survey_data,
				"start_time":start_time
				}
			}
	except:
		log.error("Error in Fetcher")
		log.warning(traceback.print_exc())
	return t
if __name__ == '__main__':
	pass