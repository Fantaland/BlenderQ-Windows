#BrenderQue Win-0.1a
#Written by Ethan Montgomery on 1/23/2020

from tkinter import * # for interface.
#import smtplib # for email alerts.
import subprocess # to run the batch process kicking off the actual rendering.
import threading # enough said.
import pathlib #to get the path of the python file.

programpath = str(pathlib.WindowsPath(__file__).parent.absolute())
blenderfilepath = 'C:/Program Files/Blender Foundation/Blender 2.81/'
renderjobs = []
settingsfile = 'settings'
currentjob = subprocess.Popen('cd', shell=True)
currentjob.wait()

# Load in the variables from settings.
def Load():
    global blenderfilepath
    # # look inside settings file for settings.
    sf = open(programpath + '\\' + settingsfile, 'r')
    for line in sf:
        if 'BPL' in line:
            bfp = line.split('-', maxsplit=1)
            # blenderfilepath = str(pathlib.Path(bfp[1]))
            blenderfilepath = str(bfp[1])
            print('Path loaded for Blender: ' + blenderfilepath)
    #
    #         if pathlib.Path(blenderfilepath).is_dir():
    #             print('Blender File Path is real.')
    #         else:
    #             print('Path is invalid!')
        else:
            print('Using default config...')
            return

    sf.close()
    print('Settings loaded')


# this is the button handler function for create job.  it also calls JobManager, getting rid of the delay between adding the first job and rendering.
def AddJob():
    CreateJob(newFilePath.get(), isanim.get()) #Call create job.
    newFilePath.delete(0, END) #clear the entry box.
    JobManager() #call JobManager.

# CreateJob actually assembles the job and puts it in the que.
# p is the path, a is if it is an animation or not.
def CreateJob(p, a):
    s = 'blender -b "' + p + '"'
    if a == True:
        s += ' -a'
    else:
        s += ' -f 1'

    renderjobs.append(s) #put the job in the que.
    inQue.insert(len(renderjobs), p) #show the path in the que list.

    print('Job created for file: ' + s)

# Run next job executes the command to run the next job.
def RunNextJob():
    print('Running next job...')
    print(blenderfilepath)
    currentjob = subprocess.call('START ' + renderjobs[0], cwd=str(blenderfilepath), shell=True, stdout=subprocess.PIPE)
    inQue.delete(0)
    finished.insert(0, renderjobs[0])

# Job manager determines if it is time for the next scene to be rendered.
def JobManager():
    currentjob.wait()
    if len(renderjobs) > 0:
        if currentjob.returncode == None:
            return
        elif currentjob.returncode == 0:
            RunNextJob()
            renderjobs.pop(0)
    else:
        return

# Kicks off important JobManager function and Load function.
def Init():
    # subprocess.call('cd C:/Program Files/Blender Foundation/Blender 2.81/', shell=True)
    threading.Timer(5, JobManager).start()
    Load()
    print('Init finished.')

# Opens and draws the options menu
def OpenOpt():
    blenderfilepathlabeltxt = StringVar()

    optionsmenu = Toplevel(wind)
    optionsmenu.geometry('400x400')
    optionsmenu.title('BrenderQue Options')
    # optionsmenu.call('wm', 'iconphoto', optionsmenu._w, PhotoImage(file=programpath + '\\resources\\brenderQueLogo.png'))
    optionsmenu.resizable(False, False)

    blenderfilepathbox = Entry(optionsmenu)
    blenderfilepathbox.place(height=25, width=220, x=90, y=70)
    # blenderfilepathbox.set(blenderfilepath)

    blenderfilepathlabel = Label(optionsmenu, textvariable=blenderfilepathlabeltxt)
    blenderfilepathlabeltxt.set('Blender File Path')
    blenderfilepathlabel.place(x=90, y=45)

    optbtn = Button(optionsmenu, text='Save Options', command=SaveOpt)
    optbtn.place(height=25, width=80, x=160, y=350)

    optionsmenu.mainloop()

    print('Options opened.')

# Saves options.
def SaveOpt():
    sf = open(programpath + '\\' + settingsfile, 'w')
    sf.write('BPL-' + blenderfilepathbox.get())
    sf.close()
    # optionsmenu.destroy()
    print('Options saved.')

Init()

###########INTERFACE############
#Interface creation
wind = Tk()
wind.geometry('800x600')
wind.title('BrenderQue')
wind.call('wm', 'iconphoto', wind._w, PhotoImage(file=programpath + '\\resources\\brenderQueLogo.png'))
wind.resizable(False, False)
wind['bg'] = '#2c2930'

#Interface variables.
versiontxt = StringVar()
inQuetxt = StringVar()
finishedtxt = StringVar()
isanim = BooleanVar()

versionL = Label(wind, textvariable=versiontxt)
versiontxt.set('Version 0.5')
versionL.pack(side='bottom', pady=5)
versionL['bg'] = '#2c2930'
versionL['fg'] = '#f2f2f2'

newFilePath = Entry()
newFilePath.place(height=25, width=220, x=250, y=120)

addbtn = Button(text="Add Job", command=AddJob)
addbtn.place(height=25, width=80, x=470, y=120)

optbtn = Button(text="Options", command=OpenOpt)
optbtn.place(height=25, width=80, x=715, y=5)

isanimbtn = Checkbutton(text="Is Animation", var=isanim)
isanimbtn.place(height=25, width=100, x=140, y=120)
isanimbtn['bg'] = '#2c2930'
isanimbtn['fg'] = '#f2f2f2'

inQueL = Label(wind, textvariable=inQuetxt)
inQuetxt.set('Files in Que')
inQueL.place(width=100, x=90, y=190)
inQueL['bg'] = '#2c2930'
inQueL['fg'] = '#f2f2f2'

inQue = Listbox()
inQue.place(height=300, width=200, x=100, y=210)

finishedL = Label(wind, textvariable=finishedtxt)
finishedtxt.set('Finished')
finishedL.place(width=100, x=485, y=190)
finishedL['bg'] = '#2c2930'
finishedL['fg'] = '#f2f2f2'

finished = Listbox()
finished.place(height=300, width=200, x=500, y=210)

wind.mainloop()
