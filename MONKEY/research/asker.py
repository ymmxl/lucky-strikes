from InquirerPy import inquirer,prompt
from InquirerPy.separator import Separator
from InquirerPy import get_style
import re
from InquirerPy.validator import EmptyInputValidator,NumberValidator
style = get_style({
	"separator": '#6C6C6C',
	"questionmark": '#C33E1B bold',
	"pointer": '#FF9D00 bold',
	"answer": '#2196f3 bold',
	"question": 'white bold',
	"input":"green"
},style_override=False)


t=[{
	"qid": "686338994",
	"qtype": "single_choice_vertical",
	"qnum": "1",
	"qname": "What year were the first-ever modern Olympic games?",
	"optlist": ["1896","1912","1874","1956"]
    },
{
	"qid": "686338995",
	"qtype": "single_choice_vertical",
	"qnum": "2",
	"qname": "Who holds the record for most Olympic medals?",
	"optlist": ["Usain Bolt","Simone Biles","Michael Phelps","Ryan Lochte"]
    },
{
	"qid": "686338996",
	"qtype": "single_choice_vertical",
	"qnum": "3",
	"qname": "What’s the only country to have hosted the olympics three times?",
	"optlist": ["United Kingdom","Japan","U.S.A.","Russia"]
    },
{
	"qid": "686338997",
	"qtype": "single_choice_vertical",
	"qnum": "4",
	"qname": "What country hosted the first-ever Olympic games?",
	"optlist": ["Sweden","Greece","Russia","Spain"]
    },
{
	"qid": "686338992",
	"qtype": "single_choice_vertical",
	"qnum": "5",
	"qname": "What size shoes do you want?",
	"optlist": ["4","4.5","5","5.5","6","6.5","7","7.5","8","8.5","9","9.5","10","10.5","11","11.5","12","13","14","15"]
    },
{
	"qid": "686338993",
	"qtype": "contact",
	"qnum": "5",
	"qname": "Enter your shipping address and phone number. Only US addresses allowed. No PO Boxes.",
	"optlist": ""
    }
]

def	rs(t):
	asklist=[]
	qnums=[]
	answer=[]
	for i in t:
		if i["qtype"]=="contact":
			continue
		elif re.search(r"shoe|size",i["qname"]):
			q=inquirer.text(
			message=i["qname"]+"\n"+str(i["optlist"]),
			filter=lambda	result:	list(range(*[int(b)+c for c, b in enumerate(result.split('-'))]))
			)
		else:
			q=inquirer.select(
			message=i["qname"],
			choices=i["optlist"],
			pointer=">",
			style=style,
			#set default location to top
			default=0,
			)
		qnums.append("q{}".format(i["qnum"]))
		asklist.append(q)
	for	i,j	in zip(qnums,asklist):
	#	i	=	j.execute()
		answer.append({i:j.execute()})
	return answer

a=rs(t)
print(a)