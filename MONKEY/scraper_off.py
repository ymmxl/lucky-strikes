import requests
import logging
import traceback
import json,sys,os,math,re
from bs4 import BeautifulSoup as bs
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
log = logging.getLogger(__name__)
def calculateDimensions(q,qtype,optcount):
	try:
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
	except Exception:
		log.error(f"calculateDimensions Error")
		log.warning(traceback.print_exc())

def calculateRelativePosition(index,qtype,optcount):
	try:
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
		return [n]	
	except Exception:
		log.error(f"calculateRelativePosition Error")
		log.warning(traceback.print_exc())

def process_dropdown(q):
	try:	
		s = []
		n = None
		# ans = task["q{}".format(str(qnum))]
		options = q.select_one("select").find_all("option")
		#empty option header is needed
		optlist = [j.text.strip() for j in options]
		#dropdown matrix not supported yet
		#"other option" not supported yet	
		# paired = [{j.text.strip():int(j.attrs["value"])} for j in options]
		paired = []
		for j,k in enumerate(options):
			p={
			"name":k.text.strip(),
			"value":k.attrs["value"],
			"pos":j
			}
			paired.append(p)
		
		#{opt1:val1,opt2:val2}
		# try:
		# 	o = optlist.index(ans)
		# 	s = [[o,0]]
		# 	input_id = paired[ans]
		# except ValueError:
		# 	print(f"[{task['email']}] Dropdown answer not found")
		# 	raise
		# return [s,n],input_id
		return paired
	except Exception:
		log.error(f"process_dropdown Error")
		log.warning(traceback.print_exc())

def process_singleChoice(q,qnum,qtype):
	try:
		# ans = task["q{}".format(str(qnum))]
		inputs = q.find_all("input",{"type":"radio"})
		paired = []
		for j,k in enumerate(inputs):
			p={
			"name":k.find_next_sibling().get_text(strip=True),
			"value":k.attrs["value"],
			"pos":j
			}
			paired.append(p)
		
		# inputlist = [j.find_next_sibling().get_text(strip=True) for j in inputs]
		# try:
		# 	o = inputlist.index(ans)
		# 	s = await calculateRelativePosition(o,qtype,0)
		# 	input_id = paired[ans]
		# except ValueError:
		# 	print(f"[{task['email']}] SChoice answer not Found")
		# 	traceback.print_exc()()
		# 	raise
		
		# return [s],input_id
		return paired
	except Exception:
		log.error(f"process_singleChoice Error")
		log.warning(traceback.print_exc())

def process_contact(q):
	try:
		s = {}
		qbody = q.select("div[class~=question-body]")[0]
		qbodylist = qbody.select("label[class~=answer-label]")
		paired = {' '.join(j.get_text().lower().split()):j.attrs["for"] for j in qbodylist}
		for k,v in paired.items():
			print(k,v)
			if "name" in k:
				s["name"] = v
			elif "company" in k:
				s["company"] = v
			elif re.search(r"(?<!email )address (?=\*)(?!2)",k):
				#matches address *
				s["add1"] = v
			elif re.search(r"(?<!email )address (?=2)(?!\*)",k):
				s["add2"] = v
			elif re.search(r"city|town",k):
				s["city"] = v
			elif "state" in k:
				s["state"] = v
			elif re.search(r"zip|post",k):
				s["postcode"] = v
			elif "email" in k:
				s["email"] = v
			elif "phone" in k:
				s["phone"] = v
		return s
	except Exception:
		log.error(f"process_contact Error")
		log.warning(traceback.print_exc())

def process_questions(q):
	try:
		done,optcount,relpos,dim,p,hybrid = False,None,None,None,None,False
		qid = "qid_{}".format(q.select_one("div[id|=question-field]").attrs["data-question-id"])
		qnum = q.select_one("div[id|=question-field]").attrs["data-qdispnumber"]
		qtype = q.attrs["data-rq-question-type"]
		qname = q.select_one("span[class~=user-generated]").get_text(strip=True)
		optcount = max(len(q.select("input[type!=text]")),len(q.select("option")))
		dim = calculateDimensions(q,qtype,optcount)
		#process according to qtype
		if "dropdown" in qtype:
			#[{opt1:value1},{opt2:value2}]
			optlist = process_dropdown(q)
		elif "single" in qtype:
			#[{opt1:value1},{opt2:value2}]
			optlist = process_singleChoice(q,qnum,qtype)
		elif "contact" in qtype:
			#order:name,company,add1,add2,city,state,postcode,email,phone	
			optlist = process_contact(q)
		if qtype == "open_ended":
			p = "text_typed"
			hybrid = True
			optlist=None
			# ansid = task["q{}".format(str(qnum))]
		tmp = {
			"qid":qid,
			"number":int(qnum),
			"qname":qname,
			"type":qtype,
			"option_count":optcount if optcount else None,
			"has_other":False,
			"other_selected":None,
			"relative_position":relpos,
			"dimensions":dim if dim else None,
			"input_method":p,
			"is_hybrid":hybrid,
			"optlist": optlist
		}
		return tmp
	except Exception:
		log.error(f"process_questions Error")
		log.warning(traceback.print_exc())

def get_ans(qlist):
	asklist=[]
	qnums=[]
	try:
		for i in qlist:
			if i["type"] == "contact":
				continue
			elif i["type"] == "open_ended":
				q = inquirer.text(
					message=i["qname"],
					).execute()
			elif re.search(r"size",i["qname"]):
				q = inquirer.text(
					message=f"{i['qname']}\n{','.join(j["name"] for j in i['optlist'])}\nex: 4-9\npress ENTER for all",
					default="all",
					filter=lambda result: result.split("-") if result != "all" else result,
					).execute()
			else:
				q = inquirer.select(
						message=i["qname"],
						choices = [{'name':j["name"],'value':j} for j in i["optlist"]],
						pointer = ">",
						style=style,
						#set default location to top
						default = 0,
						).execute()
			i["answer"] = q
	except Exception as e:
		log.error("Error getting answer")
		traceback.print_exc()()
		return None
		#############################################
	# 	qnums.append(f"q{i['qnum']}")
	# 	asklist.append(q)
	# for i,j in zip(qnums,asklist):
	# 	# i = j.execute()
	# 	answer.append({i:j.execute()})
	return qlist

def process():
	try:
		soup = bs(open("211123 new raffle","r",encoding="utf-8"),"html.parser")
		form = soup.find("form")
		if not form:
			log.info("form not found.")
			return None
		else:
			# q=form.find_all(attrs={"data-rq-question-type":True})
			# qlist=[]
			# for i in q:
			# 	d = process_questions(i)
			# 	qlist.append(d)
			# 	if not d:
			# 		log.error("Scraper Error parsing question")
			# 		return
			# with open("qlist.json","w+") as f:
			# 	json.dump(qlist,f,indent=4)
			# log.info("Done!")
			# return qlist
			q=form.find_all(attrs={"data-rq-question-type":True})
			for i in q:
				qtype = i.attrs["data-rq-question-type"]
				if "single" in qtype:
					# qbody = i.select("div[class~=question-body]")[0]
					# qbodylist = i.select("label[class~=answer-label]")	
					# for j in qbodylist:
					# 	print(repr(' '.join(j.get_text().lower().split())))		
					qnum = i.select_one("div[id|=question-field]").attrs["data-qdispnumber"]	
					s=process_singleChoice(i,qnum,qtype)
					print(s)
	except Exception:
		log.error(f"process Error")
		log.warning(traceback.print_exc())

if __name__ == '__main__':
	#LINK = input("Link?\n")
	process()