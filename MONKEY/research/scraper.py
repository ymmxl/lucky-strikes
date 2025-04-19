import requests,time,sys,traceback,json
from bs4 import BeautifulSoup as bs
import csv,re,random,string
from faker import Faker
fake = Faker("en_us")
Faker.seed(0)
##############IMPORT ASKER####################
from InquirerPy import inquirer,prompt
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

def jig(n):
	return "".join(random.choices(string.ascii_uppercase + string.digits,k=n))
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

def build_form(anslist):
	try:
		config = json.load(open("config.json","r"))
		print("Config loaded.")
	except Exception:
		print("Error loading config.")
		traceback.print_exc()
		sys.exit()
	try:
		emails = [i.strip() for i in open("emails.txt").readlines()]
		print("Emails loaded.")
	except Exception:
		print("Error loading emails")
		traceback.print_exc()
		sys.exit()
		#["link","email","name","add1","add2","city","state","postcode","phone"]
	#get q len()
	with open("{}_tasks.csv".format(form_name),"a+",newline="") as f:
		writer = csv.writer(f)
		for email in emails:
			c = random.choice(config["address"])
			fname = c["fname"] if c["fname"] != "RANDOM" else fake.first_name()
			lname = c["lname"] if c["lname"] != "RANDOM" else fake.last_name()
			name = "{} {}".format(fname,lname)
			add1 = c["address1"].replace("##",jig(4)).replace("#suff#",jig_suffix())
			add2 = c["address2"].replace("#pre#",jig_prefix())
			city = c["city"]
			state = c["state"]
			postcode = c["zip"]
			phone = "7{}".format("".join(random.choices(string.digits,k=9)))
			r = [LINK,email,name,add1,add2,city,state,postcode,phone]
			#[{'q1': '1896'}, {'q2': 'Usain Bolt'}, {'q3': 'United Kingdom'}]
			for i in h[9:]:
				for j in anslist:
					for x,y in j.items():
						if i == x:
							if type(y) == list:
								y=random.choice(y)
							r.append(y)
			writer.writerow(r)

def get_ans(qlist):
	asklist=[]
	qnums=[]
	answer=[]
	for i in qlist:
		if i["qtype"] == "contact":
			continue
		elif i["qtype"] == "open_ended":
			q = inquirer.text(
				message=i["qname"],
				)			
		elif re.search(r"shoe|size",i["qname"]):
			q = inquirer.text(
				message=i["qname"]+"\n"+str(i["optlist"])+"ex: 4-9",
				filter=lambda result: list(range(*[int(b) + c  for c, b in enumerate(result.split('-'))]))
				)
		else:
			q = inquirer.select(
					message=i["qname"],
					choices = i["optlist"],
					pointer = ">",
					style=style,
					#set default location to top
					default = 0,
					)
		qnums.append("q{}".format(i["qnum"]))
		asklist.append(q)
	for i,j in zip(qnums,asklist):
		# i = j.execute()
		answer.append({i:j.execute()})
	return answer

def process(LINK):
	global h,form_name
	s = requests.session()
	s.headers.update({
	    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	    "accept-encoding": "gzip, deflate, br",
	    "accept-language": "en-GB,en;q=0.9",
	    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
	    "sec-ch-ua": "\"Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
	    "sec-ch-ua-mobile": "?0",
	    "upgrade-insecure-requests": "1",
	    "cache-control": "max-age=0"
	    })
	r = s.get(LINK)
	soup = bs(r.text,"html.parser")
	if "This survey is currently closed." in r.text:
		print("Survey is closed.")
		sys.exit()
	form = soup.find("form")
	if not form:
		print("form not found.")
		sys.exit()
	else:
		form_name = LINK.split(r"/")[-1]
		q=form.find_all(attrs={"data-rq-question-type":True})
		h = ["link","email","name","add1","add2","city","state","postcode","phone"]
		qlist=[]
		with open("{}-options.txt".format(form_name),"w+") as f:
			for i in q:
				qid = i.select_one("div[id|=question-field]").attrs["data-question-id"]
				qnum = i.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
				qtype = i.attrs["data-rq-question-type"]
				qname = i.select_one("span[class~=user-generated]").get_text(strip=True)
				optlist = []
				f.write("\nq{}\nqname:{}\nqid:{}\nqType:{}\n\n".format(qnum,qname,qid,qtype))
				if not qtype == "contact":
					#adds to header
					h.append("q{}".format(qnum))
				if qtype == "dropdown":				
					optlist = i.select_one("select").find_all("option")
					optlist = [j.text.strip() for j in optlist]
					f.write("options\n")
					for item in optlist:
						f.write(item+"\n")
					f.write("\n")
				if "single_choice" in qtype:
					inputs = i.find_all("input",{"type":"radio"})
					optlist = [j.find_next_sibling().get_text(strip=True) for j in inputs]
					f.write("options\n")
					for item in optlist:
						f.write(item+"\n")
				qlist.append({
				"qid":qid,
				"qtype":qtype,
				"qnum":qnum,
				"qname":qname,
				"optlist":optlist
				})
		with open("qlist.json","w+") as f:
			json.dump(qlist,f,indent=4)
		with open("{}_tasks.csv".format(form_name),"w+",newline="") as f:
			writer = csv.writer(f)
			writer.writerow(h)
		print("Done!")
		c = input("build form? (y/n)\n")
		flag = True
		while flag:
			if c == "y":
				flag = False
				ans = get_ans(qlist)
				build_form(ans)
			elif c == "n":
				flag = False
				print("Thank you")
				sys.exit()
			else:
				print("y/n only")	


def offline(LINK):
	global h,form_name
	form = bs(open("ccs_mock_form.html","r"),"html.parser")
	form_name = "test"
	q=form.find_all(attrs={"data-rq-question-type":True})
	h = ["link","email","name","add1","add2","city","state","postcode","phone"]
	qlist={}
	with open("{}-options.txt".format(form_name),"w+") as f:
		for i in q:
			qid = i.select_one("div[id|=question-field]").attrs["data-question-id"]
			qnum = i.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
			qtype = i.attrs["data-rq-question-type"]
			qname = i.select_one("span[class~=user-generated]").get_text(strip=True)
			f.write("\nq{}\nqname:{}\nqid:{}\nqType:{}\n\n".format(qnum,qname,qid,qtype))
			if not qtype == "contact":
					#adds to header
				h.append("q{}".format(qnum))
			if qtype == "dropdown":
				optlist = i.select_one("select").find_all("option")
				optlist = [j.text.strip() for j in optlist]
				f.write("options\n")
				for item in optlist:
					f.write(item+"\n")
				f.write("\n")
			if "single_choice" in qtype:
				inputs = i.find_all("input",{"type":"radio"})
				inputlist = [j.find_next_sibling().get_text(strip=True) for j in inputs]
				f.write("options\n")
				for item in inputlist:
					f.write(item+"\n")
			qlist[qnum] = {
				"qid":qid,
				"qtype":qtype,
				"qnum":qnum,
				"qname":qname,
				"optlist":optlist
				}
	with open("{}_tasks.csv".format(form_name),"w+",newline="") as f:
		writer = csv.writer(f)
		writer.writerow(h)
	print("Done!")
	c = input("build form? (y/n)\n")
	flag = True
	while flag:
		if c == "y":
			flag = False
			ans = get_anwsers(qlist)
			build_form(ans)
		elif c == "n":
			flag = False
			print("Thank you")
			sys.exit()
		else:
			print("y/n only")	




if __name__ == "__main__":
	global LINK
	LINK = input("Link?\n")
	#offline(LINK)
	process(LINK)