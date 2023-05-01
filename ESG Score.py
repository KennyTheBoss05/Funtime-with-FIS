import requests
import json
import pandas as pd
import math
f = open("esg.csv", "w")
f.truncate()
f.close()
url = "https://esg-environmental-social-governance-data.p.rapidapi.com/goals"
url2 = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"
company_name = []
esg_id = []
exchange_symbol = []
stock_symbol = []
goals = []
environment_grade = []
environment_level = []
social_grade = []
social_level = []
governance_grade = []
governance_level = []
total_grade = []
total_level = []
type = []
allq = ["Boeing","Airbus","Transport Corporation of India","Singapore airlines","Airbnb","Apple Inc.","Vodafone Group","Bharti Airtel","John Deere",
		"Cargill","Bechtel Corporation","Whiting-Turner","Pearson 1PSO","Byju's","Johnson & Johnson","Pfizer and Merck","Tyson Food Inc","PepsiCo",
		"Kaiser Permanente","Blue Cross Blue Shield","Marriott International","Hyatt Hotels Corporation","YouTube","Netflix","Facebook","Twitter",
		"Saudi Aramco","Shell","Volkswagen","Cardinal Health","Soundcloud","Spotify","Glencore PLC","Rio Tinto PLC","Amazon","Google","Samsung","Sony"]
types = ["Aerospace Industry","Transport Industry","Computer Industry"
,"Telecommunication industry","Agriculture industry","Construction Industry","Education Industry","Pharmaceutical Industry",
		 "Food Industry","Health care Industry","Hospitality Industry","Entertainment Industry","News Media Industry","Energy Industry","Manufacturing Industry",
		 "Music Industry","Mining Industry","Worldwide web","Electronics Industry"]
c=0
for q in allq:
	querystring = {"q":q}
	headers = {
		"X-RapidAPI-Key": "e9a5e3ecebmsh6212fa046ac197ep10d1a4jsna0b5fcf27d70",
		"X-RapidAPI-Host": "esg-environmental-social-governance-data.p.rapidapi.com"
	}

	response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
	print(response)
	if not len(response[0]) == 2:
		#for resp in response:
		type.append(types[int(math.floor(c / 2))])
		resp = response[0]
		company_name.append(resp["company_name"])
		esg_id.append(resp["esg_id"])
		if "exchange_symbol" in resp:
			exchange_symbol.append(resp["exchange_symbol"])
		else:
			exchange_symbol.append(" ")
		stock_symbol.append(resp["stock_symbol"])
		#goals.append(str(resp["goals"]))

		response2 = json.loads(requests.request("GET", url2, headers=headers, params=querystring).text)
		#for resp2 in response2:
		resp2 = response2[0]
		environment_grade.append(resp2["environment_grade"])
		environment_level.append(resp2["environment_level"])
		social_grade.append(resp2["social_grade"])
		social_level.append(resp2["social_level"])
		governance_grade.append(resp2["governance_grade"])
		governance_level.append(resp2["governance_level"])
		total_grade.append(resp2["total_grade"])
		total_level.append(resp2["total_level"])

	c = c+1

#"""
print(type)
print(company_name)
print(esg_id)
print(exchange_symbol)
print(stock_symbol)
#print(goals)
print(environment_grade)
print(environment_level)
print(social_grade)
print(social_level)
print(governance_grade)
print(governance_level)
print(total_grade)
print(total_level)
print("")
#"""
df0 = pd.DataFrame(type,columns=['type'])
df1 = pd.DataFrame(company_name,columns=['company_name'])
df2 = pd.DataFrame(esg_id,columns=['esg_id'])
df3 = pd.DataFrame(exchange_symbol,columns=['exchange_symbol'])
df4 = pd.DataFrame(stock_symbol,columns=['stock_symbol'])
#df5 = pd.DataFrame(goals,columns=['goals'])
df6 = pd.DataFrame(environment_grade,columns=['environment_grade'])
df7 = pd.DataFrame(environment_level,columns=['environment_level'])
df8 = pd.DataFrame(social_grade,columns=['social_grade'])
df9 = pd.DataFrame(social_level,columns=['social_level'])
df10 = pd.DataFrame(governance_grade,columns=['governance_grade'])
df11 = pd.DataFrame(governance_level,columns=['governance_level'])
df12 = pd.DataFrame(total_grade,columns=['total_grade'])
df13 = pd.DataFrame(total_level,columns=['total_level'])

df = pd.concat([df0,df1,df2,df3,df4,df6,df7,df8,df9,df10,df11,df12,df13],axis=1)
df.to_csv("esg.csv",mode = 'a',index = False,header = True)

#print(response)
#print(type(response))
#print(response2)
#print(type(response2))
