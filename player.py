import os
import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer                  
from mutagen.mp3 import MP3  
import tkinter.ttk as ttk


#funtions for Buttons
def addMusic():             #function to open a file
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                    playList.insert(END, song)

def playMusic():            #function to play the music
    musicName = playList.get(ACTIVE)
    playList.selection_set(ACTIVE)
    status.config(text = ' ')
    slider.config(value=0)
    print(musicName[0:-4])
    mixer.music.load(playList.get(ACTIVE))
    mixer.music.play(loops=0)
    getTime()


global stopped
stopped = False

def stop():                 #function to stop the music
    status.config(text = ' ')
    slider.config(value=0)

    mixer.music.stop()
    status.config(text='')

    global stopped
    stopped = True
     
#Global Variable Declaration     
global paused
paused = False

def pause(is_paused):       #function to pause/play the music
    global paused
    paused = is_paused

    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True     

def nextSong():
    status.config(text = ' ')
    slider.config(value=0)
    next = playList.curselection()
    next = next[0]+1
    song = playList.get(next)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    playList.selection_clear(0,END)
    playList.activate(next)

    playList.selection_set(next, last=None)
    getTime()

def prevSong():
    status.config(text = ' ')
    slider.config(value=0)
    prev = playList.curselection()
    prev = prev[0]-1
    song = playList.get(prev)
    mixer.music.load(song)
    mixer.music.play(loops=0)

    playList.selection_clear(0,END)
    playList.activate(prev)

    playList.selection_set(prev, last=None)
    getTime()

def getTime():
    currTime = mixer.music.get_pos() /1000
    convertedTime = time.strftime('%H : %M : %S', time.gmtime(currTime)) 
   
    currSong = playList.curselection()
    song = playList.get(currSong)
    #Mutagen SongLength
    songMutagen = MP3(song)
    global songLen
    songLen = songMutagen.info.length
    convertedsongLen = time.strftime('%H : %M : %S', time.gmtime(songLen)) 

    currTime +=1

    if int(slider.get()) == int(songLen):
        status.config(text = f'Time Elapsed: {convertedsongLen} of {convertedsongLen} ')
        nextSong()

    elif paused:
        pass

    elif int(slider.get()) == int(currTime):
        sliderPos = int(songLen)
        slider.config(to = sliderPos, value = int(currTime))
    
    else:
        sliderPos = int(songLen)
        slider.config(to = sliderPos, value = int(slider.get()))
        convertedTime = time.strftime('%H : %M : %S', time.gmtime(int(slider.get()))) 
        status.config(text = f'Time Elapsed: {convertedTime} of {convertedsongLen} ')
        nextTime = int(slider.get()) + 1
        slider.config(value= nextTime)
    
    status.after(1000, getTime)


def slide(x):
    song = playList.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0, start= int(slider.get()))

#Tkinter Window
root = Tk()             #Window
root.geometry("485x700+290+10")      #xaxis x yaxis + xshift + yshift  
root.title("TEMPO TAP") 
root.configure(background ="#20004D")
root.resizable(False,False)
mixer.init()

#mainFrame
l_frame = Frame(root, bg= "#FFFFFF", width= 485, height= 180)
l_frame.place(x = 0 , y = 400)

frameCnt = 30
frames = [PhotoImage(file='giphy (1).gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(40, update, ind)
label = Label(root)
label.place(x=0, y=0)
root.after(0, update, 0)

#TitleIcon
img_Icon = PhotoImage(file="LOGO.png")
root.iconphoto(False, img_Icon)

#MenuArea
Menu = PhotoImage(file = "menu.png")
Label(root, image = Menu).place(x=0 , y = 580 , width = 485 , height= 100)

#MusicFrame
frame_Music = Frame(root, bd = 2 , relief = RIDGE)      #relief is a 3D effect style to a button
frame_Music.place(x = 0 , y = 585, width = 485, height = 100)

#Buttons
playButton = PhotoImage(file = "play.png")
pauseButton = PhotoImage(file = "pause.png")
stopButton = PhotoImage(file = "stop.png")
nextButton = PhotoImage(file = "next.png")
prevButton = PhotoImage(file = "prev.png")

#ButtonPlacement
Button(root, image = playButton, height = 50, width= 50, command = playMusic, borderwidth=0, bg="#ffffff").place(x = 210, y = 487)
Button(root, image = pauseButton, height = 50, width= 50, command = lambda: pause(paused),borderwidth=0,bg="#ffffff").place(x = 270, y = 487)
Button(root, image = stopButton, height = 50, width= 50, command = stop,borderwidth=0,bg="#ffffff").place(x = 145, y = 487)
Button(root, image = nextButton, height = 50, width= 50, command = nextSong,borderwidth=0,bg="#ffffff").place(x = 330, y = 487)
Button(root, image = prevButton, height = 50, width= 50, command = prevSong,borderwidth=0,bg="#ffffff").place(x = 80, y = 487)
Button(root, text = "Browse Music" , width = 59 , height = 1, font = ("calibri" , 12 , "bold"), fg = "Black" , bg = "#ffffff", command = addMusic).place(x = 0 , y = 550) #Browse Music

#ScrollBar for Music Progress
Scroll = Scrollbar(frame_Music)

#slider
slider = ttk.Scale(root, from_ =0 , to = 100 , orient= HORIZONTAL , value= 0, command= slide, length= 450)
slider.place(x = 15, y = 457)

#statusbar
status = Label(root ,text=' ',bd= 1, relief= GROOVE, anchor= E)
status.pack(fill = X , side = BOTTOM, ipady = 2)



#Playlist
playList = Listbox(frame_Music, width = 100 , font = ("Times new roman", 10,), bg = "#333333", fg = "grey", selectbackground= "lightblue", cursor = "hand2", bd = 0, yscrollcommand= Scroll.set)
Scroll.config(command= playList.yview)
Scroll.pack(side = RIGHT, fill = Y)
playList.pack(side = RIGHT, fill = BOTH)
root.mainloop()

