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
import logger
#########################LOAD UTILS###################################
import json,traceback,re
import modules.scraper as scraper

def load_questions_from_file():
    try:
        with open("qlist.json", "r") as f:
            qlist = json.load(f)
        log.info("Questions loaded from qlist.json")
        return qlist
    except Exception:
        log.error("Error loading questions from qlist.json")
        log.warning(traceback.print_exc())
        return None

def display_answers(answer_list):
    log.info("Selected answers:")
    for q in answer_list:
        if "answer" in q:
            if q["type"] == "open_ended":
                log.info(f"Question: {q['qname']} | Answer: {q['answer']}")
            elif re.search(r"size", q["qname"]):
                log.info(f"Question: {q['qname']} | Size Range: {q['answer']}")
            elif q["type"] != "contact":
                log.info(f"Question: {q['qname']} | Answer: {q['answer']['name']}")
            else:
                log.info(f"Question: {q['qname']} | Contact information")

def main():
    log.info("Loading questions from qlist.json")
    qlist = load_questions_from_file()
    
    if not qlist:
        log.error("Error loading questions from qlist.json")
        sys.exit(1)
    
    log.info("Getting answers for questions")
    answers = scraper.get_ans(qlist)
    
    if answers:
        display_answers(answers)
        log.success("Answers processed successfully!")
    else:
        log.error("Failed to get answers")
        sys.exit(1)

if __name__ == '__main__':
    log = logger.setup_logger(name="offline_app")
    main() 