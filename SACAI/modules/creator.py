import requests
import sys
from bs4 import BeautifulSoup as bs
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, '../utils/')
from tools import UTILS as ut
import logging
from faker import Faker
fake = Faker("ja_jp")

import random,string,time,sys
from random import randint
from imap_tools import MailBox, AND
import logging,traceback
SIGNUP_LINK = "https://store.sacai.jp/signup?lang=en&back_url=https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D"
TOKEN_URL = "https://store.sacai.jp/apis/csrf/token.json"
SIGNUP_SUBMIT_1 = "https://store.sacai.jp/signup/step03"
SIGNUP_SUBMIT_2 = "https://store.sacai.jp/signup/pre_complete"
ADDY_API = "https://random-data-api.com/api/address/random_address"

UTILS = ut("ja_jp")
log = logging.getLogger(__name__)
fake = Faker("en_us")

def fetch_addy(p):
	try:
		r = requests.get(ADDY_API,proxies=p).json()
	except Exception:
		log.debug(traceback.print_exc())
		r = {
			"street_address":fake.street_address(),
			"secondary_address":fake.secondary_address(),
			"postcode":fake.postalcode(),
			"city":fake.city(),
			"state":fake.state(),
			"country":fake.country()
		}
	return r

def do(domain_name,plist,custom=None):
	with requests.session() as s:
		fname = UTILS.get_fname()
		lname = UTILS.get_lname()
		if custom:
			email = custom
		else:
			email = UTILS.get_email(fname,lname,domain_name)
		p = UTILS.get_proxy(plist)
		s.proxies.update(p)
		s.headers.update({
			"Host": "store.sacai.jp",
			"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",			
			"Sec-Ch-Ua-Mobile": "?0",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-User": "?1",
			"Sec-Fetch-Dest": "document",
			"Referer": SIGNUP_LINK,
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "en-US,en;q=0.9"
			})
		log.info(f"[{email}] getting token")
		r = s.get(SIGNUP_LINK)
		try:
			token = s.cookies["fuel_csrf_token"]
		except:
			r = s.get(TOKEN_URL).json()
			token = bs(r["html"],"html.parser").find("input").attrs["value"]
		s.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
		addy = fetch_addy(p)
		add1 = f"{UTILS.jig(4)} {addy['street_address']}{UTILS.jig(4)}"
		add2 = f"{UTILS.jig(4)} {addy['secondary_address']}"
		city = addy["city"]
		postcode = addy["postcode"].split("-")[0]
		state = addy["state"]
		country = addy["country"]
		year=randint(1980,2005)
		month=randint(1,12)
		day=randint(1,28)
		bday="{}-{}-{}".format(year,month,day)
		phone = "".join(random.choices(string.digits,k=10))
		pw = UTILS.get_pw(10,symbol=False)
		payload = {
			"fuel_csrf_token":token,
			"back_url":"https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D",
			"confirm":"1",
			"name1":fname,
			"name2":lname,
			"name1_kana":"",
			"name2_kana":"",
			"zip":postcode,
			"city":city,
			"town":add1,
			"address":add2,
			"state":state,
			"country":country,
			"pref_id":"",
			"tel":phone,
			"mail":email,
			"password":pw,
			"birth_year":year,
			"birth_month":month,
			"birth_day":day,
			"mail_info_send":"2",
			"check_preserve_login":"1",
			"preserve_login_flag":"1",
			"confirm":"I+AGREE+TO+TERMS+AND+CONFIRM"
		}	
		r2 = s.post(SIGNUP_SUBMIT_1,data=payload)
		if r2.status_code == 200:
			payload2={
				"fuel_csrf_token":r2.cookies["fuel_csrf_token"],
				"back_url":"https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D",
				"customer_attributes%5B1%5D%5Blang%5D":"en",
				"name1":fname,
				"name2":lname,
				"name1_kana":"",
				"name2_kana":"",
				"zip":postcode,
				"country":country,
				"state":state,
				"pref_id":"",
				"city":city,
				"town":add1,
				"address":add2,
				"tel":phone,
				"mail":email,
				"password":pw,
				"password_confirm":"",
				"sex_id":"1",
				"birth":bday,
				"birth_year":year,
				"birth_month":month,
				"birth_day":day,
				"mail_info_send":"2",
				"mail_info_send_flag":"1",
				"mail_magazine_send_flag":"",
				"check_preserve_login":"1",
				"preserve_login_flag":"1",
				"end":"Send+to+email+address"
			}
			log.info(f"[{email}] submit 2")
			r3 = s.post(SIGNUP_SUBMIT_2,data=payload2)
			if "procedure email has been sent" in r3.text:
				log.info(f"[{email}] waiting verification")
				return s,email,pw
			else:
				log.info(f"[{email}] {r3.status_code}")
				err = bs(r3.text,"html.parser").find(class_="error-messages")
				if err:
					log.error(f"[{email}] Error submit2")
					log.warning(err.get_text().strip())
				else:
					log.error(f"[{email}] Unknown error submit2")
					with open("failed submit2.html","w+",encoding="utf-8") as f:
						f.write(r3.text)
				return None,None,None
		else:
			log.error(f"[{email}] something wrong submit 1")
			return None,None,None