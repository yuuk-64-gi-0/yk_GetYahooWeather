import tkinter

def fontsizefrompixel(app : tkinter.Tk, pixel : int,fontname : None or str,testtext = "Test"):
    Label = tkinter.Label(app,bg="#ffffff")
    Label["text"] = testtext
    Label["font"] = (fontname,1)
    Label.place(x=0,y=int(app.geometry().split("+")[0].split("x")[1]))
    loop0 = True
    fontsize = 1
    while loop0:
        Label["font"] = (fontname,fontsize + 1)
        Label.update_idletasks()
        if Label.winfo_height() > pixel:
            loop0 = False
            return fontsize
        else:
            fontsize += 1
