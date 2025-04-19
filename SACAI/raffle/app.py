import traceback,sys,time
import requests
from bs4 import BeautifulSoup as bs
import json,random
LOGIN_URL = "https://store.sacai.jp/login?lang=en"
TOKEN_URL = "https://store.sacai.jp/apis/csrf/token.json"
LOT_URL = "https://store.sacai.jp/apis/apply/lottery/customer.json"
CUS_URL = "https://store.sacai.jp/apis/customer.json"
ITEM_URL = "https://store.sacai.jp/item/detail/1_1_21-0322S_1/303"

def getProxy():
	if plist:
		p = random.choice(plist).split(":")
		try:
			return "{}:{}@{}:{}".format(p[2],p[3],p[0],p[1])
		except:
			return "{}:{}".format(p[0],p[1])
	return None
def get_sess():
	s = requests.Session()
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
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
		})
	p = getProxy()
	s.proxies.update({
		"http": "http://"+p,
		"https": "http://"+p
	})	
	return s

def main(acc):
	s = get_sess()
	r = s.get(TOKEN_URL).json()
	token = bs(r["html"],"html.parser").find("input").attrs["value"]

	payload = {
	"fuel_csrf_token":token,
	"back_url": ITEM_URL,
	"login_id": acc.split(":")[0],
	"password": acc.split(":")[1],
	"check_preserve_login": 1,
	"preserve_login_flag": 1
	}
	s.headers.update({
		"Content-Type": "application/x-www-form-urlencoded"
		})
	r2 = s.post(LOGIN_URL,data=payload)
	print(r2.url)
	if r2.status_code == 200:
		try:
			s.headers.update({"X-Requested-With": "XMLHttpRequest","referer":LOGIN_URL})
			j = s.get(CUS_URL).json()
			if j["status"] == "success":
				print(j["customer"]["customer_id"])
				ecuu = j["customer"]["unique_code"]
				print("[{}] Logged in".format(acc.split(":")[0]))
			else:
				print("Error get_cus")
		except Exception:
			print("Error login")
			traceback.print_exc()
	else:
		print(r2.status_code)
		print(r2.url)
	print("Entering raffle")
	s.headers.update({
		"Host": "store.sacai.jp",
		"Origin": "https://store.sacai.jp",
		"Referer": ITEM_URL,
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
		})
	s.cookies.set("ecuuc",ecuu)
	size = str(random.choice([8.5,9]))
	print(size)
	for i in sizelist:
		if i["size_code"] == size:
			sid = i["goods_id"]
	d = {
	"goods_id":sid,
	"detail_disp_manage_code":"1_1_21-0322S_1"
	}
	res = s.post(LOT_URL,data=d)
	if res.status_code == 200:
		q = res.json()
		if q["is_success"]:
			print("[{}] Successfully Entered".format(acc.split(":")[0]))
			with open("Entered.txt","a+",encoding="utf-8") as f:
				f.write(acc+","+size+"\n")
		else:
			print("Entry Failed")
			print(res.json())

if __name__ == '__main__':
	try:
		plist = [i.replace("\n","") for i in open("proxies.txt").readlines()]
	except Exception:
		print("Error loading proxies.")
		traceback.print_exc()
	try:
		accounts = [i.replace("\n","") for i in open("Accounts.txt","r").readlines()]
	except Exception:	
		print("Error loading Accounts.")
		traceback.print_exc()
	global sizelist
	#TAN
	sizelist = json.load(open("v3.json","r",encoding="utf-8"))["colors"][1]["sizes"]
	# size = str(random.choice([8.5,9,9.5,10,10.5,11]))
	# print(size)
	# for i in sizelist:
	# 	if i["size_code"] == size:
	# 		sid = i["goods_id"]
	# print(sid)
	# sys.exit()
	for i in accounts:
		main(i)
		time.sleep(30)
