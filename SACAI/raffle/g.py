from logzero import logger as log
import logzero,logging

import json,os,sys,string,requests,random,time
from python_capmonster import NoCaptchaTaskProxyless
from datetime import datetime as dt

##################### ENABLES log.success() USAGE #####################################
logging.addLevelName(15,"success")
def success(self, message, *args, **kws):
  if self.isEnabledFor(15):
    self._log(15,message,args,**kws)
logging.Logger.success = success
logzero.LogFormatter.DEFAULT_COLORS[15] = logzero.colors.Fore.GREEN
################# ENABLE FOR SCRIPTS IN SERVERS ###############
SERVER=True
fmt = logzero.LogFormatter(fmt = "%(color)s[%(asctime)s] %(message)s %(end_color)s",datefmt = "%Y-%m-%dT%H:%M:%SZ")
logzero.LogFormatter.DEFAULT_COLORS[20] = logzero.colors.Fore.CYAN
################# ENABLE FOR SCRIPTS IN SERVERS ###############
#loglevel info = 20, change log.info to CYAN, default was green
#################### ENABLES log.success() USAGE #####################################
######################## INITIALIZE LOG FILE #######################
def init_log(file=""):
	global log
	d = dt.now().strftime("%y%m%d %Hh%Mm")
	logfile = "{}.log".format(d)
	if SERVER and file:
		if not os.path.exists("./logs"):
			os.mkdir("logs")
		if not os.path.exists("./logs/{}".format(logfile)):
			with open("./logs/{}".format(logfile),"w+"): pass
		log = logzero.setup_logger(logfile = "logs/{}".format(logfile),maxBytes=1e6, backupCount=3,formatter=fmt)	
	elif SERVER and not file:
		log = logzero.setup_logger()
	elif not SERVER and file:
		if not os.path.exists("./logs/{}".format(logfile)):
			with open("./logs/{}".format(logfile),"w+"): pass
		log = logzero.setup_logger(logfile = "logs/{}".format(logfile),maxBytes=1e6, backupCount=3)
	else: #log to stdout only
		log = logzero.setup_logger()
	log.info("Logfile initialized.")
######################## INITIALIZE LOG FILE #######################

z = """{'green': [{'size': '3.5', 'goods_id': '4455'}, {'size': '4', 'goods_id': '4456'}, {'size': '5', 'goods_id': '4457'}, {'size': '6', 'goods_id': '4458'}, {'size': '6.5', 'goods_id': '4459'}, {'size': '7', 'goods_id': '4460'}, {'size': '7.5', 'goods_id': '4461'}, {'size': '8', 'goods_id': '4462'}, {'size': '8.5', 'goods_id': '4463'}, {'size': '9', 'goods_id': '4464'}, {'size': '9.5', 'goods_id': '4465'}, {'size': '10', 'goods_id': '4466'}, {'size': '10.5', 'goods_id': '4467'}, {'size': '11', 'goods_id': '4468'}, {'size': '11.5', 'goods_id': '4469'}, {'size': '12', 'goods_id': '4470'}, {'size': '13', 'goods_id': '4471'}], 'red': [{'size': '3.5', 'goods_id': '4472'}, {'size': '4', 'goods_id': '4473'}, {'size': '5', 'goods_id': '4474'}, {'size': '6', 'goods_id': '4475'}, {'size': '6.5', 'goods_id': '4476'}, {'size': '7', 'goods_id': '4477'}, {'size': '7.5', 'goods_id': '4478'}, {'size': '8', 'goods_id': '4479'}, {'size': '8.5', 'goods_id': '4480'}, {'size': '9', 'goods_id': '4481'}, {'size': '9.5', 'goods_id': '4482'}, {'size': '10', 'goods_id': '4483'}, {'size': '10.5', 'goods_id': '4484'}, {'size': '11', 'goods_id': '4485'}, {'size': '11.5', 'goods_id': '4486'}, {'size': '12', 'goods_id': '4487'}, {'size': '13', 'goods_id': '4488'}]}"""
sizes = json.loads(z.replace("'","\""))
URL = "https://store.sacai.jp/signup?lang=en"
C_URL = "https://store.sacai.jp/signup/step02"
temp = "https://store.sacai.jp/signup/step03"
submit_url = "https://store.sacai.jp/signup/step04"
SITEKEY = "6Ldrt5IUAAAAAPKXDLBG2QA2ZPydklEpXeIYcISw"
apiKey = ""
CAPMONSTER_API = ""

def get_captcha():
	try:
		capmonster = NoCaptchaTaskProxyless(client_key=CAPMONSTER_API)
		taskId = capmonster.createTask(website_key=SITEKEY, website_url=C_URL)
		response = capmonster.joinTaskResult(taskId=taskId)
		return response
	except Exceptions as e:
		log.error("Captcha exception:{}".format(e))
		return

def get_sess():
	s = requests.session()
	s.headers.update({
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
		"Connection": "keep-alive",
		"Host": "store.sacai.jp",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "none",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
		})
	proxy = getProxy()
	if proxy is not None:
		s.proxies.update({
			"http": "http://"+proxy,
			"https": "http://"+proxy
		})
	return s,proxy

def getProxy():
	if plist:
		p = random.choice(plist).split(":")
		try:
			return "{}:{}@{}:{}".format(p[2],p[3],p[0],p[1])
		except:
			return "{}:{}".format(p[0],p[1])
	return None

def login(s,proxy,email,pw):
	ecuu = None
	url = "https://store.sacai.jp/login"
	log.info("proxy: {}".format(proxy))
	log.info("Logging in.[{}]".format(email))
	s.get(url,timeout=TIMEOUT)
	token = s.cookies['fuel_csrf_token']

	s.headers.update({
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	"content-type" : "application/x-www-form-urlencoded"
	})

	payload = {
	"fuel_csrf_token": token,
	"back_url": "https://store.sacai.jp/cart",
	"login_id": email,
	"password": pw,
	"check_preserve_login": 1,
	"preserve_login_flag": 1
	}
	r = s.post(url,data=payload,timeout=TIMEOUT)
	if r.status_code == 200:
		try:
			j = s.get("https://store.sacai.jp/apis/customer.json",timeout=TIMEOUT).json()
			if j:
				if j["status"] == "success":
					log.info(j["customer"]["customer_id"])
					ecuu = j["customer"]["unique_code"]
					log.success("logged in!")
				else:
					log.warning("Error getCustomer")
					log.warning(j.json())
		except Exception as e:
			log.error("Error getCustomer")
			log.warning(e)
	else:
		print(r.status_code)
		print(r.url)
		with open("failed.html","w+",encoding="utf-8") as f:
			f.write(r.text)
	return s,ecuu

def enter(s,email,ecuu):
	log.info("Entering raffle.")
	#s.get("https://store.sacai.jp/item/detail/1_1_20-0216S_1/584")
	s.headers.update({
		"accept":"application/json, text/javascript, */*; q=0.01",
		"content-type":"application/x-www-form-urlencoded; charset=UTF-8",
		"referer":"https://store.sacai.jp/item/detail/1_1_20-0216S_1/584",
		"X-Requested-With":"XMLHttpRequest"
		})
	url = "https://store.sacai.jp/apis/apply/lottery/customer.json"
	s.cookies.set("ecuuc",ecuu)
	size_list = str(random.choice([8.5,9,9.5,10,10.5,11,11.5,12]))
	# for i in sizes[random.choice(["red","green"])]:
	for i in sizelist:
		if i["size"] == size_list:
			size = i["goods_id"]
	d = {
	"goods_id": size,
	"detail_disp_manage_code": "1_1_21-0322S_1"
	}
	res = s.post(url,data = d)
	if res.status_code == 200:
		q = res.json()
		if q["is_success"]:
			log.success("Entered.")
			log.success("Size: {}".format(size_list))
			with open("Entered.txt","a+",encoding="utf-8") as f:
				f.write(email+","+size_list+"\n")
		else:
			log.warning("Entry failed.")
			log.warning(q["errors"])
	else:
		log.warning("failed fetch entry json")
		log.warning(res.status_code)


if __name__ == "__main__":
	file=True
	init_log(file)

	try:
		plist = [i.replace("\n","") for i in open("proxies.txt").readlines()]
	except Exception as e:
		log.error("Error loading proxies.")
		log.error(e)
	try:
		accounts = [i.replace("\n","") for i in open("Accounts.txt","r").readlines()]
	except Exception as e:
		log.error("Error loading accounts.")
		log.error(e)
		sys.exit()
	global sizelist
	#TAN
	sizelist = json.load(open("v3.json","r",encoding="utf-8"))["colors"][1]["sizes"]

	TIMEOUT = 10
	for i in accounts:
		s,proxy=get_sess()
		email = i.split(":")[0]
		pw = i.split(":")[1]
		try:
			s,ecuu = login(s,proxy,email,pw)
			enter(s,email,ecuu)
		except:
			pass
		time.sleep(30)
