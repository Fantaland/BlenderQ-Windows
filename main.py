# BrenderQue Win-0.5
# Written by Ethan Montgomery on 1/23/2020 (0.1a)
# 0.5 Completed by Ethan Montgomery on 2/4/2020

from tkinter import * # for interface.
from tkinter import filedialog # for the file browser.
from tkinter import font # for fonts.
#import smtplib # for email alerts.
import subprocess # to run the batch process kicking off the actual rendering.
import threading # enough said.
import pathlib # to get the path of the python file and for blender file path handling.
import psutil # for checking process id

programpath = str(pathlib.WindowsPath(__file__).parent.absolute()) # path of BrenderQue
blenderfilepath = 'C:/Program Files/Blender Foundation/Blender 2.81/'
renderjobs = []
settingsfile = 'settings'
blenderoutputfile = 'current-output.txt'
executefile = 'ex.bat'

currentjob = subprocess.Popen('cd', shell=True)
currentjob.wait()
curpid = 99999

isfirstrender = True

# Load in the variables from settings.
def Load():
    global blenderfilepath
    # # look inside settings file for settings.
    sf = open(programpath + '\\' + settingsfile, 'r')
    for line in sf:
        if 'BPL' in line:
            bfp = line.split('=', maxsplit=1)
            # blenderfilepath = str(pathlib.Path(bfp[1]))
            blenderfilepath = str(bfp[1].rstrip())
            print('Path loaded for Blender: ' + blenderfilepath)

            if pathlib.Path(blenderfilepath).is_dir():
                print('Blender File Path is real.')
            else:
                print('Path is invalid!')
        else:
            print('Using default config...')
            return

    sf.close()
    print('Settings loaded')


# this is the button handler function for create job.  it also calls JobManager, getting rid of the delay between adding the first job and rendering.
def AddJob():
    CreateJob(newFilePath.get(), isanim.get()) # Call create job.
    newFilePath.delete(0, END) # clear the entry box.
    JobManager() # call JobManager.

# CreateJob actually assembles the job and puts it in the que.
# p is the path, a is if it is an animation or not.
def CreateJob(p, a):
    s = 'call "' + str(blenderfilepath) + 'blender" -b "' + p + '"'
    if a == True:
        s += ' -a'
    else:
        s += ' -f 1'

    s += ('1> ' + programpath + '\\' + blenderoutputfile + ' &')

    renderjobs.append(s) # put the job in the que.
    inQue.insert(len(renderjobs), p) # show the path in the que list.

    print('Job created for file: ' + s)

# Run next job executes the command to run the next job.
def RunNextJob():
    global currentjob

    print('Running next job...')

    ef = open(programpath + '\\' + executefile, 'w')
    # ef.write('cd ' + str(blenderfilepath))
    ef.write(renderjobs[0])
    ef.close()
    # currentjob = subprocess.Popen(renderjobs[0], cwd=str(blenderfilepath), shell=True, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE) # Old method with security threat and doesn't work for "queing"
    currentjob = subprocess.Popen(programpath + '\\' + executefile, cwd=str(blenderfilepath))
    global curpid
    curpid = currentjob.pid
    print('PID: ' + str(curpid))
    nf = inQue.get(0,0)
    inQue.delete(0)
    finished.insert(0, nf)


# Job manager determines if it is time for the next scene to be rendered.
def JobManager():
    global isfirstrender

    threading.Timer(5, JobManager).start()
    isrendering = False
    op = open(programpath + '\\' + blenderoutputfile)
    linesop = op.readlines()
    op.close()
    lastline = linesop[-1].rstrip()

    if lastline == 'Blender quit':
        print('Ready to render next file.')
        isrendering = False
    else:
        isrendering = True

    if len(renderjobs) > 0:
        if isrendering and isfirstrender == False:
            print('Still Rendering')
        else:
            RunNextJob()
            renderjobs.pop(0)
            isfirstrender = False

    # print('isrendering =' + str(isrendering))
    # print(lastline)
    # print(linesop[-1])


# Kicks off important JobManager function and Load function.
def Init():
    # subprocess.call('cd C:/Program Files/Blender Foundation/Blender 2.81/', shell=True)
    Load()
    threading.Timer(5, JobManager).start()
    print('Init finished.')

# Opens and draws the options menu
def OpenOpt():
    global blenderfilepathbox
    global optionsmenu
    blenderfilepathlabeltxt = StringVar()
    credittxt = StringVar()

    optionsmenu = Toplevel(wind)
    optionsmenu.geometry('400x400')
    optionsmenu.title('BrenderQue Options')
    # optionsmenu.call('wm', 'iconphoto', optionsmenu._w, PhotoImage(file=programpath + '\\resources\\brenderQueLogo.png'))
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

    print('Options opened.')

# Saves options.
def SaveOpt():
    blenderfilepath = str(blenderfilepathbox.get())
    sf = open(programpath + '\\' + settingsfile, 'w')
    sf.write('BPL=' + blenderfilepathbox.get())
    sf.close()
    optionsmenu.destroy()
    print('Options saved.')

previousdir = '' #previousdir needs to remain outside of the OpenFileDialog function so the filepath can persist.
# OpenFileDialog opens a file browser and sets the new file path entry to the path of whatever file is selected.
def OpenFileDialog():
    print('file dialog opened.')
    global previousdir

    n = filedialog.askopenfilename(initialdir = previousdir,title = "Select file",filetypes = (("Blend files","*.blend"),("All files","*.*")))
    newFilePath.delete(0, END)
    newFilePath.insert(0, n)
    previousdir = str(pathlib.Path(newFilePath).parent.absolute()) # This causes an error but seems to work fine.

Init()

###########INTERFACE############
#Interface creation
wind = Tk()
wind.geometry('800x600')
wind.title('BrenderQue')
wind.call('wm', 'iconphoto', wind._w, PhotoImage(file=programpath + '\\resources\\brenderQueLogo.png'))
wind.resizable(False, False)
# wind['bg'] = '#2c2930'
wind['bg'] = '#88789e'

smallfont = font.Font(size=9)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12) # set font with family=

#Interface variables.
versiontxt = StringVar()
inQuetxt = StringVar()
finishedtxt = StringVar()
isanim = BooleanVar()

versionL = Label(wind, textvariable=versiontxt)
versiontxt.set('Version 0.5')
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
# browsebtn['font'] = mainfont

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

wind.mainloop()
