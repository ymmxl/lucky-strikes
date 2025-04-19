import requests,json
import random
import string,re,sys,time,traceback
from faker import Faker
import ctypes
from bs4 import BeautifulSoup as bs
from threading import Thread,Lock
import queue
globallock=Lock()
LINK = "https://prodirect-mail.com/p/1D2I-QMV/womens-air-jordan-1-seafoam-raffle"

def get_proxy():
	p = random.choice(plist)
	p = p.split(":")
	return {"http://":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1]),"https://":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1])}
def jig_prefix():
	y="""Flat/Flt/Flat./Flt. #
	/Apartment/Appartment/Apartmentt/Appartmentt/Aparttment/Aparttment/Aparttmentt/Apartmente/Appartmente/Appt/Apt/Apptment/Aptment/Apartment./Appartment./Apartmentt./Appartmentt./Aparttment./Aparttment./Aparttmentt./Apartmente./Appartment./Appt./Apt./Apptment./Aptment. #
	/House/Hse/H0USE/House./Hse./H0USE. #
	/Concierge/Concierge Lounge/Concierge Room/Concierge Desk/Reception/Reception Lounge/Reception Room/Reception Desk/Front Desk/Lobby/Concierge./Concierge Lounge./Concierge Room./Concierge Desk./Reception./Reception Lounge./Reception Room./Reception Desk./Front Desk./Lobby./Concierge-Desk/Reception-Lounge/Reception-Room/Reception-Desk/Front-Desk/Concierge-Desk./Reception-Lounge./Reception-Room./Reception-Desk./Front-Desk.
	/Unit/Unit. #
	/Room/R00M/Room./R00M. #
	/Number./No./N./#"""
	t=y.strip().replace("\n","").split("/")
	return random.choice(t).strip()

def jig_suffix():
	x="""Road/Rd/Road./Rd./R0AD
    /Lane/Lne/Ln/Lane./Lne./Ln.
    /Street/Stret/Strt/St/Street./Stret./Strt./St."""
	t=x.strip().replace("\n","").split("/")
	return random.choice(t).strip()

def jig(n):
	return "".join(random.choices(string.ascii_uppercase + string.digits,k=n))

def enter():
	iscomplete = False
	with requests.session() as s:
		email = f"{fake.first_name().lower()}{fake.last_name().lower()}{''.join(random.choices(string.digits,k=4))}@jozomail.com"
		add = random.choice(config["address"])
		proxy = get_proxy()
		s.proxies.update(proxy)
		s.headers.update({
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-GB,en;q=0.9",
			"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",
			"sec-ch-ua-mobile": "?0",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
			})
		print(f"[{email}] Fetching.")
		r = s.get(LINK)
		soup = bs(r.text,"html.parser").find("form")
		SUBMIT_LINK = "https://prodirect-mail.com"+soup.attrs["action"]+"&random={}".format(str(random.random()))
		respondent = soup.find("input",{"name":"respondent"}).attrs["value"]
		size = random.choice([37,38,39,40,41,42,43,1,3,4])
		add1 = add["address1"]
		add2 = add["address2"]
		pat = re.compile("%var=.+?%")
		found = pat.findall(add1)
		#found
		if len(found) > 0:
			for i in found:
				add1 = add1.replace(i,random.choice(i.split("var=")[1].replace("%","").split(",")))
		found2 = pat.findall(add2)
		if len(found2) > 0:
			for i in found2:
				add2 = add2.replace(i,random.choice(i.split("var=")[1].replace("%","").split(",")))
		add1 = add1.replace("##",jig(4)).replace("#suff#",jig_suffix()).replace("#pre#",jig_prefix())
		add2 = add2.replace("##",jig(4)).replace("#suff#",jig_suffix()).replace("#pre#",jig_prefix())
		city = add["city"]
		state = add["state"]
		postcode = add["zip"]
		addy = f"{add1} {add2} {city} {postcode} {state}"
		payload = {
			"1": fake.first_name(),
			"2": fake.last_name(),
			"3": email,
			"14": "on",
			"17": addy,
			"18": str(size),
			"20": "",
			"23": "1",
			"defaultSubmitAction": "Complete",
			"respondent": respondent
		}
		slp = random.randint(15,30)
		print(f"[{email}] sleeping {slp}")
		time.sleep(slp)
		s.headers.update({
			"cache-control": "no-cache, no-store, max-age=0, must-revalidate",
			"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
			"origin": "https://prodirect-mail.com",
			"referer":LINK,
			})
		r2 = s.post(SUBMIT_LINK,data = payload)
		if r2.status_code == 200:		
			if "responseSaved=False" in r2.url:
				print(f"[{email}] Entered!")
				iscomplete=True
			else:
				print(f"[{email}] Unknown error")
		return {"complete":iscomplete,"email":email,"addy":addy}
			

def process(j,k,maxthread,amount,q):
	while q.qsize() > 0:
		try:
			try:
				q.get_nowait()
			except Exception:
				raise
			result = enter()
			
			if result["complete"] == False:
				k+=1
				with globallock:
					with open("Failed.txt","a+") as f:
						f.write(f"{result['email']}\n")
			else:
				j+=1
				with globallock:
					with open("Entered.txt","a+") as f:
						f.write(f"{result['email']},{result['addy']}\n")
			ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
		except Exception:
			traceback.print_exc()
			q.put(1)

def main(j,k,maxthread,amount):
	ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
	q = queue.Queue()
	for i in range(0,amount):
		q.put(1)
	try:
		for i in range(0,maxthread):
			Thread(target=process,args=(j,k,maxthread,amount,q)).start()
	except KeyboardInterrupt:
		raise
if __name__ == '__main__':
	fake = Faker("en_gb")
	j = 0
	k = 0	
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
	maxthread = config["maxthread"]
	amount = config["amount"]
	main(j,k,maxthread,amount)