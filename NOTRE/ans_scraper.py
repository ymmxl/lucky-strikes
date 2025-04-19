import requests,json,time

def save_data(existing,data):
	if existing:
		for i in existing:
			if i["id"] == data["id"]:
				print("item exists, skipping")
				return
	with open("qlist.json","w+",encoding="utf-8") as g:
		existing.append(data)
		json.dump(existing,g,indent=4)
head = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
	"cache-control": "max-age=0",
	"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "\"Windows\"",
	"sec-fetch-dest": "document",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "none",
	"sec-fetch-user": "?1",
	"upgrade-insecure-requests": "1",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

def fetch(existing):
	try:
		r = requests.get("https://notreraffle.com/api/question-answers/random",headers=head)
		if r.status_code == 200:
			print("fetched")
			try:
				data = r.json()["qna"]
				print(data["id"])
				# did = data["id"]
				# question = data["question"]
				# options = data["options"]
				# answer = data["answer"]
				# created_at = data["created_at"]
				# updated_at = data["updated_at"]
				# key = data["key"]
				save_data(existing,data)
			except Exception as e:
				print("error with json fetched")
				print(e)
				print(data)
	except:
		print(r.status_code)
		print("Error in request")

	time.sleep(15)


for i in range(100):
	with open("qlist.json", "r") as f:
		existing = json.load(f)
	fetch(existing)