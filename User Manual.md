# BrenderQue User Manual #
Version 0.5

Written on 2/6/2020.

BrenderQue is a tool that allows you to que Blender Renders for render on a machine.  It is useful in multi-scene projects where you have multiple blender files to render and don't want to constantly check to see if your rendering computer is ready to render the next scene in your project.  It makes more sense to use this tool if you have multiple computers involved in the project (ex. a work station and a render horse), but using BrenderQue on single machine projects would still make your job easier.

***

## Basic Usage ##

### First Time Setup ###

Unzip the BrenderQue folder.  Do not move or modify any files within the folder.  You can move the folder where you like.  On first launch, OR anytime Blender is updated, open the options tab inside the BrenderQue interface and set the Blender file path to the path of the folder which houses blender.exe.  Do not include "blender.exe" in the path.  The path should resemble something like "C:\Program Files\Blender Foundation\Blender 2.81".  


### Launching BrenderQue ###

If you are using the executable release package (Most users):
Simply run the "BrenderQue.exe" file.

If you are using the Python distribution:
Launch BrenderQue from the command line using "python3 BrenderQue/main.py".

*Note that you must supply the full path to main.py.  For example, if BrenderQue is in your downloads folder, and your username was karl, the command would be "python3 C:/Users/karl/Downloads/BrenderQue/main.py"

***

### Your First Que ###
After BrenderQue launches, you can then use it right away.  To add a render job, simply input the full file path to the file you want to render, specify if it is an animation or not, and click add job.  Blender will open up in command line mode and begin rendering.

***

### Visit the Wiki! ###
For updated and more in-depth documentation, visit the BrenderQue wiki here: https://github.com/Fantaland/BrenderQue/wiki
