from imap_tools import MailBox, AND
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

ITEMS = []
G = Lock()
def save_file():
	if ITEMS:
		logging.info("found items")
		with G:
			with open("verify links","w+",encoding="utf-8") as f:
				json.dump(ITEMS,f)
	else:
		logging.info("Waiting for items.")

def save_accounts(email,pw):
	with G:
		with open("v_email_created.txt","a+") as f:
			f.write(f"{email}:{pw}\n")

class IMAP():
	def __init__(self):
		self.mb = None
		self.uids = []
		self.refresh_time = 30
		self.islogin = self.imap_worker()	
		if self.islogin:
			self.run()

	def imap_worker(self):
		logging.info("Logging in imap.")
		try:
			self.mb = MailBox(config["verifier"]["imap"])
			#mb = MailBox("lolololol")
			self.mb.login(config["verifier"]["login"]["user"],config["verifier"]["login"]["pw"],
				initial_folder=config["verifier"]["email_folder"])
		except Exception:
			logging.error("Error logging in imap.")
			traceback.print_exc()
			MAIN_EVENT.set()
			return
		return True

	def fetch(self):
		messages = self.mb.fetch(AND(subject="URL for membership registration procedure"),limit=20,bulk=True,reverse=True)
		for msg in messages:
			if "S_FETCHED" not in msg.flags:
				self.uids.append(msg.uid)
				email = msg.to[0]
				link = re.search(".+access_key.+",msg.text).group().strip()
				t={"email":email,"link":link}
				logging.info(t)
				with G:
					ITEMS.append(t)
		self.mb.flag(self.uids,["S_FETCHED"],True)

	def run(self):
		while not MAIN_EVENT.is_set():
			time.sleep(self.refresh_time)
			logging.info("Fetching")
			self.fetch()
			

def acc_creator(n):
	c=0
	found = False
	max_retries = 2
	retry_delay = 50
	logging.info(f"Creating {n}")
	s,email,pw = creator.do(n)
	if s is None:
		time.sleep(5)
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
						logging.info(f"[{email}] Link not found. Retrying({c})")			
				else:
					logging.info(f"[{email}] ITEMS empty. Retrying({c})")
		except Exception:
			traceback.print_exc()
	if found:
		logging.info(f"[{email}] Found link. Verifying")
		r = s.get(link)
		if "Thank you for registering" in r.text:
			logging.info(f"[{email}] ACCOUNT CREATED SUCCESSFULLY.")
		else:
			logging.info(f"[{email}] Account creation failed")
			print(r.text)
		save_accounts(email,pw)
		logging.info(f"[{email}] account saved.")
	time.sleep(config["task_delay"])
	return	




def main():
	global MAIN_EVENT,ITEMS
	MAIN_EVENT = threading.Event()
	threading.current_thread().name = "SACAI_APP"
	logging.info("starting worker threads.")
	t1 = Thread(target=IMAP,name="imap_worker",daemon=True)
	t1.start()
	logging.info(f"{t1.name} started.")
	sleep_time = 60.0
	t2 = RepeatedTimer("file_worker",sleep_time,save_file)
	logging.info(f"{t2.name} started.")
	with ThreadPoolExecutor(max_workers = 2, thread_name_prefix="TASK") as executor:
		executor.map(acc_creator,emails)
	logging.info("tasks finished")
	MAIN_EVENT.set()
	#time.sleep(20)
	while True:
		#only exits when signup threads completes
		if MAIN_EVENT.is_set():
			t1.join(5)
			t2.stop()
			break
if __name__ == "__main__":
	config = json.load(open("config.json","r",encoding="utf-8"))
	emails = [i.strip() for i in open("emails.txt","r").readlines()]
	#msecs is float and 0>3.0f round up and concantenate to 
	logging.basicConfig(style = "{",
		format="[{levelname}][{asctime}.{msecs:0>3.0f}][{threadName:<11}] {message}",
		datefmt="%H:%M:%S",level=logging.INFO)
	#main()
	main()

