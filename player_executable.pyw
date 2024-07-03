import os
import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer

# App setup
root = Tk()
root.title("MP3 Player")
root.geometry("485x700+290+10")
root.configure(background = "#333333")
root.resizable(False, False)




# Application frame & icon configuration
lower_frame = Frame(root, bg= "#FFFFFF", width= 485, height= 180)
lower_frame.place(x= 0, y= 400)

image_icon = PhotoImage(file= "xpcat.png")
root.iconphoto(False, image_icon)




# Animated background setup
frame_count = 30
frames = []
for i in range(frame_count):
    try:
        frame = PhotoImage(file="bgplaying.gif", format=f'gif -index {i}')
        frames.append(frame)
    except Exception as e:
        print(f"Error loading frame {i}: {e}")
        break  # Exit the loop if an error occurs, likely due to no more frames

def update(ind):
       frame = frames[ind]
       ind += 1
       if ind >= len(frames):  # Use len(frames) to ensure it works even if frames are less than expected
              ind = 0
       animated_bg.configure(image=frame)
       root.after(40, update, ind)

animated_bg = Label(root)
animated_bg.place(x=0, y=0)
root.after(0, update, 0)




# Button configurations & setup
class MusicPlayer:
       def __init__(self, playlist):
              self.playlist = playlist
              self.status = 'stopped'  # Possible values: 'playing', 'paused', 'stopped'
              self.volume_slider = None # Volume slider
              mixer.init()

       def add_music(self):
              path = filedialog.askdirectory()
              if path:
                     os.chdir(path)
                     songs = os.listdir(path)
              for song in songs:
                     if song.endswith("mp3"):
                            playlist.insert(END, song)
       
       def play_music(self):
              if self.status == 'paused':
                     mixer.music.unpause()
                     self.status = 'playing'
                     print("Music resumed.")
              elif self.status in ['stopped', 'playing']:  # Handle 'playing' status by stopping and playing the new song
                     if self.status == 'playing':
                            mixer.music.stop()  # Stop the currently playing music
                     music_name = self.playlist.get(ACTIVE)
                     print(music_name[0:-4])
                     mixer.music.load(self.playlist.get(ACTIVE))
                     mixer.music.play()
                     self.status = 'playing'
              else:
                     print("Music is already playing.")

       def stop_music(self):
              if self.status in ['playing', 'paused']:
                     music_name = self.playlist.get(ACTIVE)
                     print(f'{music_name[0:-4]} STOPPED')
                     mixer.music.stop()
                     self.status = 'stopped'
              else:
                     print("No music is playing at the moment.")

       def pause_music(self):
              if self.status == 'playing':
                     music_name = self.playlist.get(ACTIVE)
                     print(f'{music_name[0:-4]} PAUSED')
                     mixer.music.pause()
                     self.status = 'paused'
              else:
                     print("No music to pause.")

       def volume_music(self):
              if self.status == 'playing':
                     self.toggle_volume_slider()
              else:
                     print("No music to set volume to.")
       
       def toggle_volume_slider(self):
              if self.volume_slider is None:
                     self.volume_slider = Scale(root, from_= 0, to= 100, orient= HORIZONTAL, command= self.update_volume)
                     self.volume_slider.set(mixer.music.get_volume() * 100)
                     self.volume_slider.place(x= 20, y= 450)
              else:
                     self.volume_slider.place_forget() # Hides the slider
                     self.volume_slider = None       
       
       def update_volume(self, value):
              volume_level = int(value) / 100
              mixer.music.set_volume(volume_level)
              
       def music_timer(self):
              pass
              
        
        


Menu = PhotoImage(file= "menu.png")
Label(root, image= Menu).place(x= 0, y= 580, width= 485, height= 110)

frame_music = Frame(root, bd= 2, relief= RIDGE)
frame_music.place(x= 0, y= 585, width= 485, height= 110)




# Scroll & Playlist configuration
scroll = Scrollbar(frame_music)
playlist = Listbox(frame_music, width= 100, font= ("Times New Roman", 10), bg= "#333333", fg= "grey", selectbackground= "lightblue", cursor= "hand2", bd= 0, yscrollcommand= scroll.set)
scroll.config(command= playlist.yview)
scroll.pack(side= RIGHT, fill= Y)
playlist.pack(side= RIGHT, fill= BOTH)
player = MusicPlayer(playlist)




# Buttons configuration
Button(root, text= "Browse Music", width= 60, height= 1, font= ("calibri", 12, "bold"), fg= "#333333", command= player.add_music).place(x= 0, y= 550)

button_play = PhotoImage(file= "play1.png")
Button(root, image= button_play, bg= "#FFFFFF", bd= 0, height= 60, width= 60, command= player.play_music).place(x= 215, y= 487)

button_stop = PhotoImage(file= "stop1.png")
Button(root, image= button_stop, bg= "#FFFFFF", bd= 0, height= 60, width= 60, command= player.stop_music).place(x= 130, y= 487)

button_pause = PhotoImage(file= "pause1.png")
Button(root, image= button_pause, bg= "#FFFFFF", bd= 0, height= 60, width= 60, command= player.pause_music).place(x= 300, y= 487)

button_volume = PhotoImage(file= "volume.png")
Button(root, image= button_volume, bg= "#FFFFFF", bd= 0, height= 60, width= 60, command= player.volume_music).place(x= 20, y= 487)




# Starting the program
root.mainloop()