# %%
#ui
import tkinter as tk
from tkinter import *
import tkmacosx as tkm

#clicking
import pyautogui

#keybinds
import keyboard

#other
import time
import threading
import subprocess
import json

# %%
#put window on top
def ontop():
    if (topcheckval.get() == 0): 
        window.attributes('-topmost', False)
        window.lift()
        JSONsave("Ontop", '0')

    if (topcheckval.get() == 1):
        window.attributes('-topmost', True)
        JSONsave("Ontop", '1')
# %%
#notification
import subprocess

CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def notify(title, text):
  subprocess.call(['osascript', '-e', CMD, title, text])

# %%
#clicker class
class Clicker():
    #init/contrusctor
    def __init__(self, delay, amount):
        self.delay = delay
        self.amount = amount
        self.running = False
        self.clickingalready = False

    #start clicking
    def _startclicking(self):
        #stop new binds from coming
        stopbindentry.config(state= "disabled")
        startbindentry.config(state= "disabled")

        #if not already clicking
        if self.clickingalready == False:
            
            self.clickingalready = True

            #notify
            if notifval.get() == 1:
                subtitle = f"Press 'Command + {str(stoptxt.get()).upper()}' to stop clicking"
                notify("Clicking", subtitle)

            #infinite clicks
            if self.amount == 'inf' or self.amount == 0:
                    
                    #click infinitlely
                    while self.running == True:
                        pos = list(pyautogui.position())
                        pyautogui.click(x=pos[0], y=pos[1])
                        #delay
                        time.sleep(self.delay)
                    
                    #break when stopped
                    if self.running == False:
                        self.stopclicking()

            else:

                #click for int value
                for x in range(self.amount):

                    #if stop not clicked run
                    if self.running == True:
                        pos = list(pyautogui.position())
                        pyautogui.click(x=pos[0], y=pos[1])
                        #delay
                        time.sleep(self.delay)
                    
                    #break when stopped
                    if self.running == False:
                        self.stopclicking()
                        break

            #once click range over end clicking
            self.stopclicking()

        else:
            pass
    
    #threading start clicking
    def startclicking(self):
        #start thread
        if self.amount == 'inf' or self.amount >= 0:
            self.running = True
            self.clickthread = threading.Thread(target=self._startclicking)
            self.clickthread.start()
        else:
            pass

    #stop clicking
    def stopclicking(self):
        if self.running == True:
            #let new binds happen
            stopbindentry.config(state= "normal")
            startbindentry.config(state= "normal")

            #notify
            if notifval.get() == 1:
                subtitle = f"Press 'Command + {str(starttxt.get()).upper()}' to start clicking"
                notify("Stopped Clicking", subtitle)

            #stop click
            self.running = False
            self.clickthread.join()
            self.clickingalready = False
            pass
        else:
            pass


# %%
ClickClass = 0

#%%
#JSON remapping
JSON_FILE = open('settings.json','r').read()
JSON_DATA = json.loads(JSON_FILE)

def JSONsave(variable, value):
    JSON_DATA["MainSettings"][variable] = str(value)
    JSON_DUMP = json.dumps(JSON_DATA) 
    JSON_FILE = open('settings.json','w')
    JSON_FILE.write(JSON_DUMP)

# %%
#entry limit

#https://stackoverflow.com/questions/5446553/tkinter-entry-character-limit
def amt_limit(entry_text):
    if len(entry_text.get()) > 4:
        #remove last entry
        crs = amtentry.index(INSERT)
        lastentrm = entry_text.get()[:crs -1] + entry_text.get()[crs:]
        amtentry.icursor(amtentry.index(INSERT) - 1)
        
        #set entry to new value
        entry_text.set(lastentrm)

def time_limit(entry_text):
    if len(entry_text.get()) > 5:
        #remove last entry
        crs = delayentry.index(INSERT)
        lastentrm = entry_text.get()[:crs -1] + entry_text.get()[crs:]
        delayentry.icursor(delayentry.index(INSERT) - 1)
        
        #set entry to new value
        entry_text.set(lastentrm)

# %%
#inputs

def clickamt(entry):
    centryplc = entry.get()
    if len(entry.get()) == 5:
        centryplc = entry.get()[:-1]

    #0 fixes
    try:
        if entry.get()[0] == '0' and len(str(entry.get())) > 1:
            entry.set(entry.get()[1:])
            amtentry.icursor(amtentry.index(INSERT) - 1)
    except:
        pass

    #check if value is inf
    try:
        int(centryplc)
        #reassign the values in the class
        ClickClass.__init__(float(delaytxt.get()) ,int(amttxt.get()))
        JSONsave("DefaultClicks", int(amttxt.get()))

    except ValueError:
        if entry.get() == 'i' or entry.get() == 'in' or entry.get() =='inf':
            ClickClass.__init__(float(delaytxt.get()) ,int(0))
            JSONsave("DefaultClicks", '0')
        else:
            entry.set(entry.get()[:-1])

def delayamt(entry):
    dentryplc = entry.get()
    #limit of length
    if len(entry.get()) == 6:
        dentryplc = entry.get()[:-1]

    #0 fixes   
    try:
        if entry.get()[0] == '0' and entry.get()[1] == '0':
            entry.set(entry.get()[1:])
            delayentry.icursor(delayentry.index(INSERT) - 1)
    except:
        pass

    if dentryplc == '.':

        #try reassinging
        try:
            ClickClass.__init__(float(0) ,int(amttxt.get()))
            JSONsave("DefaultDelay", (0.0))
        except:
        #catch the click value of "inf" maybe breaking the thing
            ClickClass.__init__(float(0) ,int(0))
            JSONsave("DefaultDelay", (0.0))

    try:
        float(dentryplc)
        ClickClass.__init__(float(delaytxt.get()) ,int(amttxt.get()))
        JSONsave("DefaultDelay", (delaytxt.get()))
    except ValueError:
        pass

# %%
#main
window = tk.Tk()
window.option_add('*tearOff', FALSE)

#break between clicks or super lag
pyautogui.PAUSE = 0.025

#entries for delay and amount of clicks
delaytxt = StringVar()

delaylabel = tk.Label(window, text='Delay:', highlightthickness=0, borderwidth=0)
delaylabel2 = tk.Label(window, text=' secs', highlightthickness=0, borderwidth=0)
delayentry = tk.Entry(window, textvariable=delaytxt, width=5)

amttxt = StringVar()

amtlabel = tk.Label(window, text='Clicks:', highlightthickness=0, borderwidth=0)
amtlabel2 = tk.Label(window, text='(inf for infinite)', highlightthickness=0, borderwidth=0)
amtentry = tk.Spinbox(window, from_=0, to=9999, width=5, textvariable=amttxt, wrap=True,)
amtentry.delete(0,END)

#character limits
amttxt.trace("w", lambda *args: amt_limit(amttxt))
delaytxt.trace("w", lambda *args: time_limit(delaytxt))

#trace to make entry to the varibales below
amttxt.trace("w", lambda *args: clickamt(amttxt))
delaytxt.trace("w", lambda *args: delayamt(delaytxt))

#default values for clicker
delay = 0.0 # in seconds btw ^^
clicks = 0

delayentry.insert(0, delay)
amtentry.insert(0, clicks)

#buttons prereq
stop_threads = False

#Clicker
ClickClass = Clicker(float(delayentry.get()), int(amtentry.get()))

#buttons
startbtn = tkm.Button(window, text='Start', command=ClickClass.startclicking)
stopbtn = tkm.Button(window, text='Stop', command=ClickClass.stopclicking)

hfix=-0.15

#place buttons
startbtn.place(relx=0.25, rely=0.75-hfix, anchor=CENTER)
stopbtn.place(relx=0.75, rely=0.75-hfix, anchor=CENTER)

x = 0.15
#label interaactive parts placing
delaylabel.place(relx=0.15, rely=0.25 - x, anchor=CENTER)
delayentry.place(relx=0.4, rely=0.25- x, anchor=CENTER)
delaylabel2.place(relx=0.625, rely=0.25 - x, anchor=CENTER)

amtlabel.place(relx=0.15, rely=0.4 - x, anchor=CENTER)
amtentry.place(relx=0.437, rely=0.395 - x, anchor=CENTER)

#seperator lines
separatorfrm = tk.LabelFrame(window, text='OpenClicker', bg='#D3D3D3', font=(30))

#separator = tk.Frame(window, bg="#D3D3D3", height=1, bd=0)
separatorfrm.place(relx=0, rely=0.5 - x, relwidth=1,)

#geometry
w=200
h=220

#save position of last app for next imt eapp opened
posx = int(JSON_DATA['MainSettings']['appx'])
posy = int(JSON_DATA['MainSettings']['appy'])

def dragging(event):
    JSONsave('appx', str(window.winfo_rootx()))
    JSONsave('appy', str(window.winfo_rooty()))

window.bind('<Configure>', dragging)

ww = posx
wh = posy

def defined():
    defined.clicc = 6

defined()

#keybinds
def startinvoke():
    if defined.clicc == 6:
        defined.clicc = 12

    else:
        ClickClass.startclicking()
        defined.clicc = 12

def stopinvoke():
    ClickClass.stopclicking()
    clicc = 8

def destroyerdd():
    window.destroy()

def bindglobally():
    if globalbindval.get() == 1:
        JSONsave("GlobalBind", '1')
        try:
            keyboard.add_hotkey(f'Command+{starttxt.get()}', lambda: startinvoke())
            keyboard.add_hotkey(f'Command+{stoptxt.get()}', lambda: stopinvoke())
        except NameError:
            keyboard.add_hotkey(f'Command+.', lambda: startinvoke())
            keyboard.add_hotkey(f'Command+/', lambda: stopinvoke())

    if globalbindval.get() == 0:
        JSONsave("GlobalBind", '0')
        try:
            keyboard.remove_hotkey(f'Command+{starttxt.get()}')
            keyboard.remove_hotkey(f'Command+{stoptxt.get()}')
        except:
            pass

#menubar
menubar = tk.Menu(window)
appmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="App", menu=appmenu)

topcheckval = tk.IntVar()

appmenu.add_checkbutton(label='Stay on top', variable=topcheckval, onvalue=1, offvalue=0, command=ontop)

#global bind selection
globalbindval = tk.IntVar()

appmenu.add_checkbutton(label='Set keybinds globally', variable=globalbindval, onvalue=1, offvalue=0, command=bindglobally)

if JSON_DATA['MainSettings']['GlobalBind'] == '1':
    globalbindval.set(int(JSON_DATA['MainSettings']['GlobalBind']))

#notificaions selection
notifval = tk.IntVar()

#save notifucaitipons to json
def notifsave():
    if notifval.get() == 1:
        JSONsave("Notifications", '1')
    if notifval.get() == 0:
        JSONsave("Notifications", '0')

appmenu.add_checkbutton(label='Notificaions', variable=notifval, onvalue=1, offvalue=0, command=notifsave)

#other stuff
appmenu.add_separator()

appmenu.add_command(label="Close" ,underline=0, command=destroyerdd, accelerator="Command-w")
window.bind(f"<{appmenu.entrycget('Close', 'accelerator')}>", lambda e: destroyerdd())

#start and stop commands
controlsMenu = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label="Controls", underline=0, menu=controlsMenu)

#startclick
controlsMenu.add_command(label="Start", underline=0, accelerator="Command-.", command=startinvoke)
window.bind(f"<{controlsMenu.entrycget('Start', 'accelerator')}>", lambda e: startinvoke())

#stopclick
controlsMenu.add_command(label="Stop", underline=60, accelerator="Command-/", command=stopinvoke)
window.bind(f"<{controlsMenu.entrycget('Stop', 'accelerator')}>", lambda e: stopinvoke())

window.config(menu=menubar)

#custom binds

#starting code bind
def startbind():
    #more then one character
    cursorpos = startbindentry.index(INSERT)

    starttxt.set(starttxt.get().lower())

    if len(starttxt.get()) < 1:
        startbindentry.configure(highlightbackground="red")
    
    if len(starttxt.get()) >= 1:
        startbindentry.config(highlightbackground='#FFFFFF')

        if cursorpos == 1:   
            starttxt.set(starttxt.get()[:1])

        if cursorpos == 2:
                starttxt.set(starttxt.get()[1:])

        controlsMenu.entryconfigure('Start', accelerator=f'Command-{starttxt.get()}')
        window.bind(f"<{controlsMenu.entrycget('Start', 'accelerator')}>", lambda e: startinvoke())
        
        #save to json
        JSONsave("StartBind", (starttxt.get()))

        #global bind
        bindglobally()

starttxt = StringVar()

startlbl = tk.Label(window, text='⌘ +', highlightthickness=0, borderwidth=0)
startbindentry = tk.Entry(window, textvariable=starttxt, width=1, justify='center', borderwidth=0, highlightthickness=2, highlightcolor='#78C5EF')
startbindentry.config(insertontime=0)

starttxt.set('.')

startlbl.place(relx=0.2, rely=0.65-hfix, anchor=CENTER)
startbindentry.place(relx=0.3025, rely=0.645-hfix, anchor=CENTER)
starttxt.trace("w", lambda *args: startbind())

#starting code bind
def stopbind():
    #more then one character
    cursorpos = stopbindentry.index(INSERT)

    stoptxt.set(stoptxt.get().lower())

    if len(stoptxt.get()) < 1:
        stopbindentry.configure(highlightbackground="red")
    
    if len(stoptxt.get()) >= 1:
        stopbindentry.config(highlightbackground='#FFFFFF')

        if cursorpos == 1:     
            stoptxt.set(stoptxt.get()[:1])

        if cursorpos == 2:
                stoptxt.set(stoptxt.get()[1:])

        controlsMenu.entryconfigure('Stop', accelerator=f'Command-{stoptxt.get()}')
        window.bind(f"<{controlsMenu.entrycget('Stop', 'accelerator')}>", lambda e: stopinvoke())

        #save to json
        JSONsave("StopBind", (stoptxt.get()))

        #global bind
        bindglobally()

stoptxt = StringVar()

stoplbl = tk.Label(window, text='⌘ +', highlightthickness=0, borderwidth=0)
stopbindentry = tk.Entry(window, textvariable=stoptxt, width=1, justify='center', borderwidth=0, highlightthickness=2, highlightcolor='#78C5EF')
stopbindentry.config(insertontime=0)

stoptxt.set('/')

v = 0.025
stoplbl.place(relx=1-0.3025+v, rely=0.65 - hfix, anchor=CENTER)
stopbindentry.place(relx=1-0.2+v, rely=0.645 - hfix, anchor=CENTER)
stoptxt.trace("w", lambda *args: stopbind())

#json save file
JSON_FILE = open('settings.json','r').read()
JSON_DATA = json.loads(JSON_FILE)

#set info from json
starttxt.set(JSON_DATA['MainSettings']['StartBind'])
stoptxt.set(JSON_DATA['MainSettings']['StopBind'])
amttxt.set(int(JSON_DATA['MainSettings']['DefaultClicks']))
delaytxt.set(float(JSON_DATA['MainSettings']['DefaultDelay']))
delaytxt.set(float(JSON_DATA['MainSettings']['DefaultDelay']))
topcheckval.set(int(JSON_DATA['MainSettings']['Ontop']))
globalbindval.set(int(JSON_DATA['MainSettings']['GlobalBind']))
notifval.set(int(JSON_DATA['MainSettings']['Notifications']))

ontop()
bindglobally()

# %%
#window info
window.title('OpenClicker')
window.geometry('%dx%d+%d+%d' % (w, h, ww, wh))
window.resizable(False, False)
window.mainloop()