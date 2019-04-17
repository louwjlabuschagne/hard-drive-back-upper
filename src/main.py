import os
import argparse
from shutil import copyfile
from time import gmtime, strftime

def log_print(message):
    """
    A print function with the timestamp
    """
    print('[%s]: %s'%(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message))

def files_in_dir(root_dir):
    """
    A function to get the full file paths for all files in root_dir
    """
    file_set = set()

    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            file_set.add(rel_file)
    return file_set

if __name__ == '__main__':
    description = """
    This program copies all new files in a source directory (src_dir) to a destination directory (dst_dir).

    Rules for conflicts:

    1. If the same file exists in both the source and destination don't copy.
       Here the same means the same full file path.
       In other words, if you copy accross the file manually to the destination
       and it exists on the source, then it won't be coppied again, EVEN IF IT IS A DIFFERENT
       FILE WITH THE SAME NAME.
    2. If the file exists on the source but not the destination copy it across
    3. If the file exists on the destination but not the source, leave it on the destination

    The current implementation will ignore empty folders.
    """

    parser = argparse.ArgumentParser(prog='Hard Drive Back Upper',description=description)
    parser.add_argument('-s', '--src_dir', type=str,
                        help='The source directory to copy from')
    parser.add_argument('-d', '--dst_dir', type=str,
                        help='The destination directory to copy to')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print out logs')
    args = parser.parse_args()

    src_drive = args.src_dir
    dst_drive = args.dst_dir
    v = args.verbose

    #if we have both a source and a destination drive, then continue
    if (bool(src_drive)) & (bool(dst_drive)):
        if v: log_print('App Start')
        src_files = files_in_dir(src_drive)
        #macOS creates DS_Store files for each folder, this just removes them from our source files to copy
        src_files = set([file for file in src_files if 'DS_Store' not in file])
        if v: log_print('There are %d files in the source directory'%len(src_files))

        dst_files = files_in_dir(dst_drive)
        #macOS creates DS_Store files for each folder, this just removes them from our destination files to copy
        dst_files = set([file for file in dst_files if 'DS_Store' not in file])
        if v: log_print('There are %d files in the destination directory'%len(dst_files))

        files_that_are_on_the_src_and_not_on_the_dst = [file for file in src_files if file not in dst_files]
        if v: log_print('Found %d new files to copy'%len(files_that_are_on_the_src_and_not_on_the_dst))

        #if there are new files to copy
        if len(files_that_are_on_the_src_and_not_on_the_dst) != 0:
            if v: log_print('New files to be copied %s'%str(files_that_are_on_the_src_and_not_on_the_dst))
            if v: log_print('Copying started')
            for file in files_that_are_on_the_src_and_not_on_the_dst:
                #get the full file path of the source and destination files
                dst_file = dst_drive+file
                src_file = src_drive+file

                #but if the folders don't exists, we first need to create them
                #this gets the destination folder for file
                dst_folder = dst_file.rsplit('/', maxsplit=1)[0]

                #check if the destination folder exists, if not create it
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                    if v: log_print('Created folder %s'%('dst:/'+dst_folder.replace(dst_drive, '')))

                #the actual copying happens here
                copyfile(src_file, dst_file)
                if v: log_print('Coppied %s --> %s'%('src:/'+file, 'dst:/'+file))
            if v: log_print('Copying Complete')
        if v: log_print('App End')
    else:
        print('Please specify src_dir and dst_dir. See -h for help.')
