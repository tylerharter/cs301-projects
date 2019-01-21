# Lab 1: Running Programs

Welcome to your first lab!  If you're using a lab computer, you're
required to work in pairs (otherwise, we won't have enough machines).
If you've already installed [Python on your
computer](https://tyler.caraza-harter.com/cs301/spring19/videos.html),
you may still learn more by choosing to work with somebody.  This
document is meant to be self guiding, and you may leave when you're
finished.  Be sure to ask a neighbour or flag down a TA if you have
any questions, though (don't be shy!).

This semester, you're going to learn how to write your own Python
code.  But for this lab, you're just going to practice running some
Python programs we give you.

# Download Your First Program

The first thing you're going to need to decide is where to keep your
project work this semester.  If you don't have a preference, we
recommend creating a folder named "cs301" under "Documents".  How to
find the Documents folder may vary from computer to computer.  On a
Windows machine, you might find it like this in File Explorer:

<img src="windows-documents.png" width="400">

On a Mac, you might find it in Finder here:

<img src="mac-documents.png" width="200">

Inside the new "cs301" folder you created under "Documents", we
recommend you create a sub-folder called "lab1" and use it for all
your files related to this lab.

Next, you will need to download a file named "hello.py" to your "lab1"
folder.  At the top of this page, you'll see a list of files,
something like this:

<img src="github.png" width="800">

Downloading files from GitHub (the site hosting this document) is a
little tricky for those new to it.  Follow these steps carefull:

1. left-click on "hello.py"
2. right-click on the "Raw" button
3. Choose "Save Link As..." (or similar)
4. Save the file in your "lab" folder

We recommend you use the Chrome browser (other browsers will work too,
but sometimes we've seen Safari automatically renaming files when
downloaded, which is usually problematic).  In Chrome, right-clicking
the "Raw" button looks like this:

<img src="raw.png" width="300">

## Run Your First Program

Now it gets a little tricky.  You need to figure out the path of your
"lab1" folder.  You can think of a "path" is just a more complete name
for a file or folder.

1. open your "Documents" in either File Explorer or Finder
2. copy the pathname of "lab1" using either these [Windows directions](https://www.pcworld.com/article/251406/windows_tips_copy_a_file_path_show_or_hide_extensions.html) or [Mac directions](http://osxdaily.com/2015/11/05/copy-file-path-name-text-mac-os-x-finder/)
3. paste the pathname of "lab1" in your notes somewhere

Now, you'll need to open something called a "terminal emulator".

**Windows**:
1. hit the Windows logo key on your keyboard
2. click "Windows PowerShell" (be careful, DO NOT choose the ones that say "ISE" or "x86")

**Mac**:
1. open Finder
2. click "Applications"
3. open "Utilities"
4. double-click Terminal.app

Ok, now the directions are the same for Mac and Windows again.  Type
this in the terminal (replace P1-PATH with the pathname of "p1", as
you determined above; keep the quotes around the pathname, though) and
hit enter:

```
cd "P1-PATH"
```

Type `ls` and hit enter.  If you've done everything correctly so far,
you should see the "hello.py" file that you downloaded in step 1
listed.

Now, type `python hello.py` and hit ENTER (if you're not using a lab
computer, you may need to instead type `python3 hello.py`, depending
on your setup).  If everything is working correctly, you should see
the following message printed:

```
Hello, World!
```

Congrats!  The above is the trickiest part of the lab.  If there other
students near you who are struggling to get this far, please take a
minute and show them what you did (this helps if the TAs are swamped
with questions).