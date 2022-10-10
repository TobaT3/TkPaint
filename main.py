from glob import escape
import tkinter
from tkinter import BOTTOM, HORIZONTAL, TOP, colorchooser, filedialog, messagebox, font
from PIL import ImageGrab
import pathlib
import os, sys
import tkfontchooser

try:
    import pyi_splash
    pyi_splash.close()
except:
    pass #for pyisntaller

win = tkinter.Tk()
win.resizable(False, False)
win.title("TkPaint Canvas")

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

path_to_ico = os.path.abspath(os.path.join(bundle_dir, 'drawtk.ico'))

win.iconbitmap(path_to_ico) #couldnt get pyinstaller to package the thing in the exe so i gave up

c = tkinter.Canvas(win, height=500, width=700, highlightthickness=0,borderwidth=0)
c.pack()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
center_x = int(screen_width/2 - 700 / 2)
center_y = int(screen_height/2 - 500 / 2)
win.geometry(f'{700}x{500}+{center_x}+{center_y}')


mode = "rectangle"
x = 0
y = 0
xc1 = 0
xc2 = 0
xc3 = 0
yc1 = 0
yc2 = 0
yc3 = 0
clickc = 0
roundto = 50
ids = 0
idlist = []
linec = 0
linethicc = 1
getfirstpoint = True
drawingngon = False
text = ""
font = "Helvetica 15"
fontstr = "Helvetica 15"
textid = 999999999999
previewid = None
previewobj = None
preview = False
pwcoordc = 1 #preview coordinate count (eg. xc2,yc2 exist for triangles and stuff)

clickcs = []

exportlines = []

fillcolor = "#FFFFFF"
linecolor = "#000000"
isfilltransparent = True

def callback(e):
    global c,x,y, poslabel, snapp, roundto,xc1,yc1,xc2,yc2,previewid,ids,preview, linethicc, isfilltransparent, fillcolor, linecolor, pwcoordc, mode, idlist, previewid, drawingngon, previewobj, clickcs
    
    x = e.x
    y = e.y

    rx = round(x/roundto)*roundto
    ry = round(y/roundto)*roundto

    roundto = snapp.get()
    if roundto == 0:
        roundto=1
    linethicc = thicc.get()

    poslabel.config(text="snapped to "+str(round(x/roundto)*roundto)+"x, "+str(round(y/roundto)*roundto)+"y")
    #print("Pointer is currently at %d, %d" %(x,y))

    if preview == True:
        ids +=1
        c.delete(previewobj)
        previewobj = None
        if mode == "rectangle":
            if isfilltransparent == True:
                previewobj = c.create_rectangle(xc1,yc1,rx,ry, fill="", outline=linecolor, width=linethicc, dash=(5,2))
            elif isfilltransparent == False:
                previewobj = c.create_rectangle(xc1,yc1,rx,ry, fill=fillcolor, outline=linecolor, width=linethicc, dash=(5,2))
        if mode == "oval":
            if isfilltransparent == True:
                previewobj = c.create_oval(xc1,yc1,rx,ry, fill="", outline=linecolor, width=linethicc, dash=(5,2))
            elif isfilltransparent == False:
                previewobj = c.create_oval(xc1,yc1,rx,ry, fill=fillcolor, outline=linecolor, width=linethicc, dash=(5,2))
        if mode == "line":
            previewobj = c.create_line(xc1,yc1,rx,ry, fill=linecolor, width=linethicc, dash=(5,2))
        if mode == "triangle":
            if pwcoordc == 1:
                previewobj = c.create_line(xc1,yc1,rx,ry, fill=linecolor, width=linethicc, dash=(5,2))
            elif pwcoordc == 2:
                if isfilltransparent == True:
                    previewobj = c.create_polygon(xc1,yc1,xc2,yc2,rx,ry, fill="", width = linethicc, outline=linecolor, dash=(5,2))
                elif isfilltransparent == False:
                    previewobj = c.create_polygon(xc1,yc1,xc2,yc2,rx,ry, fill=fillcolor, width = linethicc, outline=linecolor, dash=(5,2))
        if mode == "ngon":
            if isfilltransparent == True:
                previewobj = c.create_polygon(clickcs,rx,ry, fill="", width=linethicc, outline=linecolor, dash=(5,2)) #sure it appears closed even if it isnt but a better solution with lines would have been way too complicated
            elif isfilltransparent == False:
                previewobj = c.create_polygon(clickcs,rx,ry, fill=fillcolor, width=linethicc, outline=linecolor, dash=(5,2)) #sure it appears closed even if it isnt but a better solution with lines would have been way too complicated


def click(e):
    global xc1,xc2,yc1,yc2,xc3,yc3,clickc,roundto, exportlines, ids, getfirstpoint, clickcs, drawingngon, linethicc, linec, thicc, textid, font, idlist, preview, pwcoordc,previewid
    
    clickc += 1
    pwcoordc += 1
    print("Clicked")

    if clickc == 1:
        xc1 = round(x/roundto)*roundto
        yc1 = round(y/roundto)*roundto
        preview = True
        c.delete(previewid)
    if clickc == 2:
        if mode == "ngon" and getfirstpoint == False:
            xc1 = xc2
            yc1 = yc2

        xc2 = round(x/roundto)*roundto
        yc2 = round(y/roundto)*roundto
        
        if mode=="triangle":
            escape
        elif mode =="ngon":
            clickc = 1
        else:
            clickc = 0
            preview = False
            pwcoordc = 0
            

        if mode == "rectangle":
            print(fillcolor, isfilltransparent)
            if isfilltransparent == True:
                ids += 1
                idlist.append(ids)
                c.delete(previewobj)
                c.create_rectangle(xc1,yc1,xc2,yc2, fill="", outline=linecolor, width=linethicc)
                exportlines.append("c.create_rectangle("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+", width="+str(linethicc)+",fill='', outline='"+linecolor+"')")
            elif isfilltransparent == False:
                ids += 1
                idlist.append(ids)
                c.delete(previewobj)
                c.create_rectangle(xc1,yc1,xc2,yc2, fill=fillcolor, outline=linecolor, width=linethicc)
                exportlines.append("c.create_rectangle("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+", width="+str(linethicc)+",fill='"+fillcolor+"', outline='"+linecolor+"')")
        if mode == "oval":
            if isfilltransparent == True:
                ids += 1
                idlist.append(ids)
                c.delete(previewobj)
                c.create_oval(xc1,yc1,xc2,yc2, fill="", outline=linecolor, width=linethicc)
                exportlines.append("c.create_oval("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+", width="+str(linethicc)+",fill='', outline='"+linecolor+"')")
            elif isfilltransparent == False:
                ids += 1
                idlist.append(ids)
                c.delete(previewobj)
                c.create_oval(xc1,yc1,xc2,yc2, fill=fillcolor, outline=linecolor, width=linethicc)
                exportlines.append("c.create_oval("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+", width="+str(linethicc)+",fill='"+fillcolor+"', outline='"+linecolor+"')")
        if mode == "line":
            ids += 1
            idlist.append(ids)
            c.delete(previewobj)
            c.create_line(xc1,yc1,xc2,yc2, fill=linecolor, width=linethicc)
            exportlines.append("c.create_line("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+", width="+str(linethicc)+", fill='"+linecolor+"')")

            

    if clickc == 3:
        linethicc = thicc.get()
        if mode == "triangle":
            ids += 1
            idlist.append(ids)
            c.delete(previewobj)
            clickc=0
            preview = False
            pwcoordc = 0

            xc3 = round(x/roundto)*roundto
            yc3 = round(y/roundto)*roundto

            if isfilltransparent == True:
                c.create_polygon(xc1,yc1,xc2,yc2,xc3,yc3, fill="", outline=linecolor, width=linethicc)
                exportlines.append("c.create_polygon("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+","+str(xc3)+","+str(yc3)+", fill='',outline='"+linecolor+"', width="+str(linethicc)+")")
            elif isfilltransparent == False:
                c.create_polygon(xc1,yc1,xc2,yc2,xc3,yc3, fill=fillcolor, outline=linecolor, width=linethicc)
                exportlines.append("c.create_polygon("+str(xc1)+","+str(yc1)+","+str(xc2)+","+str(yc2)+","+str(xc3)+","+str(yc3)+", fill='"+fillcolor+"',outline='"+linecolor+"', width="+str(linethicc)+")")
    
    if mode == 'ngon':

        rx = round(x/roundto)*roundto
        ry = round(y/roundto)*roundto

        if len(clickcs) >> 2: #to avoid an IndexError; could have done a try except but whatever
            print(clickcs[0], clickcs[1])
            print(x, y)
            if clickcs[0] == rx and clickcs[1] == ry:
                print("drawngon")

                ids += 1
                idlist.append(ids)

                if isfilltransparent == True:
                    test = c.create_polygon(clickcs, fill="", outline= linecolor, width=linethicc)
                    print(test)
                    exportlines.append("c.create_polygon("+str(clickcs)+", fill='', outline='"+linecolor+"', width="+str(linethicc)+")")
                elif isfilltransparent == False:
                    c.create_polygon(clickcs, fill=fillcolor, outline= linecolor, width=linethicc)
                    exportlines.append("c.create_polygon("+str(clickcs)+", fill='"+fillcolor+"', outline='"+linecolor+"', width="+str(linethicc)+")")

                c.delete(previewobj)

                preview = False
                pwcoordc = 0
                
                print("still drawngon")

                del clickcs [:]
                clickc = 0
                linec = 0
            else:
                clickcs.append(rx)
                clickcs.append(ry)
        else:
            print("error", clickcs)
            clickcs.append(rx)
            clickcs.append(ry)

    
    if mode == 'text':
        xc1 = round(x/roundto)*roundto
        yc1 = round(y/roundto)*roundto

        c.delete(textid)
        c.create_text(xc1,yc1,text=text, font=font)
        print(exportlines)
        ids += 1
        textid = ids

    if mode == 'delete': # thanks https://stackoverflow.com/questions/38982313/python-tkinter-identify-object-on-click
        
        delid = (c.find_closest(e.x, e.y)[0])
        if len(exportlines) > 1:
            exportlines.pop(delid-1)
        
        
        c.delete(delid)
        idinlist = idlist.index(delid)
        idinlist = idlist.pop(idinlist)

        print(exportlines)
        


def onKeyPress(event):
    global textid, text, idlist, ids, xc1,xc2, font
    
    if mode == "text":
        if event.keysym != "BackSpace":
            print("you pressed %s\n" % (event.char))
            text = text+event.char
        elif event.keysym == "BackSpace":
            print("backspace")
            text = text[:-1]

        c.delete(textid)
        c.create_text(xc1,yc1,text=text, font=font)
        ids += 1
        textid = ids

def drawngon():
    global ids, clickcs, fillcolor, linecolor, linethicc, c, linec, idlist,preview, clickc

    print("CLEARED clickcs", clickcs)
    
    print("end drawngon")
def donetext():
    global textid, text, idlist, ids, xc1,xc2, font, exportlines

    c.delete(textid)
    c.create_text(xc1,yc1,text=text, font=font)
    exportlines.append("c.create_text("+str(xc1)+','+str(yc1)+", text='"+text+"', font='"+str(font)+"')")
    ids += 1
    idlist.append(ids)
    preview = False
    textid = 999999
    text = ""



win.bind('<Motion>',callback)
win.bind("<Button-1>", click)
win.bind('<KeyPress>', onKeyPress)


def modedelete():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc, delobjbutton
    clickc = 0
    mode = "delete"
    print(mode)

    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#BDBDBD")

    if mode=="text":
        donetext()
        textwindow.destroy()
def moderectangle():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc, delobjbutton
    clickc = 0
    mode = "rectangle"
    print(mode)

    rectanglebutton.configure(bg="#BDBDBD")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#FFFFFF")

    if mode=="text":
        donetext()
        textwindow.destroy()
def modeoval():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc, delobjbutton
    clickc = 0
    mode = "oval"
    print(mode)
    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#BDBDBD")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#FFFFFF")

    if mode=="text":
        donetext()
        textwindow.destroy()
def modeline():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc, delobjbutton
    clickc = 0
    mode = "line"
    print(mode)
    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#BDBDBD")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#FFFFFF")

    if mode=="text":
        donetext()
        textwindow.destroy()
def modetriangle():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc, delobjbutton
    clickc = 0
    mode = "triangle"
    print(mode)
    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#BDBDBD")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#FFFFFF")

    if mode=="text":
        donetext()
        textwindow.destroy()
def modengon():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc,getfirstpoint, drawingngon, delobjbutton
    clickc = 0
    getfirstpoint = True
    mode = "ngon"

    print(mode)
    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#BDBDBD")
    textbutton.configure(bg="#FFFFFF")
    delobjbutton.configure(bg="#FFFFFF")

    if mode=="text":
        donetext()
        textwindow.destroy()
def modetext():
    global mode, rectanglebutton,ovalbutton,linebutton,trianglebutton,ngonbutton,clickc,getfirstpoint, drawingngon, toolwindow, textwindow, textwindow, delobjbutton
    clickc = 0
    mode = "text"

    createtextwindow()

    print(mode)
    rectanglebutton.configure(bg="#FFFFFF")
    ovalbutton.configure(bg="#FFFFFF")
    linebutton.configure(bg="#FFFFFF")
    trianglebutton.configure(bg="#FFFFFF")
    ngonbutton.configure(bg="#FFFFFF")
    textbutton.configure(bg='#BDBDBD')
    delobjbutton.configure(bg="#FFFFFF")

def fontchooser():
    global font, fontbutton

    font = tkfontchooser.askfont()

    font = tkinter.font.Font(root=None, family=font["family"], size=font["size"], weight=font["weight"], slant=font["slant"], underline=font["underline"], overstrike=font["overstrike"])

    print(font)

    fontstr = font["family"]+" "+str(font["size"])

    fontbutton.configure(text="Change font and size ("+fontstr+")")

def createtextwindow():
    global textwindow, fontbutton, fontstr

    textwindow = tkinter.Toplevel(toolwindow)
    textwindow.geometry("300x100")
    textwindow.title("Text")
    textwindow.resizable(False, False)
    textwindow.overrideredirect(True)

    x = toolwindow.winfo_x()
    y = toolwindow.winfo_y()
    textwindow.geometry(f'{300}x{60}+{x-300}+{y+235}')

    fontbutton = tkinter.Button(textwindow, text="Change font and size "+str(fontstr), command=fontchooser)
    fontbutton.pack()

    donebutton = tkinter.Button(textwindow, text="DONE", command=donetext)
    donebutton.pack()

    textwindow.bind('<KeyPress>', onKeyPress) # so you can type in both windows; annoyed me when you couldnt
    



def opencolorpick():
    global fillcolor,colpickbut
    
    fillcolor = colorchooser.askcolor(title ="Choose Fill Color")[1]
    colpickbut.configure(bg=fillcolor)
    print(fillcolor)
    print(type(fillcolor))
def opencolorpick2():
    global linecolor,colpickbut2
    
    linecolor = colorchooser.askcolor(title ="Choose Line Color")[1]
    colpickbut2.configure(bg=linecolor)
    print(linecolor)
def togglefilltransparent():
    global isfilltransparent,filltransparentbut
    
    if isfilltransparent == True:
        isfilltransparent = False

        filltransparentbut.configure(bg="#FFFFFF")
        filltransparentbut.config(text="Fill Transparent (F)")
    else:
        isfilltransparent = True

        filltransparentbut.configure(bg="#BDBDBD")
        filltransparentbut.config(text="Fill Transparent (T)")

def load():
    global ids, idlist, exportlines

    fp = filedialog.askopenfile(initialdir = pathlib.Path(__file__).parent.resolve(), title = "Open a DrawTk generated .py file", filetypes=[("Python file", ".py")], defaultextension=".py")

    i = 0
    
    for x in fp:
        i += 1

        if i > 6 and x != "tkinter.mainloop()":
            exec(x)
            exportlines.append(x)
            ids += 1
            idlist.append(ids)

def exportpy():

    fp = filedialog.asksaveasfile(initialdir = pathlib.Path(__file__).parent.resolve(), title = "Select a .py file to export to", filetypes=[("Python file", ".py")], defaultextension=".py")

    print('generating')
    #fp = open(filename, 'w')
    fp.write('#If you want to load this file make sure lines 1-6 are not modified\n')
    fp.write('\nimport tkinter')
    fp.write('\nc = tkinter.Canvas(height=500, width=700)')
    fp.write('\nc.pack()\n')
    
    for x in exportlines:
        print(x)
        fp.write('\n'+x)
    
    fp.write("\ntkinter.mainloop()")
    fp.write("\n#Made in DrawTk by TobaT3")

    fp.close()
    print('generated')


def exportpng():
    #Thanks to B.Jenkins on stack overflow for https://stackoverflow.com/a/38645917/15888488 (yes its like 6 years old but it still works)
    x=win.winfo_rootx()+c.winfo_x()
    y=win.winfo_rooty()+c.winfo_y()
    x1=x+c.winfo_width()
    y1=y+c.winfo_height()
    
    filename = filedialog.asksaveasfilename(initialdir = pathlib.Path(__file__).parent.resolve(), title = "Select an image file to export to", filetypes=[("PNG", ".png"), ("JPEG", ".jpeg"), ("TIFF", ".tiff"), ("BMP", ".bmp")], defaultextension=".png")
    ImageGrab.grab().crop((x,y,x1,y1)).save(filename)


#generate()

def undo():
    global ids, idlist, exportlines, c
    
    c.delete(idlist[len(idlist)-1])
    idlist.pop()
    exportlines.pop()

    print(exportlines, type(exportlines))
    print(ids, idlist)

def deleteall():
    global exportlines

    if messagebox.askokcancel("Are you sure?", "This will delete your canvas for ever (a long time)", icon = 'warning') == False:
        print("cancelled deleteall")
    else:
        c.delete("all")
        exportlines.clear()

toolwindow = tkinter.Toplevel(win)
toolwindow.geometry("300x700")
toolwindow.title("Toolbox")
toolwindow.resizable(False, False)

screen_width = toolwindow.winfo_screenwidth()
screen_height = toolwindow.winfo_screenheight()
center_x = int(screen_width/2 - 700 / 2)
center_y = int(screen_height/2 - 500 / 2)
toolwindow.geometry(f'{300}x{700}+{center_x-310}+{center_y}')

def movetoolwin(e):
    x = win.winfo_x()
    y = win.winfo_y()

    toolwindow.geometry(f'{300}x{700}+{x-310}+{y}')

    if mode == "text":
        x = toolwindow.winfo_x()
        y = toolwindow.winfo_y()
        textwindow.geometry(f'{300}x{60}+{x-300}+{y+235}')


win.bind('<Configure>', movetoolwin)

#lbl = tkinter.Label(toolwindow, text="I am in this toolwindow thing right").pack()

menu = tkinter.Menu(toolwindow)
toolwindow.configure(menu=menu)

filemenu = tkinter.Menu(menu)
filemenu.add_command(label="Load", command=load)
filemenu.add_separator()
filemenu.add_command(label="Save/Export to .py", command=exportpy)
filemenu.add_command(label="Export image", command=exportpng)
menu.add_cascade(label="File", menu=filemenu)

editmenu = tkinter.Menu(menu)
editmenu.add_command(label="Clear Canvas", command=deleteall)
menu.add_cascade(label="Edit", menu=editmenu)

poslabel = tkinter.Label(toolwindow, text="", font="Roboto 14")
poslabel.pack()

topgrid = tkinter.Frame(toolwindow)
topgrid.pack()

undobutton = tkinter.Button(topgrid, text="Undo", command=undo, bg="light green").grid(row=1,column=0)
delobjbutton = tkinter.Button(topgrid, text="Delete object", command=modedelete, bg="#FFFFFF")
delobjbutton.grid(row=1, column=1)


toolgrid = tkinter.Frame(toolwindow)
toolgrid.pack()


toollabel = tkinter.Label(toolgrid, text="Tools", font="Roboto 14").grid(row=0, column=0, columnspan=3)
rectanglebutton = tkinter.Button(toolgrid, text="Rectangle", command=moderectangle, bg="#BDBDBD")
rectanglebutton.grid(row=1, column=0)
ovalbutton = tkinter.Button(toolgrid, text="Oval", command=modeoval)
ovalbutton.grid(row=1, column=1)
linebutton = tkinter.Button(toolgrid, text="Line", command=modeline)
linebutton.grid(row=1, column=2)
trianglebutton = tkinter.Button(toolgrid, text="Triangle", command=modetriangle)
trianglebutton.grid(row=2, column=0)
ngonbutton = tkinter.Button(toolgrid, text="Polygon", command=modengon)
ngonbutton.grid(row=2, column=1)
textbutton = tkinter.Button(toolgrid, text="Text", command=modetext)
textbutton.grid(row=2, column=2)

colgrid = tkinter.Frame(toolwindow)
colgrid.pack()

collabel = tkinter.Label(colgrid, text="Colors and thickness", font="Roboto 14").grid(row=0,column=0,columnspan=3)
colpickbut = tkinter.Button(colgrid, text="Fill Color", command=opencolorpick, bg=fillcolor)
colpickbut.grid(row=1, column=0)

filltransparentbut = tkinter.Button(colgrid, text="Fill Transparent (T)", command=togglefilltransparent, bg=("#BDBDBD"))
filltransparentbut.grid(row=1, column=1)

colpickbut2 = tkinter.Button(colgrid, text="Line Color", command=opencolorpick2, bg=linecolor, fg="white")
colpickbut2.grid(row=1, column=2)

thicc = tkinter.Scale(colgrid, from_=1, to=75, orient=HORIZONTAL, tickinterval=10, length=200, label="Line Width", resolution=5)
thicc.grid(row=2,column=0,columnspan=3)

snapp = tkinter.Scale(colgrid, from_=0, to=200, orient=HORIZONTAL, length=200, label="Snapping (0 to turn off)", resolution=5)
snapp.grid(row=3,column=0,columnspan=3)
snapp.set(roundto)

#selobjframe = tkinter.Frame(toolwindow)
#selobjframe.pack()

#selobjname = tkinter.Label(selobjframe, text="Select object to edit it")
#selobjname.pack()

melabel = tkinter.Label(toolwindow, text="Made by TobaT3", font="Roboto 8").pack()


win.mainloop()
toolwindow.mainloop()