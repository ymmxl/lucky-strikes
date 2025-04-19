##############IMPORT ASKER####################
from InquirerPy import inquirer
from InquirerPy import get_style
style = get_style({
	"separator": '#6C6C6C',
	"questionmark": '#C33E1B bold',
	"pointer": '#FF9D00 bold',
	"answer": '#2196f3 bold',
	"question": 'white bold',
	"input":"green"
},style_override=False)
##############IMPORT ASKER####################
#########################LOAD UTILS###################################
import sys,os
# insert at position 1 in the path, as 0 is the path of this file.
#sys.path.insert(1, '../utils/')
sys.path.append(os.path.abspath('../utils/'))
from tools import UTILS as ut
UTILS = ut('en_us')
import logger
from dotenv import load_dotenv
sys.path.append(os.path.abspath('../'))
from utils.env_loader import load_environment
#########################LOAD UTILS###################################
import csv,math
from bs4 import BeautifulSoup as bs
import math,random,time,json,string,traceback,sys,re
import requests
from faker import Faker
fake = Faker("en_us")
Faker.seed(0)

# Load environment variables
env_vars = load_environment()

SIGN_UP = "https://notreraffle.com/api/register"
SITEKEY = env_vars.get('NOTRE_SITEKEY', "6LdkgS0aAAAAANN1A9vAzqqeszXWuQ7r94U_Ro11")
APIKEY = env_vars.get('CAPTCHA_API_KEY', "")
C_URL = "https://notreraffle.com/register"
def fetch():
	# addy = random.choice(config["address"])
	addy = {
		"fname":fake.first_name(),
		"lname":fake.last_name(),
		"address1":f"{fake.street_address()} #suff#",
		"address2":f"## #pre#{random.randint(10,19483)}",
		"city" :fake.city(),
		"state" :fake.state(),
		"postcode" :fake.postcode(),
		"phone": f"9{''.join(random.choices(string.digits,k=9))}",

	}
	add1,add2 = UTILS.format_addy(addy["address1"],addy['address2'])
	with requests.Session() as s:
		s.headers.update({
			"Host": "notreraffle.com",
			"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",			
			"Sec-Ch-Ua-Mobile": "?0",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Sec-Fetch-Site": "none",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-User": "?1",
			"Sec-Fetch-Dest": "document",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
			"sec-ch-ua-platform": "\"Windows\"",
			"referer":LINK	
			})
		proxy = UTILS.get_proxy(plist)
		s.proxies.update(proxy)
		log.info("Fetching page")
		r = s.get(LINK)
		log.info("registering user")
		q = s.get("https://notreraffle.com/api/question-answers/random")
		xsrf = q.cookies["XSRF-TOKEN"]
		q = q.json()
		key = q["qna"]["key"]
		q_id = q["qna"]["id"]
		options = q["qna"]["options"]
		for i in ans_list:
			if q_id == i["id"]:
				answer = i["answer"]
			else:
				print("answer not found.")
				print(q["qna"]["question"])
				sys.exit()
		g = get_captcha(email,APIKEY,SITEKEY,C_URL)
		if g:
			s.headers.update({
				"Accept": "application/json, text/plain, */*",
				"X-Requested-With": "XMLHttpRequest",
				"Content-Type": "application/json;charset=UTF-8",
				"Origin": "https://notreraffle.com",
				"Referer": "https://notreraffle.com/register",
				"x-xsrf-token":xsrf
				})
			payload = {
				"state": addy['state'],
				"country": "United States",
				"meta":
				{
					"optins":
					{
						"email_marketing_optin": True
					}
				},
				"recaptcha":g,
				"first_name": addy["fname"],
				"last_name": addy["lname"],
				"email": email,
				"phone_number": addy["phone"],
				"street_address": f"{add1} {add2}",
				"city": addy["city"],
				"zip": addy["postcode"],
				"qna_key": key,
				"answer": options[answer]
			}
			try:
				r2 = s.post(SIGN_UP,json=payload)
				print(r2.status_code)
				print(r2.json()["success"])
			except:
				print("error register")
				pass



if __name__ == '__main__':
	log = logger.setup_logger()
	try:
		plist = [i.strip() for i in open("proxies.txt").readlines()]
		print("Proxies loaded")
	except Exception:
		print("Error loading proxies.")
		sys.exit()
		traceback.print_exc()
	try:
		config = json.load(open("config.json","r"))
		print("config loaded.")
	except Exception:
		print("Error loading config.")
		traceback.print_exc()
		sys.exit()
	try:
		ans_list = json.load(open("answers.json","r"))
		print("ans_list loaded.")
	except Exception:
		print("Error loading ans_list.")
		traceback.print_exc()
		sys.exit()
	#LINK = input("Raffle ID?")
	LINK = "https://notreraffle.com/raffles/147"