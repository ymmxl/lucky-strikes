import requests,time,sys
from bs4 import BeautifulSoup as bs
f = open("C:\\Users\\ymmxl\\Desktop\\outlook accounts.txt","r").readlines()
e = [i.split(":")[0] for i in f]
emails = [i.strip() for i in e]
for email in emails:
	if email:
		s = requests.session()
		LINK = "https://coptivitygen.com/"
		print("[{}] Get page".format(email))
		s.headers.update({
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"content-type": "application/x-www-form-urlencoded",
			"origin": "https://coptivitygen.com",
			"referer": "https://coptivitygen.com/",
			"sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
			})
		r = s.get(LINK)
		soup = bs(r.text,"html.parser")
		token = soup.find("meta",{"name":"csrf-token"}).attrs["content"]
		print(token)

		data = {
			"_token":token,
			"newsletter-email":email
		}
		r2 = s.post("https://coptivitygen.com/newsletter",data=data)
		if r2.status_code == 200:
			# if "subscribed successfully!" in r.text:
			# 	print("[{}] Subsribed.".format(email))
			# elif "already enrolled!" in r.text:
			# 	print("[{}] Already entered.".format(email))
			print("[{}] Subsribed.".format(email))
			with open("subbed.txt","a+") as f:
				f.write(email+"\n")
		else:
			print(r2.status_code)
		time.sleep(10)
