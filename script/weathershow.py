import tkinter, time, sys, json, os
from tkinter import ttk
import yjwcast as yc
import subprocess as sp
import tkinter.font
import getfontsize as gfs

launchtime = time.time()
rundelay = 10
weatherinfojsonpath = os.path.join("..","jsondata","tables_%d.json" % os.getpid())#"..\\jsondata\\tables.json"
#targetarea = "千代田区"
area_url = yc.areasearch.getareaurl_JP()

def windowdestroy():
    global app_0
    global prc
    app_0.after_cancel(renewafter)
    app_0.after_cancel(dlafter)
    app_0.after_cancel(impafter)
    app_0.destroy()
    print("waiting subprocess (pid:%d)" % prc.pid)
    prc.wait()
    if os.path.isfile(weatherinfojsonpath):
        try:
            os.remove(weatherinfojsonpath)
        except:
            pass
    print("Windowdestroy")
    exit()

if sys.argv[-1].isdecimal():
    windowheight = int(sys.argv[-1])
else:
    windowheight = 220
myselfpath = os.path.abspath(sys.argv[0])
print(myselfpath)

zoomrate = windowheight / 360
windowwidth = int(1660 * zoomrate)
fontname = ['system','Yu Gothic','Terminal'][1]
app_0 = tkinter.Tk()
app_0.title("weather_yk")
app_0.geometry(str(windowwidth) + "x" + str(windowheight))
style = ttk.Style(app_0)
fontsize = gfs.fontsizefrompixel(app_0,int(40 * zoomrate),fontname,"起動中")#int(19 * (zoomrate ** 0.5))
style.configure("Treeview", rowheight=50,font=(fontname, fontsize))
fixed_map = lambda option:[elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
basestrcolor = "#000000"
bgcolor = "#ffffff"
canvas_mainback = tkinter.Canvas(app_0,width = windowwidth,height = windowheight,bg = bgcolor)
canvas_mainback.place(x = 0,y = 0)

tablelabelarray = []
pos_y = [0,45,90,180,225,270,315]#area,time,weth,temp,wet,rain,wind
for rowind in range(7):
    tablelabelarray.append([tkinter.Label(app_0,font=(fontname,fontsize),foreground=basestrcolor,background=bgcolor)])
    tablelabelarray[rowind][0].place(x=0,y=int(pos_y[rowind] * zoomrate))
    for colind in range(8):
        tablelabelarray[rowind].append(tkinter.Label(app_0,font=(fontname,fontsize),foreground=basestrcolor,background=bgcolor))
        tablelabelarray[rowind][colind + 1].place(x=int((220 + colind * 180) * zoomrate),y=int(pos_y[rowind] * zoomrate))
#area_url = yc.areasearch.getareacand_st(targetarea)[0]["url"]
soup = yc.get_soup(area_url)
areaname = yc.get_areaname(soup)
datestr = yc.get_datestr(soup)
yjwtable = yc.get_weathertable(soup)
datasource = {"areaname":areaname,"date":datestr,"table":yjwtable}
tablelabelarray[0][0]["text"] = datasource["areaname"]
tablelabelarray[0][1]["text"] = datasource["date"]
datatable = datasource["table"]
for keytop in yc.tablekey:
    ind0 = yc.tablekey.index(keytop) + 1
    key = [truekey for truekey in datatable.keys() if keytop in truekey][0]
    inslist = [key] + datatable[key]
    for ind1 in range(len(inslist)):
        tablelabelarray[ind0][ind1]["text"] = inslist[ind1]

prc = sp.Popen(":",shell=True)
dummypid = prc.pid
def infodownload():
    global app_0
    global prc
    global dlafter
    rundir = os.getcwd()
    os.chdir(os.path.dirname(myselfpath))
    interval = 1000 * 20
    dlafter = app_0.after(interval,infodownload)
    savepath = weatherinfojsonpath
    if type(prc.poll()) == int:
        #prc = sp.Popen(["python3","yjwcast.py","-area",targetarea,"-o",savepath])
        prc = sp.Popen(["python3","yjwcast.py","-url",area_url,"-o",savepath])
    os.chdir(rundir)
infodownload()

def infoimport():
    global app_0
    global impafter
    global datasource
    global prc
    rundir = os.getcwd()
    os.chdir(os.path.dirname(myselfpath))
    interval = 1000 * 10
    impafter = app_0.after(interval,infoimport)
    infopath = weatherinfojsonpath
    if os.path.isfile(infopath) and prc.pid != dummypid:
        with open(infopath,"r",encoding='utf-8') as fr:
            datasource = json.load(fr)
    os.chdir(rundir)
infoimport()

def tabelrenew():
    global app_0
    global renewafter
    global tablelabelarray
    funcinterval = 5000
    renewafter = app_0.after(funcinterval,tabelrenew)
    if time.time() - launchtime > rundelay:
        tablelabelarray[0][0]["text"] = datasource["areaname"]
        tablelabelarray[0][1]["text"] = datasource["date"]
        datatable = datasource["table"]
        for keytop in yc.tablekey:
            ind0 = yc.tablekey.index(keytop) + 1
            key = [truekey for truekey in datatable.keys() if keytop in truekey][0]
            inslist = [key] + datatable[key]
            for ind1 in range(len(inslist)):
                tablelabelarray[ind0][ind1]["text"] = inslist[ind1]
tabelrenew()

app_0.protocol("WM_DELETE_WINDOW", windowdestroy)
print("Window ready")
app_0.mainloop()