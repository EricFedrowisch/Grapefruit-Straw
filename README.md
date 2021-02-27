# Grapefruit-Straw
Grapefruit Straw is a simple uploader for incrementally uploading projects too large to do in one push. Github for example has a limit of 100 MB for a single
commit and 50 MB for a single file.
## How to Use
Takes two command line arguments, a file path to the repository to upload and
a url to a git repository. Like so:
```python3
python3 gfs.py /path/to/repository https://github.com/User/Some.git
```

## Problems
Probably many. Here are a few.
* This was written in python3 on OS X. It might work other places.
* It makes no attempt to handle authentication. I used GitHub Desktop so this
doesn't cause a problem for me.
* It uses the force flag on the updates, which means it WILL overwrite whatever
is on the remote repository. You were warned.
