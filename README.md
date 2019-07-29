README

STATUS
Work in Progress

2019 July 29 
First commit and upload.
Finished media grabber and largely finished first go at gui structure.
Media grabber finds all media, names the gui panel the media should belong to so a button instance can be automatically created later, and path names to be accessed.
Tkinter will automatically scan all media folders and create a new music and sound frame + canvas for each category and layer them behind one another.

To do next:
Buttons to change panels based on what sub-directories of media is in folders.
Media handler class
Gui play, stop, vol button groups



INTRODUCTION

An environment builder for a Dungeons and Dragons Master to control music, layers of sounds, effects and lights.

My 2nd project on Python, and my first major project since I started learning how to do some programming from Khan Academy since Jan 2019.

Designed to be run from a PC/Laptop



AUTHOR

Keith Lee



PHYSICAL REQUIREMENTS

Yeelight smart bulbs
Speakers



IMPORT REQUIREMENTS

os
tkinter
vlc
tkinter


FILE STRUCTURE

Media not uploaded as they are copyrighted

4 top level folders:
CoreMusic
CoreSounds
CoreEffects
CoreSaved

CoreMusic, CoreSounds should have sub-directories for categories.  2 for CoreMusic and 1+ for CoreSounds.
CoreEffects should have no sub-directories.

