import requests,time,sys,traceback
from bs4 import BeautifulSoup as bs
import csv,re,random
def process(LINK):
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
		qlist = ["link","email"]
		with open("{}.txt".format(form_name),"w+") as f:
			for i in q:
				qid = "qid_"+i.select_one("div[id|=question-field]").attrs["data-question-id"]
				qnum = i.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
				qtype = i.attrs["data-rq-question-type"]
				qlist.append(qid)
				f.write("\n{}\nqType:{}\n\n".format(qid,qtype))
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
		with open("{}.csv".format(form_name),"w+") as f:
			writer = csv.writer(f)
			writer.writerow(qlist)
		print("Done!")

def build():
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
	with open("test.csv","a",newline="",encoding="UTF-8") as f:
		#skips headers
		reader = csv.reader(f)
		next(reader,None)
		#skips headers
		#get qname
		tmp = next(reader)
		link = tmp[0]
		email = tmp[1]
		for i,val in enumerate(tmp):
			if "name" in i.lower():

		if "name" in map(str.lower,tmp)
def offline():
	form = bs(open("ccs_mock_form.html","r"),"html.parser")
	form_name = "test"
	q=form.find_all(attrs={"data-rq-question-type":True})
	q_master = {}
	q_master["link"] = "link"
	q_master["email"] = "email"
	with open("{}-options.txt".format(form_name),"w+") as f:
		for i in q:
			qid = i.select_one("div[id|=question-field]").attrs["data-question-id"]
			qnum = i.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
			qtype = i.attrs["data-rq-question-type"]
			qname = i.select_one("span[class~=user-generated]").get_text(strip=True)
			f.write("\nq{}\nqname:{}\nqid:{}\nqType:{}\n\n".format(qnum,qname,qid,qtype))
			q_master[qid] = "q{}".format(qnum)
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
			if "contact" in qtype:
				#contact form does not require main qid
				q_master.pop(qid)
				qbody = i.select("div[class~=question-body]")[0]
				qbodylist = qbody.select("label[class~=answer-label]")
				contactOptions = {}
				f.write("options\n")
				for j in qbodylist:
					u = j.attrs["for"]
					o = j.get_text(strip=True)
					contactOptions[u] = o
					f.write("{}\n{}\n".format(o,u))	
					q_master[u]=o
	with open("{}.csv".format(form_name),"w+",newline="") as f:
		writer = csv.writer(f)
		writer.writerow(q_master.keys())
		writer.writerow(q_master.values())
	print("Done!")
	build_form = input("build form? (y/n)\n")
	flag = True
	while flag:
		if build_form == "y":
			flag = False
			build()
		elif build_form == "n":
			flag = False
			print("Thank you")
			sys.exit()
		else:
			print("y/n only")	
if __name__ == "__main__":
	#l = input("Link?\n")
	#process(l)
	offline()