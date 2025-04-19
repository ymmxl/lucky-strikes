import requests
from bs4 import BeautifulSoup as bs
import random
import time
import traceback
TOKEN_URL = "https://store.sacai.jp/apis/csrf/token.json"
CHECK_LINK = "https://store.sacai.jp/login"
#will only have newest lottery entry
#s = bs(open("winner page.html","r",encoding='utf-8'),"html.parser")
def do_check(email,html):
	w=False
	print(f"[{email}] checking")
	s = bs(html,"html.parser")
	entry = s.select("ul[class=ec-lottery__list]")
	#print(len(entry[0].contents))
	if len(entry) == 1:
		#check if have entry
		if entry[0].contents:
			campaign = entry[0].select_one("div[class~=ec-lottery__campaign_name]")
			if campaign:
				campaign = campaign.text.strip()
				result = entry[0].select_one("div[class~=ec-lottery__campaign_result]").text.strip()
				if "lose" in result:
					#LOSER
					print(f"[{email}] LOSER")
				elif "ENTRY TIME" in result:
					#WINNER	
					print(f"[{email}] WINNER!")
					w = True
				else:
					#UNKNOWN ERROR
					print(f"[{email}] Unknown Error")
					with open(f"{email} Unknown error.html","w+",encoding='utf-8') as f:
						f.write(html)
			else:
				print("no lottery")
	else:
		print("no entry found")
	return w

def save_accounts(acc,result):
	with open("checked_accounts.txt","a+") as f:
		if result:
			f.write(f"{acc}:WINNER\n")
		else:
			f.write(f"{acc}:LOSER\n")
def checker():
	try:
		plist = [i.strip() for i in open("proxies.txt").readlines()]
		print("Proxies loaded")
	except Exception:
		print("Error loading proxies.")
		sys.exit()
		traceback.print_exc()

	accounts = [i.strip() for i in open("accounts.txt").readlines()]
	for i in accounts:
		email = i.split(":")[0]
		pw = i.split(":")[1]
		print(f"[{email}] Logging in")
		with requests.Session() as s:
			s.headers.update({
				"Host": "store.sacai.jp",
				"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",			
				"Sec-Ch-Ua-Mobile": "?0",
				"Upgrade-Insecure-Requests": "1",
				"content-type": "application/x-www-form-urlencoded",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"referer":CHECK_LINK,
				"Sec-Fetch-Site": "same-origin",
				"Sec-Fetch-Mode": "navigate",
				"Sec-Fetch-User": "?1",
				"Sec-Fetch-Dest": "document",
				"Accept-Encoding": "gzip, deflate",
				"Accept-Language": "en-US,en;q=0.9"
				})
			p = random.choice(plist)
			p = p.strip().split(":")
			proxy = {"http":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1]),"https":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1])}
			s.proxies.update(proxy)
			try:
				print(f"[{email}] Getting token")
				t = s.get(TOKEN_URL).json()
				token = bs(t["html"],"html.parser").find("input").attrs["value"]
				s.cookies.update({"lang":"en"})
			except Exception:
				traceback.print_exc()
				continue
			try:
				p = {
				"fuel_csrf_token": token,
				"back_url": "https://store.sacai.jp/member/ec_lottery",
				"login_id": email,
				"password": pw,
				"check_preserve_login": 1,
				"preserve_login_flag": 1
				}
				r = s.post(CHECK_LINK,data=p)
				if r.url == "https://store.sacai.jp/member/ec_lottery":
					print(f"[{email}] Logged in")

			except Exception:
				print(f"[{email}] Login fail")
				print(r.status_code)
				continue
			try:
				result = do_check(email,r.text)
				save_accounts(i,result)
				print("saved")
			except Exception:
				traceback.print_exc()
		time.sleep(1)

if __name__ == '__main__':
	checker()
