import requests,json
import random,brotli
import string,re,sys,time,traceback
from faker import Faker
import ctypes
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

from bs4 import BeautifulSoup as bs
from threading import Thread,Lock
import queue
import threading,signal
def signal_handler(signum, frame):
    exit_event.set()
exit_event = threading.Event()
def get_sleep():
	sleep = config["time_sleep"]
	if exit_event.wait(timeout=sleep):
		return
globallock=Lock()
LINK = "https://app.viralsweep.com/sweeps/full/d3f6f6-93713?framed=1"
SUBMIT_LINK = "https://app.viralsweep.com/promo/enter"
def load_users():
	return open("usernames.txt","r").readlines()
def load_ua():
	return open("user_agents.txt","r").readlines()
def get_email(fname,lname):
	user = load_users()
	p=random.choice(["jozomail.com","mailpanda.xyz","moonflares.com"])
	r = random.choice([1,2,3])
	if r == 1:
		#username4209@moonflares.com
		t = "{}{}{}@{}".format(random.choice(user).strip(),random.choice(["",".","!","-","_"]),random.choice([jig(4),''.join(random.choices(string.digits,k=3))]),p)
	elif r ==2:
		#lname.fname13409@moonflares.com
		t = "{}{}{}{}@{}".format(lname,random.choice(["",".","!","-","_"]),fname,random.choice([jig(4),''.join(random.choices(string.digits,k=5))]),p)
	elif r == 3:
		#fname4123lname@moonflares.com
		t = "{}{}{}@{}".format(fname,random.choice([jig(4),''.join(random.choices(string.digits,k=5))]),lname,p)
	return t.lower()
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

def enter(i=""):
	while not exit_event.is_set():
		iscomplete = False
		ua_list = load_ua()
		with requests.session() as s:
			fname = fake.first_name()
			lname = fake.last_name()
			if i:
				email = i
			else:
				#email = f"{fake.first_name().lower()}{fake.last_name().lower()}{''.join(random.choices(string.digits,k=4))}@{random.choice(['moonflares','jozomail'])}.com"
				email = get_email(fname,lname)
			#add = random.choice(config["address"])
			proxy = get_proxy()
			print(f"[{email}] Proxy: {proxy['http://']}")
			s.proxies.update(proxy)
			s.headers.update({
				"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"accept-encoding": "gzip, deflate, br",
				"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
				"sec-ch-ua": "'Chromium';v='92', 'Not A;Brand';v='99', 'Google Chrome';v='92'",
				"sec-ch-ua-mobile": "?0",
				"sec-fetch-dest": "document",
				"sec-fetch-mode": "navigate",
				"sec-fetch-site": "none",
				"sec-fetch-user": "?1",
				"upgrade-insecure-requests": "1",
				"user-agent": random.choice(ua_list).strip().replace("\"","")
				})
			size = random.choice([6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,13])
			phone = "907{}".format("".join(random.choices(string.digits,k=7)))
			payload = {
				"id":"d3f6f6-93713",
				"type":"full",
				"rfid":"",
				"cpid":"",
				"refer_source":"",
				"entry_source":LINK,
				"first_name":fname,
				"last_name":lname,
				"email": email,
				"email_again":"",
				"33039_1628983856":str(size)
			}
			s.headers.update({
				"accept": "*/*",
				"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
				"origin": "https://app.viralsweep.com",
				"referer": LINK,
				"x-requested-with": "XMLHttpRequest"
				})
			r2 = s.post(SUBMIT_LINK,data=payload)
			if r2.status_code == 200:
				try:
					#t = json.loads(brotli.decompress(r2.content))
					t=json.loads(r2.text)
					print(t)
				except:
					print("Failed to load json")
					traceback.print_exc()
				if t["success"]:
					print(f"[{email}] Entered! size: {size}")
					iscomplete=True
				else:
					print(f"[{email}] Unknown error")
					print(r2.text)
			else:
				print(r2.status_code)
				print(r2.text)
			return {"complete":iscomplete,"email":email}
				

def process(maxthread,amount,q):
	j = 0
	k = 0
	ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
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
						f.write(f"{result['email']}\n")
			get_sleep()
			ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
		except Exception:
			traceback.print_exc()
			q.put(1)
			get_sleep()

def process_out(maxthread,q):
	j = 0
	k = 0
	ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
	while q.qsize() > 0:
		try:
			try:
				i = q.get_nowait()
			except Exception:
				raise
			result = enter(i)
			with globallock:
				if result["complete"] == False:
					k+=1
					with open("Failed.txt","a+") as f:
						f.write(f"{result['email']}\n")
				else:
					j+=1
					with open("Entered.txt","a+") as f:
						f.write(f"{result['email']}\n")
				ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {maxthread} | Entered: {j} | Failed: {k}")
			get_sleep()		
		except Exception:
			traceback.print_exc()
			get_sleep()
			continue

def main(maxthread,amount,mode,emails):
	q = queue.Queue()
	if mode == "email":
		for i in emails:
			q.put(i)
		try:
			thread = Thread()
			for i in range(0,maxthread):
				Thread(target=process_out,args=(maxthread,q)).start()
		except KeyboardInterrupt:
			raise
	elif mode == "domain":
		for i in range(0,amount):
			q.put(1)
		try:
			for i in range(0,maxthread):
				t=Thread(target=process,args=(maxthread,amount,q)).start()
		except KeyboardInterrupt:
			exit_event.set()
			sys.exit()
if __name__ == '__main__':
	fake = Faker("en_us")
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
	mode = inquirer.select(
		message="Select mode:",
		choices = [{"name":"domain","value":"domain"},{"name":"email","value":"email"},{"name":"Exit","value":None}],
		pointer = ">",
		style=style,
		#set default location to top
		default = 0,
		).execute()
	emails=[]
	amount=0
	maxthread = config["maxthread"]
	if mode == "email":
		try:
			emails = [i.strip() for i in open("emails.txt").readlines()]
			print("emails loaded.")
		except Exception:
			print("Error loading emails.")
			traceback.print_exc()
			sys.exit()
	elif mode == "domain":
		amount = config["amount"]	
	main(maxthread,amount,mode,emails)