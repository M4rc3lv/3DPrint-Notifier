#!/usr/bin/python3
import json
from urllib.request import Request, urlopen
import requests
import urllib
import time

SENDMAILURL="http://<yourdomain>/sendmail2.php"

Printers = [
 {"Naam":'MK4',"IP":'192.168.0.49', "Key":'hdpABCXhT4ZDfHpN', "IsPrinting":False, "IsMonitoring":False, "IsUploaded":False, "Filenaam":""},
 {"Naam":'Mini',"IP":'192.168.0.4', "Key":'XFMzbJACBDEzg2y', "IsPrinting":False, "IsMonitoring":False, "IsUploaded":False, "Filenaam":""}
]

def GetJobJson(p):
 try:
  headers = { 'X-Api-Key': p["Key"]}
  Req=Request("http://"+p["IP"]+"/api/job",headers=headers)
  with urlopen(Req) as response:
   Json = json.load(response)
  return Json
 except:
  return ""

def GetStatus(p):
 try:
  headers = { 'X-Api-Key': p["Key"] }
  Req=Request('http://'+p["IP"]+'/api/job',headers=headers)
  with urlopen(Req) as response:
   Json = json.load(response)
  return Json["state"]
 except Exception as e:
  return "Uit"

def Upload(p):
 try:
  Bestand=GetJobJson(p)["job"]["file"]["path"]
  Bestand="http://"+p["IP"]+"/thumb/l"+Bestand
  print(Bestand)
  #Download afbeelding vanaf printer
  h = { 'X-Api-Key': p["Key"] }
  Response = requests.get(Bestand,headers=h)
  with open("image"+p['Naam']+".png", 'wb') as f:
   f.write(Response.content)

  #Upload naar server
  print("== Upload ==")
  h = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
  url = "https://<your PHP Server>/upload.php"
  files = {'image': open("image"+p['Naam']+".png", 'rb')}
  data = {'upload': ''}
  Response = requests.post(url,data=data, files=files, timeout=20, headers=h)
  return True
 except Exception as e:
  print("Exceptie Upload(): ", end="")
  print(e)
  return False

while True:
 for p in Printers:
  Naam=p["Naam"];
  Stat=GetStatus(p)
  print(f"Status {Naam}: {Stat}")
  if Stat.startswith("Printing"):
   p["IsPrinting"]=True
   p["IsMonitoring"]=True
   JobJson=GetJobJson(p)
   p["Filenaam"]=JobJson["job"]["file"]["name"]
   if not p["IsUploaded"]:
    p["IsUploaded"]=Upload(p)
  else:
   p["IsPrinting"]=False

  if not p["IsPrinting"] and p["IsMonitoring"]:
   #Hij was aan het printen en nu niet meer dus is hij klaar
   url=SENDMAILURL+"?printernaam="+urllib.parse.quote(p["Naam"])+\
    "&bestandsnaam="+urllib.parse.quote(p["Filenaam"])+"&imagenaam="+urllib.parse.quote("image"+p['Naam']+".png")
   r = Request(url)
   urlopen(r)
   p["IsMonitoring"]=False

 time.sleep(5)

