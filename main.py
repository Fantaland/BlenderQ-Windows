# BrenderQue Win-1.0.0
# 0.5.1 Completed by Ethan Montgomery on 2/4/2020

from tkinter import * # for interface.
from tkinter import filedialog # for the file browser.
from tkinter import font # for fonts.
from tkinter.ttk import Progressbar # more interface.
import subprocess # to run the batch process kicking off the actual rendering.
import threading # enough said!
import pathlib # to get the path of the python file and for blender file path handling.
import ctypes # check UAC priveledge.
# import re # for cleaning up some strings.  This is mostly interface based, but might have security uses in the future.
import sys

# basic functionality.
programpath = str(pathlib.WindowsPath(__file__).parent.absolute()) # path of Blender Q
blenderfilepath = 'C:/Program Files/Blender Foundation/Blender 2.81/'
renderjobs = []
settingsfile = 'settings'
blenderoutputfile = 'current-output.txt'
executefile = 'ex.bat'
isfirstrender = True

currentjob = subprocess.Popen('cd', shell=True)
currentjob.wait()

# security related.
notallowedcharacters=[';','?','*','<','>','|','"','&','*','$']


# Load in the variables from settings.
def Load():
    global blenderfilepath # the blender filepath
    global keyloaded # loaded security key
    global f # for fernet
    # look inside settings file for settings.
    sf = open(programpath + '\\' + settingsfile, 'r')
    for line in sf:
        if 'BPL' in line:
            bfp = line.split('=', maxsplit=1)
            blenderfilepath = str(bfp[1].rstrip())
            print('NOTE: Current path loaded for Blender: ' + blenderfilepath)

            if pathlib.Path(blenderfilepath).is_dir():
                print('GOOD: Blender file path is real.')
            else:
                print('BAD: Blender file path is invalid!')
        else:
            print('NOTE: Settings not found, using default config...')
            return

    sf.close()
    print('GOOD: Settings loaded')

# Checks if user is admin and returns true or false.  If this function fails, it returns false.
def IsAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Utility to get the filename out of the inputted path reguardless of / or \ notation.  Also removes .blend when returned.  Intended for interface use only.
def ExtractFilename(full):
    if full.find('\\') != -1:
        fullsplit = full.split('\\')
    elif full.find("/"):
        fullsplit = full.split('/')

    end = fullsplit[len(fullsplit) - 1]
    name = end.split('.')
    return name[0]

# this is the button handler function for create job.  it also calls JobManager, getting rid of the delay between adding the first job and rendering.
def AddJob():
    CreateJob(newFilePath.get(), isanim.get()) # Call create job.
    JobManager() # call JobManager.

# CreateJob actually assembles the job and puts it in the que.
# p is the path, a is if it is an animation or not.
def CreateJob(p, a):
    safecheck = 0 # The saftey index
    safecharacters = False

    if p.find(':') == 1:
        safecheck += 1
    if p.find('\\') == 2 or p.find('/') == 2:
        safecheck += 1
    if p.endswith('.blend'):
        safecheck += 1

    if any(x in notallowedcharacters for x in p):
        print("BAD: Invalid character(s) inputted.")
        safecharacters = False
    else:
        print("GOOD: Characters are clean.")
        safecharacters = True

    if safecheck == 3 and safecharacters == True:
        s = 'call "' + str(blenderfilepath) + 'blender" -b "' + p + '"'
        if a == True:
            s += ' -a'
        else:
            s += ' -f 1 '

        s += ('1> ' + programpath + '\\' + blenderoutputfile + ' &')

        renderjobs.append(s) # put the job in the que.
        inQue.insert(len(renderjobs), ExtractFilename(p)) # show the path in the que list.  Use extract filename to clean it up.

        newFilePath.delete(0, END) # clear the entry box.

        print('GOOD: Job created for file: ' + p)
    else:
        print('BAD: Security issue detected.  Check inputted filepath and try again!')

# Run next job executes the command to run the next job.
def RunNextJob():
    global currentjob

    print('GOOD: Running next job...')

    ef = open(programpath + '\\' + executefile, 'w')
    ef.write(renderjobs[0])
    ef.close()
    currentjob = subprocess.Popen(programpath + '\\' + executefile, cwd=str(blenderfilepath))

    UpdateInterface() # Update the interface.


# Job manager determines if it is time for the next scene to be rendered.
def JobManager():
    global isfirstrender

    t = threading.Timer(5, JobManager).start()
    isrendering = False
    op = open(programpath + '\\' + blenderoutputfile)
    linesop = op.readlines()
    op.close()
    lastline = linesop[-1].rstrip()

    if lastline == 'Blender quit':
        print('NOTE: Ready to render next file...')
        # UpdateInterface() #This updates it so that when the last render is done it shows it as done.
        isrendering = False
    else:
        isrendering = True

    if len(renderjobs) > 0:
        if isrendering and isfirstrender == False:
            print('NOTE: Still rendering current job...')
        else:
            RunNextJob()
            renderjobs.pop(0)
            isfirstrender = False

# Updating the interface for when a file is completed rendering, added to the que, or finished rendering.  This function is unaware of actual progress, so calling placement is important.
def UpdateInterface():
    nf = inQue.get(0,0)
    inQue.delete(0)
    # This for loop cleans up the string when it gets outputted to the finished list.
    cft = currentfiletxt.get()
    for char in '\(\)\,\'':
        cft = cft.replace(char, '')

    finished.insert(0, cft)
    currentfiletxt.set(nf)

# def OpenAdminWarning():
#     global adminwarning
#     closetxt = StringVar()
#
#     adminwarning = Toplevel(wind)
#     adminwarning.geometry('400x400')
#     adminwarning.title('Admin Warning!')
#     adminwarning.resizable(False, False)
#     adminwarning['bg'] = '#f2f2f2'
#
#     closelabel = Label(adminwarning, textvariable=closetxt)
#     closetxt.set('Warning!  You are running Blender Q as an admin.  This does not inheriently pose a security risk, but consider running this application as a non-admin for stronger security.')
#     closelabel.place(x=80, y=35)
#
#     continbtn = Button(adminwarning, text='Continue', command=CloseAdminWarning)
#     continbtn.place(height=35, width=100, x=150, y=325)
#     continbtn['borderwidth'] = 0
#     continbtn['bg'] = '#88789e'
#     continbtn['fg'] = '#2c2930'
#
#     adminwarning.mainloop()
#
#     print('NOTE: Admin warning opened.')
#
# #Close admin warning
# def CloseAdminWarning():
#     adminwarning.destroy()

# Kicks off important JobManager function and Load function.
def Init():
    Load()
    global t
    t = threading.Timer(5, JobManager).start()

    print('GOOD: Init running.')

    if IsAdmin() == True:
        print('WARNING: You are running Blender Q as an admin.  This does not inheriently pose a security risk, but consider running this application as a non-admin for stronger security.')
        # OpenAdminWarning() #Open the admin warning box.
    else:
        print('GOOD: Process not run as administrator.')

# Opens and draws the options menu
def OpenOpt():
    global blenderfilepathbox
    global optionsmenu
    blenderfilepathlabeltxt = StringVar()
    credittxt = StringVar()

    optionsmenu = Toplevel(wind)
    optionsmenu.geometry('400x400')
    optionsmenu.title('Blender Q Options')
    optionsmenu.resizable(False, False)
    optionsmenu['bg'] = '#f2f2f2'

    blenderfilepathbox = Entry(optionsmenu)
    blenderfilepathbox.place(height=25, width=220, x=90, y=70)
    blenderfilepathbox.insert(0, blenderfilepath)

    blenderfilepathlabel = Label(optionsmenu, textvariable=blenderfilepathlabeltxt)
    blenderfilepathlabeltxt.set('Blender File Path')
    blenderfilepathlabel.place(x=80, y=35)

    saveoptbtn = Button(optionsmenu, text='Save Options', command=SaveOpt)
    saveoptbtn.place(height=35, width=100, x=150, y=325)
    saveoptbtn['borderwidth'] = 0
    saveoptbtn['bg'] = '#88789e'
    saveoptbtn['fg'] = '#2c2930'

    creditL = Label(optionsmenu, textvariable=credittxt)
    credittxt.set('by Ethan Montgomery, 2020')
    creditL.pack(side='bottom', pady=5)
    creditL['bg'] = '#f2f2f2'
    creditL['fg'] = '#2c2930'
    creditL['font'] = smallfont

    optionsmenu.mainloop()

    print('NOTE: Options opened.')

# Saves options.
def SaveOpt():
    blenderfilepath = str(blenderfilepathbox.get())
    sf = open(programpath + '\\' + settingsfile, 'w')
    sf.write('BPL=' + blenderfilepathbox.get())
    sf.close()
    optionsmenu.destroy()
    print('NOTE: Options saved.')

previousdir = '' #previousdir needs to remain outside of the OpenFileDialog function so the filepath can persist.
# OpenFileDialog opens a file browser and sets the new file path entry to the path of whatever file is selected.
def OpenFileDialog():
    print('file dialog opened.')
    global previousdir

    n = filedialog.askopenfilename(initialdir = previousdir,title = "Select file",filetypes = (("Blend files","*.blend"),("All files","*.*")))
    newFilePath.delete(0, END)
    newFilePath.insert(0, n)
    previousdir = str(pathlib.Path(newFilePath).parent.absolute()) # This causes an error but seems to work fine.

def OnClose():
    print('NOTE: Shutting Down Program... Goodbye!')
    # t.cancel()
    wind.destroy()
    sys.exit()

Init()

###########INTERFACE############
#Interface creation
wind = Tk()
wind.geometry('800x600')
wind.title('Blender Q')
wind.call('wm', 'iconphoto', wind._w, PhotoImage(file=programpath + '\\resources\\brenderQueLogo.png'))
wind.resizable(False, False)
wind['bg'] = '#88789e'

smallfont = font.Font(size=9)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12) # set font with family=

#Interface variables.
versiontxt = StringVar()
inQuetxt = StringVar()
finishedtxt = StringVar()
isanim = BooleanVar()
currentprogressbartxt = StringVar()
currentfiletxt = StringVar()

versionL = Label(wind, textvariable=versiontxt)
versiontxt.set('Version 1.0')
versionL.pack(side='bottom', pady=5)
versionL['bg'] = '#88789e'
versionL['fg'] = '#2c2930'
versionL['font'] = smallfont

newFilePath = Entry()
newFilePath.place(height=25, width=220, x=250, y=120)
newFilePath['bg'] = '#f2f2f2'
newFilePath['fg'] = '#2c2930'
newFilePath['borderwidth'] = 0

browsebtn = Button(text="Browse", command=OpenFileDialog)
browsebtn.place(height=25, width=80, x=470, y=120)
browsebtn['borderwidth'] = 0
browsebtn['bg'] = '#2c2930'
browsebtn['fg'] = '#f2f2f2'

addbtn = Button(text="Add Job", command=AddJob)
addbtn.place(height=35, width=100, x=350, y=170)
addbtn['borderwidth'] = 0
addbtn['bg'] = '#2c2930'
addbtn['fg'] = '#f2f2f2'

optbtn = Button(text="Options", command=OpenOpt)
optbtn.place(height=30, width=80, x=715, y=5)
optbtn['borderwidth'] = 0
optbtn['bg'] = '#2c2930'
optbtn['fg'] = '#f2f2f2'

isanimbtn = Checkbutton(text="Is Animation", var=isanim)
isanimbtn.place(height=25, width=120, x=110, y=120)
isanimbtn['bg'] = '#88789e'
isanimbtn['fg'] = '#f2f2f2'
isanimbtn['selectcolor'] = '#2c2930'
isanimbtn['bd'] = 0
isanimbtn['activebackground'] = '#88789e'
isanimbtn['activeforeground'] = '#f2f2f2'

inQueL = Label(wind, textvariable=inQuetxt)
inQuetxt.set('Files in Que')
inQueL.place(width=100, x=90, y=210)
inQueL['bg'] = '#88789e'
inQueL['fg'] = '#f2f2f2'

inQue = Listbox()
inQue.place(height=300, width=200, x=100, y=240)
inQue['borderwidth'] = 0
inQue['highlightthickness'] = 0
inQue['bg'] = '#f2f2f2'

# currentprogressbar = Progressbar(wind, orient = HORIZONTAL, length = 150, mode = 'determinate', value=35)
# currentprogressbar.place(x=325, y=280)

currentprogressbarL = Label(wind, textvariable=currentprogressbartxt)
currentprogressbartxt.set('Currently Rendering:')
currentprogressbarL.place(width=150, x=325, y=245)
currentprogressbarL['bg'] = '#88789e'
currentprogressbarL['fg'] = '#f2f2f2'

currentfileL = Label(wind, textvariable=currentfiletxt)
currentfiletxt.set('')
currentfileL.place(width=150, x=325, y=275)
currentfileL['bg'] = '#88789e'
currentfileL['fg'] = '#f2f2f2'


finishedL = Label(wind, textvariable=finishedtxt)
finishedtxt.set('Finished')
finishedL.place(width=100, x=475, y=210)
finishedL['bg'] = '#88789e'
finishedL['fg'] = '#f2f2f2'

finished = Listbox()
finished.place(height=300, width=200, x=500, y=240)
finished['borderwidth'] = 0
finished['highlightthickness'] = 0
finished['bg'] = '#f2f2f2'

wind.protocol("WM_DELETE_WINDOW", OnClose)
wind.mainloop()
