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
#########################LOAD UTILS###################################
import csv,math
from bs4 import BeautifulSoup as bs
import math,random,time,json,string,traceback,sys,re
import asyncio,httpx
from concurrent.futures import ThreadPoolExecutor
from threading import Timer,Thread, Lock
import threading
import functools
SUPPORTED_TYPES: ["dropdown", "dropdown_matrix", "single_choice_horiz", "multiple_choice_horiz", "single_choice_matrix", "multiple_choice_matrix", "emoji", "net_promoter_score", "single_choice_vertical", "multiple_choice_vertical", "single_choice_vertical_two_col", "multiple_choice_vertical_two_col", "single_choice_vertical_three_col", "multiple_choice_vertical_three_col", "single_image_choice", "multiple_image_choice"]
limits = httpx.Limits(max_keepalive_connections=20)
import modules.scraper as scraper
import modules.fetcher as fetcher
import modules.enterer as enterer
glock = Lock()

def fetch(email,l):
	proxy = UTILS.get_proxy(plist)
	addy = random.choice(config["address"])
	log.info(f"[{email}] Fetching form")
	try:
		task = fetcher.process(l,proxy,addy,email)
	except:
		log.warning(traceback.print_exc())
	if task:
		log.success(f"[{email}] Task Built")
		with glock:
			tasks.append(task)
	else:
		return

def save_file(task,status):
	if status == "success":
		with glock:
			with open("entered.txt","a+",encoding="utf-8") as f:
				f.write(f"{task['email']}:{task['fname']} {task['lname']},{task['add1']},{task['city']}")
	elif status == "failed":
		with glock:
			with open("failed.txt","a+",encoding="utf-8") as f:
				f.write(f"{task['email']}:{task['fname']} {task['lname']},{task['add1']},{task['city']}")

def enter(t,anslist,l):
	p={}
	email = t["email"]
	rq = {}
	rq["question_info"] = {}
	relpos = None
		# task = {
		# "email":email
		# "fname":fname,
		# "lname":lname,
		# "add1":add1,
		# "add2":add2,
		# "city":city,
		# "state":state,
		# "postcode":postcode,
		# "phone":phone,
		# "data":{
		# 	"session":s,
		# 	"proxy":proxy,
		# 	"survey_data":survey_data,
		# 	"start_time":start_time
		# 	}
		# }
	log.info(f"[{email}] Processing")
	try:
		for i in anslist:
			if re.search(r"shoe|size",i["qname"]):
				index=None
				if i["answer"] == "all":
					ans = list(random.choice(i["optlist"]).values())[0]
				#filter new size list
				else:
					b1 = i["answer"][0]
					b2 = i["answer"][1]
					tmplist = [j for j in i["optlist"] if  b1 <= list(j.keys())[0] <= b2]
					#choose size
					ans = list(random.choice(tmplist).values())[0]
				for j,v in enumerate(i["optlist"]):
					if list(v.values())[0] == int(ans):
						index = j
				if not index:
					log.error(f"[{email}] q{i['number']} answer not found cond1")
					return
				relpos = scraper.calculateRelativePosition(index,i["type"],i["option_count"])
				p[i['qid'].split("_")[1]] = (None,ans)
			elif i["type"] != "contact":
				index = None
				ans = i["answer"]
				if i["optlist"]:
					for j,v in enumerate(i["optlist"]):
						if list(v.values())[0] == ans:
							index = j
					if not index:
						log.error(f"[{email}] q{i['number']} answer not found. cond2")
						return
					relpos = scraper.calculateRelativePosition(index,i["type"],i["option_count"])
				else:
					#open ended
					pass
				p[i['qid'].split("_")[1]] = (None,ans)
			else:
				#contact
				relpos = None
				p[i["optlist"]["name"]] = (None,f"{t['fname']} {t['lname']}")
				p[i["optlist"]["company"]] = (None,"")
				p[i["optlist"]["add1"]] = (None,t["add1"])
				p[i["optlist"]["add2"]] = (None,t["add2"])
				p[i["optlist"]["city"]] = (None,t["city"])
				p[i["optlist"]["state"]] = (None,t["state"])
				p[i["optlist"]["postcode"]] = (None,t["postcode"])
				p[i["optlist"]["email"]] = (None,t["email"])
				p[i["optlist"]["phone"]] = (None,t["phone"])
			f={
				"number":i["number"],
				"type":i["type"],
				"option_count":i["option_count"],
				"has_other":i["has_other"],
				"other_selected":i["other_selected"],
				"relative_position":relpos,
				"dimensions":i["dimensions"],
				"input_method":i["input_method"],
				"is_hybrid":i["is_hybrid"]
			}
			rq["question_info"][i['qid']] = f
		st = t["data"]["start_time"]
		en = int(time.time()*1000)
		q = {
		"tooltip_open_count": 0,
		"opened_tooltip": False,
		"start_time": st,
		"end_time": en,
		"time_spent": en-st,
		"previous_clicked": False,
		"has_backtracked": False,
		"bi_voice":{}
		}
		rq.update(q)
		p["survey_data"] = (None,t["data"]["survey_data"])
		p["response_quality_data"] = (None,json.dumps(rq))
		p["is_previous"] = (None,"false")
		p["disable_survey_buttons_on_submit"] = (None,"")
		log.info(f"[{email}] submitting")
		time.sleep(random.randint(1, 10))
		with t["data"]["session"] as s:
			s.proxies.update(t["data"]["proxy"])
			s.headers.update({
				"origin": "https://www.surveymonkey.com",
				"referer": l
				})
			r2 = s.post(l,files=p)
			if "survey-thanks" in str(r2.url):
				log.success(f"[{email}] ENTRY SUCCESSFUL.")
				save_file(t,"success")
			else:
				log.error(f"[{email}] ENTRY FAILED.")
				log.warning(f"[{email}] Status: {r2.status_code}")
				save_file(t,"failed")
				with glock:
					with open("failed submit.html","w+",encoding="utf-8") as f:
						f.write(r2.text)
	except Exception:
		log.warning(traceback.print_exc())
		log.error("Task entry error")
		time.sleep(10)
		return




def main():
	log.info("Init tasks")
	LINK = inquirer.text(message="Raffle Link?",style=style,default="https://www.surveymonkey.com/r/G5BJMPM").execute()
	log.info("Starting scraper worker")
	qlist = scraper.process(LINK)
	if not qlist:
		log.error("[Scraper] Error parsing questions.")
		sys.exit()
	else:
		with ThreadPoolExecutor(max_workers=config["max_threads"],thread_name_prefix="TASK") as executor:
			executor.map(functools.partial(fetch,l=LINK),emails)
		log.info(f"{len(tasks)}/{len(emails)} tasks loaded. Waiting for answer input.")
		answer = scraper.get_ans(qlist)
		if answer:
			with ThreadPoolExecutor(max_workers=config["max_threads"],thread_name_prefix="TASK") as ex:
				ex.map(functools.partial(enter,anslist=answer,l=LINK),tasks)
		else:
			log.error("Answer not found")
			sys.exit()

if __name__ == '__main__':
	global LINK
	UTILS = ut("en_us")
	tasks=[]
	log = logger.setup_logger(name="main")
	threading.current_thread().name = "MONKEY_APP"
	try:
		plist = [i.strip() for i in open("proxies.txt").read().strip().split("\n")]
		log.info("Proxies loaded")
	except Exception:
		log.error("Error loading proxies.")
		sys.exit()
		traceback.print_exc()
	try:
		config = json.load(open("config.json","r"))
		log.info("config loaded.")
	except Exception:
		log.error("Error loading config.")
		traceback.print_exc()
		sys.exit()
	try:
		emails = [i.strip() for i in open("emails.txt").read().strip().split("\n")]
		log.info(f"{len(emails)} emails loaded.")
	except Exception:
		log.error("Error loading emails.")
		traceback.print_exc()
		sys.exit()

	main()