import csv,random
tasks = csv.DictReader(open("tasks.csv","r",encoding="utf-8"), skipinitialspace=True)
sizeq = "q5"
sizes = [8,8.5,9,9.5,10,10.5,11,12]

for i in tasks:
	i[sizeq] = str(random.choice(sizes))

with open("tasks_n.csv","w+",encoding="utf-8") as f:
	writer = csv.DictWriter(f,fieldnames=["link","email","name","add1","add2","city","state","postcode","phone","q1","q2","q3"])
	writer.writerow(tasks)
