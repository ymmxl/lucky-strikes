import random,re,string
from capmonster_python import RecaptchaV2Task
from faker import Faker

class UTILS():
	# def __init__(self,fake="en_us"):
	# 	self.fake = Faker(fake)
	# 	Faker.seed(0)
	# @classmethod
	def __init__(self,faker_instance=""):
		self.fake = Faker(faker_instance)
	def jig(self,n):
		return "".join(random.choices(string.ascii_uppercase + string.digits,k=n))

	# @classmethod
	def get_email(self,fname,lname,domain: list) -> str:
		if fname == "random":
			fname = self.fake.first_name()
		if lname == "random":
			lname = self.fake.last_name()
		# if load_users:
		# 	user = self.load_users()
		if not type(domain) == list:
			raise
		p=random.choice(domain)
		r = random.choice([1,2,3])
		if r == 1:
			# if load_users:
			# 	#username4209@moonflares.com
			# 	t = "{}{}{}@{}".format(random.choice(user).strip(),random.choice(["",".","!","-","_"]),random.choice([jig(4),''.join(random.choices(string.digits,k=3))]),p)
			# else:
			# 	l = self.fake.user_name()
			# 	t = "{}@{}".format(l if l[-1].isdigit() else l+"".join(random.choices(string.digits,k=3)),p)
			l = self.fake.user_name()
			t = "{}@{}".format(l if l[-1].isdigit() else l+"".join(random.choices(string.digits,k=3)),p)
		elif r ==2:
			#lname.fname13409@moonflares.com
			t = "{}{}{}{}@{}".format(lname,random.choice(["",".","!","-","_"]),fname,random.choice([self.jig(4),''.join(random.choices(string.digits,k=5))]),p)
		elif r == 3:
			#fname4123lname@moonflares.com
			t = "{}{}{}@{}".format(fname,random.choice([self.jig(4),''.join(random.choices(string.digits,k=5))]),lname,p)
		return t.lower()

	def get_fname(self):
		if 'ja_jp' in self.fake.locales:
			return self.fake.first_romanized_name()
		else:
			return self.fake.first_name()

	def get_lname(self):
		if 'ja_jp' in self.fake.locales:
			return self.fake.last_romanized_name()
		else:
			return self.fake.last_name()
	def get_pw(self,n,symbol=True,y=""):
		p = list(string.ascii_letters+string.digits)
		if symbol:
			q = list("!#$%&()+-./:;<=>?@^_~")
			t = "{}{}".format(''.join(random.choices(p,k=n)),random.choice(q))
		else:
			t = "{}".format(''.join(random.choices(p,k=n)))
		if y == "SJS":
			if re.match(r"(.*[A-Z].*\d)",t):
				return t
			else:
				for i in range(10):
					t = "{}{}".format(''.join(random.choices(p,k=n)),random.choice(q))
					if re.match(r"(.*[A-Z].*\d)",t):
						return t
				print("Failed to gen pw")
				return
		return t

	def get_proxy(self,plist):
		p = random.choice(plist)
		p = p.strip().split(":")
		return {"http":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1]),"https":"http://{}:{}@{}:{}/".format(p[2],p[3],p[0],p[1])}

	def load_users(self):
		return open("usernames.txt","r").readlines()

	def load_ua(self,file):
		return open(file,"r").readlines()

	def jig_prefix(self):
		y="""Flat/Flt/Flat./Flt./apt #
		/House/Hse/H0USE/House./Hse./H0USE. #
		/Unit/Unit. #
		/Room/R00M/Room./R00M. #
		/Number./No./N./#"""
		t=y.strip().replace("\n","").split("/")
		return random.choice(t).strip()

	def jig_suffix(self):
		x="""Road/Rd/Road./Rd./R0AD
	    /Lane/Lne/Ln/Lane./Lne./Ln.
	    /Street/Stret/Strt/St/Street./Stret./Strt./St."""
		t=x.strip().replace("\n","").split("/")
		return random.choice(t).strip()

	def format_addy(self,addy,mode):
		UPS = ["APT","BSMT","BLDG","DEPT","FL","FRNT","HNGR","KEY","LBBY","LOT","LOWR","OFC","PH","PIER","REAR","RM","SIDE","SLIP","SPC","STOP","STE","TRLR","UNIT","UPPR"]
		UPS_jig = f"{random.choice(UPS)} {random.randint(10,99)}"
		#MAX 35 chars
		add1 = addy["address1"]
		add2 = addy["address2"]
		pat = re.compile("%var=.+?%")
		found = pat.findall(add1)
		#found
		if len(found) > 0:
			for i in found:
				add1 = add1.replace(i,random.choice(i.split("var=")[1].replace("%","").split(",")))
		found2 = pat.findall(add2)
		if len(found2) > 0:
			for i in found2:
				add2 = add2.replace(i,random.choice(i.split("var=")[1].replace("%","").split(",")))
		if mode == "2":
			x = add1.split(" ## ")
			lot = random.choice([0,1])
			if lot == 1:
				x.reverse()
			# add1 = ', '.join(x)
			add1 = f"{self.jig(4)} {', '.join(x)}"
			add2 = UPS_jig if not add2 else f"{add2} {UPS_jig}"
		if mode == "1":
			x = [add1.replace(" ## "," "),UPS_jig]
			lot = random.choice([0,1])
			if lot == 1:
				x.reverse()
			add1 = ' '.join(x)
		else:
			add1 = add1.replace("##",self.jig(4)).replace("#suff#",self.jig_suffix()).replace("#pre#",self.jig_prefix())
			add2 = add2.replace("##",self.jig(4)).replace("#suff#",self.jig_suffix()).replace("#pre#",self.jig_prefix())
		return add1,add2

	def get_captcha(self,email,APIKEY,SITEKEY,C_URL):
		try:
			capmonster = RecaptchaV2Task(APIKEY)
			taskId = capmonster.create_task(C_URL,SITEKEY)
			response = capmonster.join_task_result(taskId)
			return response.get("gRecaptchaResponse")
		except Exception as e:
			print(f"[{email}] Captcha exception:{e}")
			return