from imap_tools import MailBox, AND
import imaplib
#catch imap error
from bs4 import BeautifulSoup as bs
import re,traceback
import logging,time
from threading import Timer,Thread, Lock
import threading
import json
from modules.repeatedtimer import RepeatedTimer
from concurrent.futures import ThreadPoolExecutor
import modules.creator as creator
import requests

#########################LOAD UTILS###################################
import sys,os
# insert at position 1 in the path, as 0 is the path of this file.
#sys.path.insert(1, '../utils/')
sys.path.append(os.path.abspath('../utils/'))
from tools import UTILS as ut
UTILS = ut('en_us')
import logger
#########################LOAD UTILS###################################

ITEMS = []
G = Lock()
def save_file():
	if ITEMS:
		log.info("found items")
		with G:
			with open("verify links","w+",encoding="utf-8") as f:
				json.dump(ITEMS,f)
	else:
		log.info("Waiting for items.")

def save_accounts(email,pw):
	with G:
		with open("v_created.txt","a+") as f:
			f.write(f"{email}:{pw}\n")

class IMAP():
	def __init__(self):
		self.mb = None
		self.uids = []
		self.refresh_time = 30
		self.d = self.imap_login()
		if self.d:
			self.run()

	def imap_login(self):
		log.info("Logging in imap.")
		try:
			self.mb = MailBox(config["verifier"]["imap"])
			#mb = MailBox("lolololol")
			self.mb.login(config["verifier"]["login"]["user"],config["verifier"]["login"]["pw"],
				initial_folder=config["verifier"]["email_folder"])
		except Exception:
			log.error("Error logging in imap.")
			traceback.print_exc()
			MAIN_EVENT.set()
			return
		log.info("Logged in.")
		return True

	def fetch(self):
		messages = self.mb.fetch(AND(subject="URL for membership registration procedure"),limit=20,bulk=True,reverse=True)
		for msg in messages:
			if "S_FETCHED" not in msg.flags:
				self.uids.append(msg.uid)
				email = msg.to[0]
				link = re.search(".+access_key.+",msg.text).group().strip()
				t={"email":email,"link":link}
				log.info(t)
				with G:
					ITEMS.append(t)
		self.mb.flag(self.uids,["S_FETCHED"],True)

	def run(self):
		while not MAIN_EVENT.is_set():
			try:
				time.sleep(self.refresh_time)
				log.info("Fetching")
				self.fetch()
			except imaplib.IMAP4.abort:
				#maybe timed out
				log.info("Refresh session.")
				self.imap_login()
				continue
			except Exception:
				log.error("Not imap error")
				log.warning(traceback.print_exc())
				break

def acc_creator(n):
	c=0
	found = False
	max_retries = 2
	retry_delay = 50
	log.info(f"Creating {n}")
	s,email,pw = creator.do(config["domain"],plist)
	if s is None:
		return
	while c < max_retries+1:
		c+=1
		if found:
			break
		time.sleep(retry_delay)
		try:
			with G:
				if ITEMS:
					for i in ITEMS:
						if email in i["email"]:
							link = i["link"]
							ITEMS.remove(i)
							found = True
					if not found:
						log.info(f"[{email}] Link not found. Retrying({c})")			
				else:
					log.info(f"[{email}] ITEMS empty. Retrying({c})")
		except Exception:
			log.warning(traceback.print_exc())
	if found:
		log.info(f"[{email}] Found link. Verifying")
		r = s.get(link)
		if "Thank you for registering" in r.text:
			log.info(f"[{email}] ACCOUNT CREATED SUCCESSFULLY.")
		else:
			log.info(f"[{email}] Account creation failed")
			print(r.text)
		save_accounts(email,pw)
		log.info(f"[{email}] account saved.")
	time.sleep(config["task_delay"])
	return	


def main():
	global MAIN_EVENT,ITEMS
	MAIN_EVENT = threading.Event()
	log.info("starting worker threads.")
	t1 = Thread(target=IMAP,name="IMAP",daemon=True)
	t1.start()
	log.info(f"{t1.name} started.")
	sleep_time = 60.0
	t2 = RepeatedTimer("FILER",sleep_time,save_file)
	log.info(f"{t2.name} started.")
	with ThreadPoolExecutor(max_workers = config["maxthread"], thread_name_prefix="TASK") as executor:
		executor.map(acc_creator,range(1,config["amount"]))
	log.info("tasks finished")
	MAIN_EVENT.set()
	#time.sleep(20)
	while True:
		#only exits when signup threads completes
		if MAIN_EVENT.is_set():
			t1.join(5)
			t2.stop()
			break
if __name__ == "__main__":
	log = logger.setup_logger(name="MAIN")
	threading.current_thread().name = "SACAI_APP"
	try:
		plist = [i.strip() for i in open("proxies.txt").readlines()]
		log.info("Proxies loaded")
	except Exception:
		log.error("Error loading proxies.")
		sys.exit()
		traceback.print_exc()
	try:
		config = json.load(open("config.json","r",encoding="utf-8"))
		log.info("config loaded.")
	except Exception:
		log.error("Error loading config.")
		traceback.print_exc()
		sys.exit()
	main()

