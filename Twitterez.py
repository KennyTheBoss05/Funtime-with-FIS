import requests
url = "https://twitter135.p.rapidapi.com/Search/"

querystring = {"q":"Covid","count":"20"}

headers = {
	"X-RapidAPI-Key": "e9a5e3ecebmsh6212fa046ac197ep10d1a4jsna0b5fcf27d70",
	"X-RapidAPI-Host": "twitter135.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)