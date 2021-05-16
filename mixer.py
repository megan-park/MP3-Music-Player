from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# root (window) widget, has to go first
root = Tk()
root.title('Music Player')
root.geometry("500x400")

# initalize pygame mixer to use sounds
pygame.mixer.init()

# grab song length time info
def play_time():
	if stopped:
		# exit the function
		return

	# grab current song elasped time
	current_time = pygame.mixer.music.get_pos() / 1000

	# throw temp label to get data
	slide_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')

	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# get the current song tuple (list) number
	#current_song = song_box.curselection()
	# grab song title from playlist
	song = song_box.get(ACTIVE)
	# add directory and mp3
	song = f'C:/Users/mpark/Desktop/random projects/Music Player Project/songs/{song}.mp3'

	# load song with mutagen
	song_mut = MP3(song)
	# get some length
	global song_length
	song_length = song_mut.info.length
	# convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	# increase current time by 1 sec
	current_time += 1

	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f'Time Elasped: {convert_song_length}  of  {convert_song_length}  ')
	elif paused:
		pass
	elif int(my_slider.get()) == int(current_time):
		# slider hasn't been moved
		# update slider to position
		slider_position = int(song_length)	
		#slider_label.config(to=slider_position, value=int(current_time))
	else: 
		# slider has been moved
		# update slider to position
		slider_position = int(song_length)	
		#slider_label.config(to=slider_position, value=int(my_slider.get()))

		# convert to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))

		# output time to status bar
		status_bar.config(text=f'Time Elasped: {converted_current_time}  of  {convert_song_length}  ')

		# move this along by 1 sec
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)

	# output time to status bar
	#status_bar.config(text=f'Time Elasped: {converted_current_time}  of  {convert_song_length}  ')

	# update slider position value to current song position
	#slider_label.config(value=int(current_time))

	# update time
	status_bar.after(1000, play_time)

# add song function
def add_song():
	song = filedialog.askopenfilename(initialdir='songs/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
	song = song.replace("C:/Users/mpark/Desktop/random projects/Music Player Project/songs/", "")
	song = song.replace(".mp3", "")
	song_box.insert(END, song)

# add many songs to playlist
def add_many_songs():
	songs= filedialog.askopenfilenames(initialdir='songs/', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))

	# loop through song list and replace directory info and mp3
	for song in songs:
		song = song.replace("C:/Users/mpark/Desktop/random projects/Music Player Project/songs/", "")
		song = song.replace(".mp3", "")
		# insert into playlist
		song_box.insert(END, song)


# play selected song
def play():
	# set stopped variable to false so song can play
	global stopped
	stopped = False

	song = song_box.get(ACTIVE)
	song = f'C:/Users/mpark/Desktop/random projects/Music Player Project/songs/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# call the play_time function to get song length
	play_time()

	# update slider to position
	#slider_position = int(song_length)
	#slider_label.config(to=slider_position, value=0)

	# get current volume
	#current_volume = pygame.mixer.music.get_volume()
	#slider_label.config(text=current_volume * 100)

# stop playing current song
global stopped
stopped = False

def stop():
	# reset slider and status bar
	statu_bar.config(text='')
	my_slider.config(value=0)

	# stop song from playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

	# clear the status bar
	status_bar.config(text='')

	# set stop variable to true
	global stopped
	stopped = True

# create global pause variable
global paused
paused = False

# pause and unpause current song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused: 
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()	
		paused = True

# play the next song in playlist
def next_song():
	# reset slider and status bar
	statu_bar.config(text='')
	my_slider.config(value=0)

	# get the current song tuple (list) number
	next_one = song_box.curselection()
	# add one to the current song number
	next_one = next_one[0]+1
	# grab song title from playlist
	song = song_box.get(next_one)

	song = f'C:/Users/mpark/Desktop/random projects/Music Player Project/songs/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# clear move active bar in playlist listbox
	song_box.selection_clear(0, END)

	# activate new song bar
	song_box.activate(next_one)

	# set active bar to next song
	song_box.selection_set(next_one, last=None)

# play previous song in playlist
def previous_song():
	# reset slider and status bar
	statu_bar.config(text='')
	my_slider.config(value=0)

	# get the current song tuple (list) number
	next_one = song_box.curselection()
	# add one to the current song number
	next_one = next_one[0]-1
	# grab song title from playlist
	song = song_box.get(next_one)

	song = f'C:/Users/mpark/Desktop/random projects/Music Player Project/songs/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# clear move active bar in playlist listbox
	song_box.selection_clear(0, END)

	# activate new song bar
	song_box.activate(next_one)

	# set active bar to next song
	song_box.selection_set(next_one, last=None)

# delete a song
def delete_song():
	stop()
	# delete currently selected song
	song_box.delete(ANCHOR)
	pygame.mixer.music.stop()

# delete all songs
def delete_all_songs():
	stop()
	song_box.delete(0, END)
	pygame.mixer.music.stop()

# create slider function
def slide(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'C:/Users/mpark/Desktop/random projects/Music Player Project/songs/{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

	# get current volume
	#current_volume = pygame.mixer.music.get_volume()
	#slider_label.config(text=current_volume * 100)

# create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# create playlist box, fg is text colour
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

# define player control buttons
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

# create player control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# create volume label frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# create player control buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10) 
play_button.grid(row=0, column=2, padx=10) 
pause_button.grid(row=0, column=3, padx=10) 
stop_button.grid(row=0, column=4, padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)

# add many songs to playlist
add_song_menu.add_command(label="Add Many Songs to Playlist", command=add_many_songs)

# create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a Song from PLaylist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs from PLaylist", command=delete_all_songs)

# create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# create volumn slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# create temp slider label
#slider_label = Label(root, text='0')
#slider_label.pack(pady=10)

# create event loop 
root.mainloop()