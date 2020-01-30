# BrenderQue User Manual #
Version 0.1a

Written by Ethan Montgomery on 1/25/2020.

BrenderQue is a tool that allows you to que Blender Renders for render on a machine.  It is useful in multi-scene projects where you have multiple blender files to render and don't want to constantly check to see if your rendering computer is ready to render the next scene in your project.  It makes more sense to use this tool if you have multiple computers involved in the project (ex. a work station and a render horse), but using BrenderQue on single machine projects would still make your job easier.



## Basic Usage ##

### Launching BrenderQue ###
Launch BrenderQue from the command line using "python3 BrenderQue/main.py".

*Note that you must supply the full path to main.py.  For example, if BrenderQue is in your downloads folder, and your username was karl, the command would be "python3 C:/Users/karl/Downloads/BrenderQue/main.py"


### Your First Que ###
After BrenderQue launches, you can then use it right away.  To add a render job, simply input the full file path to the file you want to render, specify if it is an animation or not, and click add job.  Blender will open up in command line mode and begin rendering.


*Note that BrenderQue currently only works if Blender is installed at "C:\Program Files\Blender Foundation\Blender 2.81".  This will be fixed in the next update.
