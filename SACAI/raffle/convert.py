import json5
import json

t = json5.loads(open("v2.json","r",encoding="utf-8").read())

with open("v3.json","w+",encoding="utf-8") as f:
	json.dump(t,f,indent=4)