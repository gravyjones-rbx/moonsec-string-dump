# warning
this script edits a moonsec lua file to make it dump itself and then runs it (the moonsec file). meaning if the moonsec devloper added malicious code to thwart debugging this script would execute that code, at the time of this writing, I dont believe theyve done this, but its a future possiblity. 

# use
this program is not user friendly, will require editing to make work

requires the moonsec file to be formatted (prettified), I used a vscode extension called LuaHelper for this

line 80 change file path to your moonsec file, should work after :3

## how it work
we edit the lua file to add an anti anti tamper, so we can edit the file without it erroring due to being tampered

then we add some code to dump the longest string in stack right before we crash 
* I found these crash sections by manually running two moon sec files and seeing where they crashed, one file compiled for lua and one for roblox executors

