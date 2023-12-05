import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

areasearchurlbase = "https://weather.yahoo.co.jp/weather/search/?p=%s&t=p&b=%d"
domain = urlparse(areasearchurlbase).scheme + "://" + urlparse(areasearchurlbase).netloc
user_agent = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
request_header = {'User-Agent': user_agent}

def urljoin(currenturl : str,suburl : str):
    urldir = currenturl[len(urlparse(currenturl).scheme)+3:].split("/")
    dirbacknum = suburl.count("../")
    absurl = urlparse(currenturl).scheme + "://" + "/".join(urldir[:-dirbacknum-1]) + "/" + suburl.replace("../","")
    return absurl

def getareacand_st(partstrings : str):
    valind = 1
    loop0 = True
    tablevaluelist = []
    while loop0:
        areasearchurl = areasearchurlbase % (partstrings,valind)
        print("accessing:%s\r" % areasearchurl,end="")
        rq = requests.get(areasearchurl,headers=request_header)
        print("  dealing:%s\r" % areasearchurl,end="")
        wholesoup_tmp = bs(rq.content,'html.parser')
        if wholesoup_tmp.find("table",class_="yjw_table3"):
            wholesoup = bs(rq.content,'html.parser').find("table",class_="yjw_table3")
            areas_elem = wholesoup.find_all("a")
            for elemind in range(len(areas_elem)):
                elem = areas_elem[elemind]
                tablevaluelist.append({
                    "url":elem.attrs["href"],
                    "areaname":elem.text})
            valind += 50
        else:
            loop0 = False
    return tablevaluelist

def getareaurl():
    loop0 = True
    while loop0:
        partstrings = input("Input part strings of area > ")
        tablevaluelist = getareacand_st(partstrings)
        print("")
        for ind0 in range(len(tablevaluelist)):
            print("[%d]"%ind0,tablevaluelist[ind0]["areaname"])
        print("[%d]"%len(tablevaluelist),"back")
        loop1 = True
        while loop1:
            com = input(" > ")
            if com in list(map(str,range(len(tablevaluelist)))):
                outurl = tablevaluelist[int(com)]["url"]
                loop1 = False
            elif com == str(len(tablevaluelist)):
                outurl = ""
                loop1 = False
        if outurl:
            loop0 = False
    return outurl

def getareaurl_JP():
    loop0 = True
    while loop0:
        partstrings = input("地域名を入力してください > ")
        tablevaluelist = getareacand_st(partstrings)
        print("")
        for ind0 in range(len(tablevaluelist)):
            print("[%d]"%ind0,tablevaluelist[ind0]["areaname"])
        print("[%d]"%len(tablevaluelist),"戻る")
        loop1 = True
        while loop1:
            com = input(" > ")
            if com in list(map(str,range(len(tablevaluelist)))):
                outurl = tablevaluelist[int(com)]["url"]
                loop1 = False
            elif com == str(len(tablevaluelist)):
                outurl = ""
                loop1 = False
        if outurl:
            loop0 = False
    return outurl

if __name__ == "__main__":
    url = getareaurl_JP()
    print(url)