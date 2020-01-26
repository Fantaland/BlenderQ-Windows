#BrenderQue Win-0.1a
#Written by Ethan Montgomery on 1/23/2020

from tkinter import * #for interface.
#import smtplib #for email alerts.
import subprocess #to run the batch process kicking off the actual rendering.
import threading #enough said.

renderjobs = []
currentjob = subprocess.Popen('cd', shell=True)
currentjob.wait()

#This is the button handler function for create job.
def AddJob():
    CreateJob(newFilePath.get(), isanim.get())
    print('Job added: ' + newFilePath.get())

#Creat job actually assembles the job and puts it in the que.
#p is the path, a is if it is an animation or not.
def CreateJob(p, a):
    s = 'blender -b "' + p + '"'
    if a == True:
        s += ' -a'
    else:
        s += ' -f 1'

    renderjobs.append(s) #put the job in the que.
    inQue.insert(len(renderjobs), p) #show the path in the que list.

    print('Job created for file: ' + s)

#Run next job executes the command to run the next job.
def RunNextJob():
    print('Running next job...')
    currentjob = subprocess.Popen('START ' + renderjobs[0], cwd='C:/Program Files/Blender Foundation/Blender 2.81/', shell=True, stdout=subprocess.PIPE)
    inQue.delete(0)
    finished.insert(0, renderjobs[0])

# Job manager determines if it is time for the next scene to be rendered.
def JobManager():
    threading.Timer(10, JobManager).start()
    currentjob.wait()
    if len(renderjobs) > 0:
        if currentjob.returncode == None:
            return
        elif currentjob.returncode == 0:
            RunNextJob()
            renderjobs.pop(0)
    else:
        return

def Init():
    # subprocess.call('cd C:/Program Files/Blender Foundation/Blender 2.81/', shell=True)
    print('Init finished.')

Init()
JobManager()

###########INTERFACE############
wind = Tk()
#Interface goes here.
#Interface variables.
versiontxt = StringVar()
inQuetxt = StringVar()
finishedtxt = StringVar()
isanim = BooleanVar()

#Interface creation
wind.geometry('800x600')
wind.title('Brender Que')

versionL = Label(wind, textvariable=versiontxt)
versiontxt.set('Version 0.1a')
versionL.pack(side='bottom', pady=5)

newFilePath = Entry()
newFilePath.place(height=25, width=220, x=250, y=120)

addbtn = Button(text="Add Job", command=AddJob)
addbtn.place(height=25, width=80, x=470, y=120)

isanimbtn = Checkbutton(text="Is Animation", var=isanim)
isanimbtn.place(height=25, width=100, x=140, y=120)

inQueL = Label(wind, textvariable=inQuetxt)
inQuetxt.set('Files in Que')
inQueL.place(width=100, x=90, y=190)

inQue = Listbox()
inQue.place(height=300, width=200, x=100, y=210)

finishedL = Label(wind, textvariable=finishedtxt)
finishedtxt.set('Finished')
finishedL.place(width=100, x=385, y=190)

finished = Listbox()
finished.place(height=300, width=200, x=400, y=210)

wind.mainloop()
