import os
import time
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from datetime import datetime as dt
import sys
import json
import areasearch



request_header = areasearch.request_header
domain = areasearch.domain
tablekey = ["時刻","天気","気温","湿度","降水量","風向"]

def urljoin(currenturl : str,suburl : str):
    urldir = currenturl[len(urlparse(currenturl).scheme)+3:].split("/")
    dirbacknum = suburl.count("../")
    absurl = urlparse(currenturl).scheme + "://" + "/".join(urldir[:-dirbacknum-1]) + "/" + suburl.replace("../","")
    return absurl

def get_soup(areaurlfortable : str):
    print("accessing:%s\r" % areaurlfortable,end="")
    entrance_requests = requests.get(areaurlfortable,headers=request_header)
    soup = bs(entrance_requests.content,'html.parser')
    return soup

def get_areaname(soup : bs):
    areaname = soup.find('div',id="cat-pass").find("p").contents[-1].replace(" ","").replace(">","").replace("\n","")
    return areaname

def get_datestr(soup : bs):
    datestr = soup.find("div",id="yjw_pinpoint_today").find("span").text.replace(' - ',"")
    return datestr

def getwt_1day(soup : bs,tomorrow = True):
    if tomorrow:
        dayid = "yjw_pinpoint_tomorrow"
    else:
        dayid = "yjw_pinpoint_today"
    tablewhilesp = soup.find("div",id=dayid).find_all("tr")
    tableobj = {}
    for rowsp in tablewhilesp:
        key = rowsp.find("small").text
        if "（" in key:
            unit = key[key.index("（") + 1:key.index("）")]
        else:
            unit = ""
        templist = []
        for val in rowsp.find_all("small")[1:]:
            valtext = val.text.replace(" ","")
            while "\n\n" in valtext:
                valtext = valtext.replace("\n\n","\n")
            valtext = valtext.replace("\n",",")
            if valtext.startswith(","):
                valtext = valtext[1:]
            if valtext.endswith(","):
                valtext = valtext[:-1]
            templist.append(valtext + " " + unit)
        tableobj[rowsp.find("small").text] = templist.copy()
    return tableobj

def get_weathertable_legacy(soup : bs,tomorrow = False):
    if tomorrow:
        dayid = "yjw_pinpoint_tomorrow"
    else:
        dayid = "yjw_pinpoint_today"
    tablewhilesp = soup.find("div",id=dayid).find_all("tr")
    tableobj = {}
    for rowsp in tablewhilesp:
        key = rowsp.find("small").text
        if "（" in key:
            unit = key[key.index("（") + 1:key.index("）")]
        else:
            unit = ""
        templist = []
        for val in rowsp.find_all("small")[1:]:
            valtext = val.text.replace(" ","")
            while "\n\n" in valtext:
                valtext = valtext.replace("\n\n","\n")
            valtext = valtext.replace("\n",",")
            if valtext.startswith(","):
                valtext = valtext[1:]
            if valtext.endswith(","):
                valtext = valtext[:-1]
            templist.append(valtext + " " + unit)
        tableobj[rowsp.find("small").text] = templist.copy()
    return tableobj

def get_weathertable(soup : bs):
    tabletoday = getwt_1day(soup,False)
    tabletomor = getwt_1day(soup,True)
    now_h = dt.now().hour + dt.now().minute / 60
    timezind = sorted(list(range(0,24,3)) + [now_h]).index(now_h) - 1
    tableobj = {}
    for key in tabletoday.keys():
        tableobj[key] = tabletoday[key][timezind:] + tabletomor[key][:timezind]
    return tableobj

if __name__ == "__main__":
    if "-area" in sys.argv:
        area_url = areasearch.getareacand_st(sys.argv[sys.argv.index("-area") + 1])[0]["url"]
    elif "-url" in sys.argv:
        area_url = sys.argv[sys.argv.index("-url") + 1]
    else:
        area_url = areasearch.getareaurl()
    soup = get_soup(area_url)
    areaname = get_areaname(soup)
    datestr = get_datestr(soup)
    weatherinfoobj = get_weathertable(soup)
    indent = " " * 10
    if "-o" in sys.argv:
        with open(sys.argv[sys.argv.index("-o") + 1],"w") as fw:
            json.dump({"areaname":areaname,"date":datestr,"table":weatherinfoobj},fw)
    else:
        for key in weatherinfoobj.keys():
            #print(key,":",",".join(weatherinfoobj[key]))
            for ind0 in range(len(weatherinfoobj[key])):
                ind1 = len(weatherinfoobj[key]) - 1 - ind0
                print(indent * ind1 + " " * 16 +weatherinfoobj[key][ind1] + "\r",end="")
            print(key)
