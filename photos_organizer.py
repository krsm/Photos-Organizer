import errno
import hashlib
import os
import shutil
import time

"""
1 - Open a directory
2 - Create folders # checked and duplicates
3 - Make comparison about files ( use extension and size, hash as parameter to see if is applicable to do a comparison)
4 - If the size is the same to the comparison
5 - If there is duplicate file move to duplicate folder - rename the file with the duplicate name, otherwise move
file to checked folder
6 - In the checked folder verify date and a group per month and year

"""

# get the folder in each the file is stored
curDir = os.getcwd()

# variable - name folder to be created with duplicated files
Folder1 = "01 - Duplicated"

ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg', 'gif'] # to define what type of file will be organized

# function to return the month based on the number
def returnmonth(montharg):

    switcher = {
        1: "01_JAN",
        2: "02_FEB",
        3: "03_MAR",
        4: "04_APR",
        5: "05_MAI",
        6: "06_JUN",
        7: "07_JUL",
        8: "08_AUG",
        9: "09_SEP",
        10: "10_OCT",
        11: "11_NOV",
        12: "12_DEC",

    }
    return switcher.get(montharg, "nothinhg")


# function to get an unique entry to list of elements
def getuniqueentry(listcheck):
    checked = []
    for k in listcheck:
        if k not in checked:
            checked.append(k)
    return checked


# create folders
# dir is not keyword
def makemydir(filedir, foldername):
    ckdir = os.path.join(filedir, foldername)
    print(ckdir)
    try:
        os.makedirs(ckdir, exist_ok=True)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise



# move files to specific folder, based on the date file was created
def move_files(filesdir, listofdates):
    for item in listofdates:

        makemydir(filesdir, item)  # create folders
        itemdate = item.split()
        getyearfolder = itemdate[0]
        getmonthfolder = itemdate[1]

        for file in os.listdir(filesdir):
            a = os.stat(os.path.join(filesdir, file))
            ckfile = False  # variable to assure it is not a folder, dir, etc
            ckfile = os.path.isfile(os.path.join(filesdir, file))  # check if is a file, and do not count folders, etcs.

            if not file.endswith(".py") and ckfile == True:  # .py to remove the python files,folder and dirs.
                datefile = time.localtime(a.st_mtime)
                print(datefile)
                getmonthfile = datefile.tm_mon
                getmonthfile = returnmonth(getmonthfile)
                getmonthfile = str(getmonthfile)  # convert to string
                getyearfile = datefile.tm_year
                getyearfile = str(getyearfile)  # convert to string
                if (getyearfolder == getyearfile):
                    if (getmonthfolder == getmonthfile):
                        shutil.move(file, os.path.join(filesdir,
                                                       item))  # move files if their year and month of creation is compatible with the folder


# get info about files.
def get_infodir(filedir):
    file_list = set()
    for file in os.listdir(filedir):
        a = os.stat(os.path.join(filedir, file))
        checkfile = False
        checkfile = os.path.isfile(os.path.join(filedir, file))  # check if is a file, and do not count folders, etcs.
        if not file.endswith(".py") and checkfile == True:  # .py to remove the python files in the dir

            datefile = time.localtime(a.st_mtime)
            getmonth = datefile.tm_mon
            getmonth = returnmonth(getmonth)
            getyear = datefile.tm_year
            getmonth = str(getmonth)
            getyear = str(getyear)
            dateinfo = getyear + " " + getmonth
            file_list.add(dateinfo)

    file_list = sorted(file_list)
    # get an unique entry for each date

    return file_list


# calculate hash for each file
def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


# function to create a list with hash of duplicate files
# create folder - duplicate files
# and move the duplicated files to that folder, based on hash and counter of hashes.

def gethashfileslist(filedir):
    dup_hash = {}
    for file in os.listdir(filedir):
        # a = os.stat(os.path.join(filedir,file))#join the dir and filename
        pathfile = os.path.join(filedir, file)  # join the dir and filename
        checkfile = False
        checkfile = os.path.isfile(os.path.join(filedir, file))  # check if is a file, and do not count folders, etcs
        if not file.endswith(".py") and checkfile == True:  # .py to remove the python files in the dir
            hashcalc = hashfile(pathfile)
            counter = 1
            # create dict with hash of files and number of same hashes
            if hashcalc not in dup_hash:
                dup_hash[hashcalc] = counter
            else:
                counter = dup_hash[hashcalc]
                counter = counter + 1
                dup_hash[hashcalc] = counter

    #print(dup_hash)
    # create folder for duplicated files
    makemydir(curDir, Folder1)

    for file in os.listdir(filedir):
        # a = os.stat(os.path.join(filedir,file))#join the dir and filename
        pathfile = os.path.join(filedir, file)  # join the dir and filename
        pathfolder1 = os.path.join(filedir, Folder1)  # join the dir and filename - dir of duplicated files
        checkfile = False
        checkfile = os.path.isfile(os.path.join(filedir, file))  # check if is a file, and do not count folders, etcs
        if not file.endswith(".py") and checkfile == True:  # .py to remove the python files in the dir
            hashcalc = hashfile(pathfile)
            hashcounter = 0
            hashcounter = dup_hash[hashcalc]

            if hashcounter > 1:
                shutil.move(file, pathfolder1)
                dup_hash[hashcalc] = hashcounter - 1


# function to get path to dir that contains pictures
def get_files_dir():
    print("#-------------------------------------------------- \n"
          "Script to organize pictures \n"
          "1 - Provide a path to the directory that contains pictures to be organized \n"
          "2 - Files will be organized by folders containing the date of their creation,"
          "and duplicated files will be moved to -> "
          "01 - Duplicated - folder that will be created.\n"
          "3 - Important!Create a backup of yours file before run the script! \n"

          "#-------------------------------------------------- \n")

    print("Type: quit, to stop execution anytime!")

    while True:

        files_dir = str(input("Provide a valid file path for pictures to be organize: "))

        if os.path.isdir(files_dir):
            return files_dir
        elif files_dir == "quit":
            print("Quit!")
            break
        else:
            print("Path provided is not valid!")


def main():

    folder_dir = get_files_dir()
    gethashfileslist(curDir)
    print("--------------------Starting getting files info--------------------")
    call_file_list = get_infodir(folder_dir)  # getting info regarding files
    print("-------------------- Moving files --------------------")
    move_files(folder_dir, call_file_list)
    print(" Finished !")


if __name__ == '__main__':

    main()
