#!/usr/bin/python3
# 2120271831cpf Minimum File Select GUI for Grapefruit Straw by EFFX
# 2120272312cpf PyFileDialog3.py
# 2021-02-28-EFF

# Grapefruit Straw is a simple uploader for incrementally uploading projects
# too large to do in one push.
# Written by Eric Fedrowisch Feb 24, 2021.
# tkinter GUI added with code from Carl Fedrowisch Feb. 28, 2021
# All rights reserved.


import sys
import os
import os.path
import pathlib
import glob
import tkinter as tk
import tkinter.filedialog
import tkinter.scrolledtext as scrolledtext


max_file_size = 52428800  # or 50 MB
max_push_size = 104857600  # or 100 MB


def getdir():
    global filenames
    global source_dir
    # Open a file dialog window
    dir = tkinter.filedialog.askdirectory()
    source_dir = dir
    if source_dir != '':  # Catch if user cancels dialog
        filenames = list(glob.iglob(dir + '**/**', recursive=True))
        # n=0
        for filename in filenames:
            filesize = os.path.getsize(filename)
            if filesize > max_file_size:
                filelist.insert(tkinter.END, filename+"\n", foreground="red")
            else:
                filelist.insert(tk.END, filename + "\n")
    else:
        filenames = []
    update_selection_stats()


def clear():
    filelist.delete("1.0", "end")
    feedback_lbl.config(text="Currently Selected: \
                        0 Folders, 0 Files,  0 MB Total")


def cropfiles():
    seltext = filelist.selection_get()
    filelist.delete("1.0", "end")
    filelist.insert(tk.END, seltext)
    update_selection_stats(seltext.split())


def update_selection_stats(filelist=None):
    global filenames
    list = filelist or filenames
    # Define Feedback Label Vars
    n_dirs = 0
    n_files = 0
    files_size = 0
    for path in list:
        if os.path.exists(path):
            if os.path.isdir(path):
                n_dirs += 1
            else:
                try:
                    files_size += os.path.getsize(path)
                    n_files += 1
                except FileNotFoundError:
                    pass
    new_text = "Currently Selected: " + \
               str(n_dirs) + " Folders, " + \
               str(n_files) + " Files, " + \
               str(round(files_size/1e+6, 2)) + " MB Total"
    feedback_lbl.config(text=new_text)


def get_url():
    return str(url_text.get('1.0', tk.END))


def upload():
    global source_dir
    if source_dir is not None and source_dir != '':
        pth = os.path.split(sys.argv[0])[0] + os.path.sep
        gfs = '"' + pth + 'gfs.py' + '"'
        cmd = 'python3 ' + gfs + " " + str(source_dir) + " " + get_url()
        os.system(cmd)
        # Remove Temp repo
        os.system('rm -rf ' + str(source_dir) + '_2')


if __name__ == '__main__':
    # Create a window with title.
    global filenames
    global source_dir
    filenames = []
    source_dir = ''
    window = tk.Tk()
    window.title("Grapefruit Straw")
    window.geometry('800x400')

    # Create Widgets
    bgd = "black"
    fgd = "white"

    # Create buttons.
    btn1 = tk.Button(window, text="Select Dir", bg=bgd, fg=fgd, command=getdir)
    btn2 = tk.Button(window, text="Clear All", bg=bgd, fg=fgd, command=clear)
    btn3 = tk.Button(window, text="Crop", bg=bgd, fg=fgd, command=cropfiles)
    btn4 = tk.Button(window, text="Upload", bg=bgd, fg=fgd, command=upload)
    # Create text box for url to push to remote git server
    url_lbl = tk.Label(window, text="HTTPS URL:", fg=fgd)
    url_text = tk.Text(window, height=1)
    # Create a scrolling textbox for selected file names.
    filelist = scrolledtext.ScrolledText(window, height=300, width=100)
    feedback_lbl = tk.Label(window, text="Currently Selected: \
                            0 Folders, 0 Files,  0 MB Total", fg=fgd)

    # Pack Widgets
    pad = tk.N + tk.S + tk.E + tk.W
    btn1.grid(row=0, column=0, sticky=pad)
    btn2.grid(row=0, column=1, sticky=pad)
    btn3.grid(row=0, column=2, sticky=pad)
    btn4.grid(row=2, column=0, sticky=pad)
    url_lbl.grid(row=1, column=0)
    url_text.grid(row=1, column=1, columnspan=2, sticky=pad)
    feedback_lbl.grid(row=3, column=0, columnspan=3, sticky=pad)
    filelist.grid(row=4, column=0, columnspan=3, sticky=pad)

    window.mainloop()
