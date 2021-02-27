#!/usr/bin/python3
# Grapefruit Straw is a simple uploader for incrementally uploading projects
# too large to do in one push.
# Written by Eric Fedrowisch Feb 24, 2021. All rights reserved.

import sys
import os
import pathlib
from shell import Shell
import glob


# Break copy target into data buckets with constraints:
# file size < 50 MB , per push limit < 100 MB
def get_data_buckets(copy_source):
    files = []
    oversized_files = []
    max_file_size = 52428800  # or 50 MB
    max_push_size = 104857600  # or 100 MB
    for filename in glob.iglob(copy_source + '**/**', recursive=True):
        try:
            size = os.path.getsize(filename)
            if size <= max_file_size:
                files.append((filename, size))
            else:
                oversized_files.append((filename, size))
        except FileNotFoundError as e:
            pass  # Ignore symlinks, shortcuts and aliases
    if oversized_files:
        print("### WARNING! Files over 50MB are too large to transfer! ###")
        print("Files over 50MB:")
        for f in oversized_files:
            print(f[0], str(f[1]/1e+6) + " MB")
    # Take file list and split into data buckets
    data_buckets = []
    bucket = []
    bucket_sum = 0
    for file in files:  # file is (filename, size)
        if bucket_sum + file[1] < max_push_size:  # If file fits...
            bucket.append(file[0])  # Put it in bucket
            bucket_sum += file[1]
        else:
            data_buckets.append(bucket)
            bucket = [file[0]]
            bucket_sum = file[1]
    data_buckets.append(bucket)

    return data_buckets


# Make New Git repo for pushing
def create_repo():
    sh = Shell()
    sh.run('mkdir ' + temp_repo)
    p = pathlib.Path(str(copy_source))
    dirs = list(glob.iglob(copy_source + '**/**', recursive=True))
    os.chdir(temp_repo)
    for x in dirs:
        if os.path.isdir(x):
            if os.path.split(x)[1] != '.git':
                mk_dir = x.replace(copy_source, temp_repo)
                sh.run('mkdir ' + mk_dir)
    # Accidently makes folder like "target_2_2". Remove that.
    sh.run('rmdir ' + temp_repo.replace(copy_source, temp_repo))
    sh = Shell()
    sh.run('echo "#" >> README.md')
    sh.run('git init')
    sh.run('git add .')
    sh.run('git commit -m "Initial commit"')
    sh.run('git remote add origin ' + target_url)
    sh.run('git push -fu origin master')


def do_incremental_push(bucket):
    global bucket_n
    sh = Shell()
    for file in bucket:
        target = file.replace(copy_source, temp_repo)
        sh.run('cp ' + file + ' ' + target)
    sh.run('git add .')
    sh.run('git commit -am ' + '"Data Bucket ' + str(bucket_n) + '"')
    bucket_n += 1
    sh.run('git push -fu origin master')


if __name__ == '__main__':
    global bucket_n
    bucket_n = 1
    copy_source = None
    target_url = None
    # No authentification is handled currently
    # user = None
    # token = None

    # Get Target Folder for Push & Sanity Checks
    try:
        if sys.argv[1]:
            if (os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1])):
                copy_source = sys.argv[1]
        if sys.argv[2]:
            target_url = sys.argv[2]
    except IndexError as e:
        if len(sys.argv) == 1:
            print("No copy source folder supplied.")
        if len(sys.argv) == 2:
            print("No remote url supplied.")

    if copy_source is not None and target_url is not None:
        temp_repo = copy_source + '_2'
        print("Copy Source: " + str(copy_source))
        print("Temp Repo: " + str(temp_repo))
        print("Copy Target: " + str(target_url))
        data_buckets = get_data_buckets(copy_source)
        repo = create_repo()
        for bucket in data_buckets:
            print("Processing " + str(bucket_n) + '/' + str(len(data_buckets)))
            do_incremental_push(bucket)
        print("DONE")
