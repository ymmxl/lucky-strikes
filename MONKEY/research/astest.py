# # import time
# # import asyncio
# # async def do_some_work(x):
# #	 print("Waiting " + str(x))
# #	 await asyncio.sleep(x)
# # loop = asyncio.get_event_loop()
# # tasks = [asyncio.ensure_future(do_some_work(2)), 
# #		  asyncio.ensure_future(do_some_work(5))]
# # loop.run_until_complete(asyncio.gather(*tasks))



# import requests
# import time

# def print_book_name(index: int, isbn: int) -> str:
# 	response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
# 	response_dict = response.json()
# 	try:
# 		title = response_dict["items"][0]["volumeInfo"]["title"]
# 		print(f"{index}: {title}")
# 	except:
# 		pass

# def main():
# 	isbn_list = [
# 		9780007355143,
# 		9780008108298,
# 		9780547249643,
# 		9781405882583,
# 		9780316095860,
# 		9780930289232,
# 		9780486415871,
# 		9780765350381,
# 		9781716814655,
# 		9789898559425,
# 		9781944529024,
# 		9780765376671,
# 		9781400079988,
# 		9781438114026,
# 		9780393066258
# 	]
	
# 	start_time = time.monotonic()
# 	for index, isbn in enumerate(isbn_list):
# 		print_book_name(index, isbn)
 
# 	print(f"Time Taken:{time.monotonic() - start_time}")
	
# if __name__ == "__main__":
# 	main()

import asyncio,httpx,time
limits = httpx.Limits(max_keepalive_connections=5)

async def get_book_name(index: int,isbn:int) -> str:
	async with httpx.AsyncClient(limits=limits) as s:
		r = await s.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
		r = r.json()
		try:
			title = r["items"][0]["volumeInfo"]["title"]
			print(f"{index}: {title}")
		except:
			pass

async def main():
	isbn_list = [
	  9780007355143,
	  9780008108298,
	  9780547249643,
	  9781405882583,
	  9780316095860,
	  9780930289232,
	  9780486415871,
	  9780765350381,
	  9781716814655,
	  9789898559425,
	  9781944529024,
	  9780765376671,
	  9781400079988,
	  9781438114026,
	  9780393066258
  ]
	tasks = []
	for index,isbn in enumerate(isbn_list):
		tasks.append(get_book_name(index,isbn))
	await asyncio.gather(*tasks)

if __name__ == '__main__':
	start = time.monotonic()
	asyncio.run(main())
	print(f"Time Taken:{time.monotonic() - start}")
