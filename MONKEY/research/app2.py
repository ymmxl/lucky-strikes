import requests,csv,math,re
from bs4 import BeautifulSoup as bs
import math,random,time,json,string,traceback,sys
SUPPORTED_TYPES: ["dropdown", "dropdown_matrix", "single_choice_horiz", "multiple_choice_horiz", "single_choice_matrix", "multiple_choice_matrix", "emoji", "net_promoter_score", "single_choice_vertical", "multiple_choice_vertical", "single_choice_vertical_two_col", "multiple_choice_vertical_two_col", "single_choice_vertical_three_col", "multiple_choice_vertical_three_col", "single_image_choice", "multiple_image_choice"]

def get_proxy():
	p = random.choice(plist)
	p = p.split(":")
	return {"http":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1]),"https":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1])}

def calculateDimensions(q,qtype,optcount):
	dimension = []
	if qtype in ["single_choice_horiz", "multiple_choice_horiz", "emoji", "net_promoter_score"]:
		dimension = [1,optcount]
	elif qtype in ["single_choice_vertical", "multiple_choice_vertical", "dropdown"]:
		dimension = [optcount,1]
	elif qtype in ["single_choice_vertical_two_col", "multiple_choice_vertical_two_col"]:
		dimension = [math.ceil(optcount/2),2]
	elif qtype in ["single_choice_vertical_three_col", "multiple_choice_vertical_three_col"]:
		dimension = [math.ceil(optcount/3),3]
	elif qtype in ["single_image_choice", "multiple_image_choice"]:
		dimension = [math.ceil(optcount/3),3]
	else:
		pass
	return dimension

def calculateRelativePosition(index,qtype,optcount):
	n = []
	if qtype in ["single_choice_horiz", "emoji", "net_promoter_score", "multiple_choice_horiz"]:
		n = [0,index]
	elif qtype in ["single_choice_vertical", "multiple_choice_vertical"]:
		n = [index,0]
	elif qtype in ["single_choice_vertical_two_col", "multiple_choice_vertical_two_col"]:
		s = math.ceil(optcount/2)
		n = [index % s,math.floor(index / s)]
	elif qtype in ["single_choice_vertical_three_col", "multiple_choice_vertical_three_col"]:
		s = math.ceil(optcount/3)
		n = [index % s,math.floor(index / s)]
	elif qtype in ["single_image_choice", "multiple_image_choice"]:
		n = [math.floor(optcount/3),index % 3]
	else:
		n = [index]
	return n	

def process_dropdown(q,qnum,qtype,task):
	s = []
	n = None
	ans = task["q{}".format(str(qnum))]
	options = q.select_one("select").find_all("option")
	#empty option header is needed
	optlist = [j.text.strip() for j in options]
	#dropdown matrix not supported yet
	#"other option" not supported yet	
	paired = {j.text.strip():j.attrs["value"] for j in options}
	try:
		o = optlist.index(ans)
		s = [[o,0]]
		input_id = paired[ans]
	except ValueError:
		print("Answer not found")
	return [s,n],input_id

def process_singleChoice(q,qnum,qtype,task):
	s=[]
	ans = task["q{}".format(str(qnum))]
	inputs = q.find_all("input",{"type":"radio"})
	paired = {j.find_next_sibling().get_text(strip=True):j.attrs["value"] for j in inputs}
	inputlist = [j.find_next_sibling().get_text(strip=True) for j in inputs]
	try:
		o = inputlist.index(ans)
		s = calculateRelativePosition(o,qtype,0)
		input_id = paired[ans]
	except ValueError:
		print("Anwser not Found")
		traceback.print_exc()
	
	return [s],input_id

def process_contact(q,qtype,task):
	s = {}
	qbody = q.select("div[class~=question-body]")[0]
	qbodylist = qbody.select("label[class~=answer-label]")
	paired = {j.get_text(strip=True):j.attrs["for"] for j in qbodylist}
	for k,v in paired.items():
		if "name" in k.lower():
			s[v] = task["name"]
		elif "company" in k.lower():
			s[v] = ""
		elif re.search(r"\baddress(?!email|2|street\b)",k.lower()):
			s[v] = task["add1"]
		elif re.search(r"\baddress(?!email\b)",k.lower()):
			s[v] = task["add2"]
		elif re.search(r"city|town",k.lower()):
			s[v] = task["city"]
		elif "state" in k.lower():
			s[v] = task["state"]
		elif re.search(r"zip|post",k.lower()):
			s[v] = task["postcode"]
		elif "email" in k.lower():
			s[v] = task["email"]
		elif "phone" in k.lower():
			s[v] = task["phone"]
	return s


def process_questions(rq,payload,q,task):
	done,optcount,relpos,dim,p,hybrid = False,None,None,None,None,False
	qid = "qid_{}".format(q.select_one("div[id|=question-field]").attrs["data-question-id"])
	qnum = q.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
	qtype = q.attrs["data-rq-question-type"]
	qname = q.select_one("span[class~=user-generated]").get_text(strip=True)
	optcount = max(len(q.select("input[type!=text]")),len(q.select("option")))
	dim = calculateDimensions(q,qtype,optcount)
	if "dropdown" in qtype:
		d,ansid = process_dropdown(q,qnum,qtype,task)
		if d[0]:
			relpos = d[0]
		else:
			return done
	elif "single" in qtype:
		d,ansid = process_singleChoice(q,qnum,qtype,task)
		if d[0]:
			relpos = d
		else:
			return done
	elif "contact" in qtype:
		contact = process_contact(q,qtype,task)

	if qtype == "open_ended":
		p = "text_typed"
		hybrid = True
		ansid = task["q{}".format(str(qnum))]

	tmp = {
		"number":int(qnum),
		"type":qtype,
		"option_count":optcount if optcount else None,
		"has_other":False,
		"other_selected":None,
		"relative_position":relpos,
		"dimensions":dim if dim else None,
		"input_method":p,
		"is_hybrid":hybrid
	}
	rq["question_info"][qid] = tmp
	if not qtype == "contact":
		payload[qid.split("_")[1]] = (None,ansid)
	else:
		for k,v in contact.items():
			payload[k] = (None,v)
	done = True
	return done
def process(task,plist):
	email = task["email"]
	s = requests.session()
	if plist:
		p = get_proxy()
		s.proxies.update(p)
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
	r = s.get(task["link"])
	soup = bs(r.text,"html.parser")
	if "This survey is currently closed." in r.text:
		print("Survey is closed.")
		sys.exit()
	form = soup.find("form")
	if not form:
		print("form not found.")
		sys.exit()

	form = bs(open("ccs_mock_form.html","r"),"html.parser")
	survey_data = form.find("input",id="survey_data").attrs["value"]
	# end = int(time.time()*1000)
	# time_spent = random.randint(40000,55000)
	# start = end - time_spent
	start = int(time.time()*1000)
	time_spent = random.randint(40000,55000)
	end = start + time_spent
	print(end)
	#parse questions
	qlist=form.find_all(attrs={"data-rq-question-type":True})
	rq = {}
	payload = {}
	rq["question_info"] = {}
	for q in qlist:
		d = process_questions(rq,payload,q,task)
		if not d:
			print("Task error. Skipping.")
			continue
	print(rq)
	b = {
	"tooltip_open_count": 0,
	"opened_tooltip": False,
	"start_time": start,
	"end_time": end,
	"time_spent": time_spent,
	"previous_clicked": False,
	"has_backtracked": False,
	"bi_voice":	{}
	}
	rq.update(b)
	print(json.dumps(payload,indent=4))
	sys.exit()
	c = {
	"survey_data":(None,survey_data),
	"response_quality_data":(None,json.dumps(rq)),
	"is_previous":(None,"false"),
	"disable_survey_buttons_on_submit":(None,""),	
	}
	payload.update(c)
	
	#POST Data
	s.headers.update({
	"origin": "https://www.surveymonkey.com",
	"referer": task["link"]
	})
	print("Sleeping")
	time.sleep(time_spent/1000)
	r2 = s.post(task["link"],files=payload)
	if "survey-thanks" in r2.url:
		print("Successfuly entered!")

	time.sleep(10)
	s.close()
if __name__ == '__main__':
	plist = []
	# try:
	# 	with open("proxies.txt","r",encoding="utf-8") as f:
	# 		plist = [i.strip() for i in f.readlines()]
	# 	print("Proxies loaded.")
	# except Exception:
	# 	print("Error loading proxies.")
	# 	traceback.print_exc()
	# 	pass
	try:
		tasks = csv.DictReader(open("tasks_test.csv","r",encoding="utf-8"), skipinitialspace=True)
		print("Tasks loaded.")
	except Exception:
		print("Error loading tasks.")
		traceback.print_exc()
		sys.exit()
	for task in tasks:
		print(task)
		process(task,plist)
	#process()