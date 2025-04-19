import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, '../utils/')
from tools import UTILS as ut
#########################LOAD UTILS###################################
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy import get_style
#######################INQUIRER STYLE SETTINGS####################333
style = get_style({
	"separator": '#6C6C6C',
	"questionmark": '#C33E1B bold',
	"pointer": '#FF9D00 bold',
	"answer": '#2196f3 bold',
	"question": 'white bold',
	"input":"green"
},style_override=False)
#######################INQUIRER STYLE SETTINGS####################333
import requests,random,time,json,string,re
import sys,ctypes,traceback
from bs4 import BeautifulSoup as bs
from faker import Faker
from random import randint
from threading import Thread,Lock
import threading
import queue
import json5
fake=Faker("ja_jp")
Faker.seed(0)
globallock = Lock()

SITEKEY="6Ldrt5IUAAAAAPKXDLBG2QA2ZPydklEpXeIYcISw"
TOKEN_URL = "https://store.sacai.jp/apis/csrf/token.json"
SIGNUP_LINK = "https://store.sacai.jp/signup?lang=en&back_url=https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D"
SIGNUP_SUBMIT_1 = "https://store.sacai.jp/signup/step03"
SIGNUP_SUBMIT_2 = "https://store.sacai.jp/signup/step04"
LOGIN_URL = "https://store.sacai.jp/login?back_url=https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D"
CUS_URL = "https://store.sacai.jp/apis/customer.json"
LOT_URL = "https://store.sacai.jp/apis/apply/lottery/customer.json"
###############################################################################################################
def wait_exit():
	a = input('Press ENTER to exit')
	if a:
	    exit(0)

def account_create_do(i):
	iscomplete = False
	ua_list = UTILS.load_ua("../utils/user_agents.txt")
	with requests.session() as s:
		fname = fake.first_romanized_name()
		lname = fake.last_romanized_name()
		if i == 1:
			email = UTILS.get_email(fname,lname,domain=config["domain"])
		else:
			email = i
		proxy = UTILS.get_proxy(plist)
		print(f"[{email}] Proxy: {proxy['http']}")
		s.proxies.update(proxy)
		s.headers.update({
			"Host": "store.sacai.jp",
			"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",			
			"Sec-Ch-Ua-Mobile": "?0",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": random.choice(ua_list).strip().replace("\"",""),
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-User": "?1",
			"Sec-Fetch-Dest": "document",
			"Referer": SIGNUP_LINK,
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "en-US,en;q=0.9"
			})
	
		print(f"[{email}] Getting token.")
		r = s.get(SIGNUP_LINK)
		try:
			token = s.cookies["fuel_csrf_token"]
		except:
			r = s.get(TOKEN_URL).json()
			token = bs(r["html"],"html.parser").find("input").attrs["value"]
		print(f"[{email}] Getting captcha.")
		c = UTILS.get_captcha(email,config["capmon"],SITEKEY,SIGNUP_SUBMIT_1)
		if not c:
			print(f"[{email}] Failed getting captcha.")
			return None
		addy = random.choice(config["address"])
		add1,add2 = UTILS.format_addy(addy)
		city = addy["city"]
		postcode = addy["zip"]
		state = addy["state"]
		country = addy["country"]
		year=randint(1980,2005)
		month=randint(1,12)
		day=randint(1,28)
		bday="{}-{}-{}".format(year,month,day)
		phone = "".join(random.choices(string.digits,k=10))
		pw = UTILS.get_pw(10,symbol=False)
		s.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
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
		print(f"[{email}] Submit 1.")
		r2 = s.post(SIGNUP_SUBMIT_1,data=payload)
		if r2.status_code == 200:
			payload2 = {
			"fuel_csrf_token":token,
			"back_url":"https%3A%2F%2Fstore.sacai.jp%2Fmember%2Fmod%3F%252Fmember%252Fmod%3D",
			"end":"1",
			"customer_attributes[1][lang]":"en",
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
			"birth":bday,
			"birth_year":year,
			"birth_month":month,
			"birth_day":day,
			"mail_info_send":"2",
			"mail_info_send_flag":"1",
			"mail_magazine_send_flag":"",
			"sex_id":"0",
			"check_preserve_login":"1",
			"preserve_login_flag":"1",
			"recaptcha_token":c,
			"g-recaptcha-response":c
			}
			print(f"[{email}] Submit 2.")
			r3 = s.post(SIGNUP_SUBMIT_2,data = payload2)
			if "Thank you for registering" in r3.text:
				print(f"[{email}] Account created.")
				iscomplete=True
			else:
				print(f"[{email}] Account creation failed.")
				with open("failed.html","w+",encoding="utf-8") as f:
					f.write(r3.text)
				print(r3.status_code)
				print(r3.url)
		return {"complete":iscomplete,"email":email,"pw":pw,"add":city}


def account_create(q):
	global j,k
	while q.qsize() > 0:
		try:
			try:
				i = q.get_nowait()
			except Exception:
				raise
			result = account_create_do(i)
			if not result:
				k+=1
			elif result["complete"] == False:
				k+=1
				with globallock:
					with open("{}accounts_failed.txt".format("domain_" if i == 1 else ""),"a+") as f:
						f.write(f"{result['email']}:{result['pw']}:{result['add']}\n")
			else:
				j+=1
				with globallock:
					with open("{}accounts_success.txt".format("domain_" if i == 1 else ""),"a+") as f:
						f.write(f"{result['email']}:{result['pw']}:{result['add']}\n")
				with globallock:
					ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {config['maxthread']} | Entered: {j} | Failed: {k}")
				time.sleep(config["task_delay"])					
		except Exception:
			traceback.print_exc()
			time.sleep(config["retry_delay"])
			continue
	wait_exit()

def raffle_entry_do(i):
	iscomplete = False
	ua_list = UTILS.load_ua("../utils/user_agents.txt")
	email = i.split(":")[0]
	pw = i.split(":")[1]
	size_list = json.load(open("sizes.json","r",encoding="utf-8"))["colors"]
	with requests.session() as s:
		proxy = UTILS.get_proxy(plist)
		print(f"[{email}] Proxy: {proxy['http']}")
		s.proxies.update(proxy)
		s.headers.update({
			"Host": "store.sacai.jp",
			"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",			
			"Sec-Ch-Ua-Mobile": "?0",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": random.choice(ua_list).strip().replace("\"",""),
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-User": "?1",
			"Sec-Fetch-Dest": "document",
			"Referer": "https://store.sacai.jp/raffle",
			"Accept-Encoding": "gzip, deflate",
			"Accept-Language": "en-US,en;q=0.9"
			})
		
		print(f"[{email}] Getting token.")
		tr = s.get(TOKEN_URL).json()
		token = bs(tr["html"],"html.parser").find("input").attrs["value"]
		s.get(LOGIN_URL)
		payload = {
		"fuel_csrf_token":token,
		"back_url": config["raffle_url"],
		"login_id": email,
		"password": pw,
		"check_preserve_login": 1,
		"preserve_login_flag": 1
		}
		s.headers.update({
			"Content-Type": "application/x-www-form-urlencoded"
			})
		print(f"[{email}] Logging in.")
		r = s.post(LOGIN_URL,data=payload)
		if r.status_code == 200:
			try:
				s.headers.update({"X-Requested-With": "XMLHttpRequest","referer":LOGIN_URL})
				j = s.get(CUS_URL).json()
				if j["status"] == "success":
					print(f"[{email}] Logged in. cid[{j['customer']['customer_id']}]")
				else:
					print(f"[{email}] Error get_cid")
			except Exception:
				print(f"[{email}] Error login")
				return
		print(f"[{email}] Entering raffle")
		s.headers.update({
			"Host": "store.sacai.jp",
			"Origin": "https://store.sacai.jp",
			"Referer": config["raffle_url"],
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
			})
		if config["size_range"]:			
			size = str(random.choice(config["size_range"]))
		else:
			size = "random"
		# #check if only 1 color
		# if len(size_list) == 1:

		color = config["color"].lower()
		if color == "random":
			y=random.choice(range(0,len(size_list)))
			color_chose = size_list[y]["color_name"]
			if size == "random":
				roulette = random.choice(size_list[y]["sizes"])
				sid = roulette["goods_id"]
				size = roulette["size_code"]
			else:
				for i in size_list[y]["sizes"]:
					if i["size_code"] == size:
						sid = i["goods_id"]
		else:
			color_chose = ""
			for i in size_list:
				if color == i["color_name"].lower():
					color_chose = i["color_name"]
					if size == "random":
						roulette = random.choice(i["sizes"])
						sid = roulette["goods_id"]
						size = roulette["size_code"]

					else:
						for j in i["sizes"]:
							if j["size_code"] == size:
								sid = j["goods_id"]						
			if not color_chose:
				print(f"[{email}] Color not found")
				return
		print(f"[{email}] get token2")
		tr2 = s.get(TOKEN_URL).json()
		token2 = bs(tr2["html"],"html.parser").find("input").attrs["value"]		
		d = {
		"goods_id":sid,
		"detail_disp_manage_code":config["raffle_url"].split("detail/")[1],
		"fuel_csrf_token":token2
		}
		entry_r = s.post(LOT_URL,data=d)
		if entry_r.status_code == 200:
			q = entry_r.json()
			if q["is_success"]:
				print(f"[{email}] Successfully Entered.")
				print(f"[{email}] color:{color_chose} size:{size}")
				iscomplete = True
			else:
				print(f"[{email}] Entry failed.")
				print(entry_r.json())
	
	return {"complete":iscomplete,"email":email,"pw":pw,"size":size,"color":color_chose}




def raffle_entry(q):
	global j,k
	while q.qsize() > 0:
		try:
			try:
				i = q.get_nowait()
			except Exception:
				raise
			result = raffle_entry_do(i)
			if not result:
				k+=1
				time.sleep(config["retry_delay"])
			elif result["complete"] == False:
				k+=1
				with globallock:
					with open("raffle_entered_failed.txt","a+") as f:
						f.write(f"{result['email']}:{result['color']}-{result['size']}\n")
				time.sleep(config["retry_delay"])
			else:
				j+=1
				with globallock:
					with open("raffle_entered_success.txt","a+") as f:
						f.write(f"{result['email']}:{result['color']}-{result['size']}\n")
				with globallock:
					ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {config['maxthread']} | Entered: {j} | Failed: {k}")
				time.sleep(config["task_delay"])					
		except Exception:
			traceback.print_exc()
			time.sleep(config["retry_delay"])
			continue
	wait_exit()

def scraper():
	ITEM_URL = input("[scraper] Enter Link (http://): ")
	if not "http" in ITEM_URL.lower():
		print("[scraper] include \"http\"")
		exit(0)
	ua_list = UTILS.load_ua("../utils/user_agents.txt")
	with requests.session() as s:
		proxy = UTILS.get_proxy(plist)
		s.proxies.update(proxy)
		s.headers.update({
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
			"Cache-Control": "max-age=0",
			"Connection": "keep-alive",
			"Host": "store.sacai.jp",
			"sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
			"sec-ch-ua-mobile": "?0",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": random.choice(ua_list).strip().replace("\"","")
			})
		r = s.get(ITEM_URL)
		t=json5.loads(re.search("var item_stock = (.+);",r.text.strip())[1])
		with open("sizes.json","w+",encoding="utf-8") as f:
			json.dump(t,f,indent=4)
	print("[scraper] Done!")
	wait_exit()

def main(mode,t):
	ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {config['maxthread']} | Entered: {j} | Failed: {k}")
	q = queue.Queue()
	if mode == "account_create":
		if t == "email":
			for i in emails:
				q.put(i)
		elif t == "domain":
			for i in range(0,config["amount"]):
				q.put(1)
		try:
			for i in range(0,config["maxthread"]):
				Thread(target=account_create,args=(q,)).start()
		except Exception:
			traceback.print_exc()
			sys.exit()	
	elif mode == "raffle_entry":
		for i in accounts:
			q.put(i)
		try:
			for i in range(0,config["maxthread"]):
				Thread(target=raffle_entry,args=(q,)).start()
		except Exception:
			traceback.print_exc()
			sys.exit()	
	elif mode == "raffle_check":
		pass
	elif mode == "scrape_stock":
		scraper()




if __name__ == '__main__':
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
	#requires faker language, defaults to en_us
	UTILS = ut("ja_jp")
	emails=[]
	t=""
	j=0
	k=0
	mode = inquirer.select(
		message="Select mode:",
		choices = [{"name":"Stock Scraper","value":"scrape_stock"},{"name":"Account Creator","value":"account_create"},{"name":"Raffle Entry","value":"raffle_entry"},{"name":"Raffle Entry Check","value":"raffle_check"},{"name":"Exit","value":None}],
		pointer = ">",
		style=style,
		#set default location to top
		default = 0,
		).execute()
	if mode == "account_create":
		t = inquirer.select(
		message="Select account type:",
		choices = [{"name":"Domain","value":"domain"},{"name":"Load from emails.txt","value":"email"},{"name":"Exit","value":None}],
		pointer = ">",
		style=style,
		#set default location to top
		default = 0,
		).execute()
		if t == "email":		
			try:
				tmp = [i.strip() for i in open("emails.txt").readlines()]
				try:
					d = [i.strip().split(":")[0] for i in open("accounts_success.txt","r+").readlines()]
					emails = [x for x in tmp if x not in d]
				except:
					emails = tmp[:]
				print(f"{len(emails)} emails loaded.")
			except Exception:
				print("Error loading emails.")
				traceback.print_exc()
				sys.exit()
	if mode == "raffle_entry":
		re_failed = inquirer.select(
		message="Select mode:",
		choices = [{"name":"Normal","value":"normal"},{"name":"Filter raffle_entered_failed.txt","value":"remove_failed"},{"name":"Exit","value":None}],
		pointer = ">",
		style=style,
		#set default location to top
		default = 0,
		).execute()
		try:
			tmp = [i.strip() for i in open("accounts.txt").readlines()]
			try:
				d = [i.strip().split(":")[0] for i in open("raffle_entered_success.txt","r").readlines()]
				tmp2 = [x for x in tmp if x.split(":")[0] not in d]
			except:
				tmp2 = tmp[:]
			if re_failed == "remove_failed":
				failed = [i.strip().split(":")[0] for i in open("raffle_entered_failed.txt","r").readlines()]
				tmp3= [x for x in tmp2 if x.split(":")[0] not in failed]
				accounts = tmp3
			else:
				accounts = tmp2
			print(f"{len(accounts)} accounts loaded.")
		except Exception:
			print("Error loading accounts.")
			traceback.print_exc()
			sys.exit()		
	main(mode,t)