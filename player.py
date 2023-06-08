import os
import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer                    #button funtionality

def addMusic():             #function to open a file
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            if song.endswith(".mp3"):
                    playList.insert(END, song)

def Resize_Image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio))
    image = image.resize(newsize, Image.ANTIALIAS)
    return image                    


def playMusic():            #function to play the music
    musicName = playList.get(ACTIVE)
    print(musicName[0:-4])
    mixer.music.load(playList.get(ACTIVE))
    mixer.music.play(loops=0)

    playTime()

def playTime()

def stop():
    mixer.music.stop()
    playList.selection_clear(ACTIVE)
     
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True     

def slide(x):
    musicName = playList.get(ACTIVE)
    print(musicName[0:-4])
    mixer.music.load(playList.get(ACTIVE))
    mixer.music.play(loops= 0, start=int(my_slider.get))


root = Tk()             #Window
root.geometry("485x700+290+10")      #xaxis x yaxis + xshift + yshift  
root.title("TEMPO TAP") 
root.configure(background ="#20004D")
root.resizable(False,False)
mixer.init()

l_frame = Frame(root, bg= "#FFFFFF", width= 485, height= 180)
l_frame.place(x = 0 , y = 400)

img_Icon = PhotoImage(file="LOGO.png")
root.iconphoto(False, img_Icon)


Menu = PhotoImage(file = "menu.png")
Label(root, image = Menu).place(x=0 , y = 580 , width = 485 , height= 100)

frame_Music = Frame(root, bd = 2 , relief = RIDGE)      #relief is a 3D effect style to a button
frame_Music.place(x = 0 , y = 585, width = 485, height = 100)




playButton = PhotoImage(file = "play.png")
Button(root, image = playButton, height = 50, width= 50, command = playMusic, borderwidth=0, bg="#ffffff").place(x = 200, y = 487)

pauseButton = PhotoImage(file = "pause.png")
Button(root, image = pauseButton, height = 50, width= 50, command = lambda: pause(paused),borderwidth=0,bg="#ffffff").place(x = 340, y = 487)

stopButton = PhotoImage(file = "stop.png")
Button(root, image = stopButton, height = 50, width= 50, command = stop,borderwidth=0,bg="#ffffff").place(x = 100, y = 487)

Button(root, text = "Browse Music" , width = 59 , height = 1, font = ("calibri" , 12 , "bold"), fg = "Black" , bg = "#ffffff", command = addMusic).place(x = 0 , y = 550) #Browse Music

Scroll = Scrollbar(frame_Music)

playList = Listbox(frame_Music, width = 100 , font = ("Times new roman", 10,), bg = "#333333", fg = "grey", selectbackground= "lightblue", cursor = "hand2", bd = 0, yscrollcommand= Scroll.set)

Scroll.config(command= playList.yview)
Scroll.pack(side = RIGHT, fill = Y)
playList.pack(side = RIGHT, fill = BOTH)

root.mainloop()
