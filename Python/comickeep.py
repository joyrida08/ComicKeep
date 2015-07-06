import os
import sys
#from shutil import copytree, copy2, copystat, rmtree, make_archive
from shutil import *
from shutil import Error
import zipfile
from subprocess import call
import fnmatch
import sqlite3 as lite

### Global Variables ###
local = "/sdcard/comics/" # Root Dir Where comics will be stored and processed
marvel = "/data/data/com.marvel.unlimited/" # Root Dir of Marvls data files
mSrc = marvel + "files/reader/pages" # Location of files stored for offline reading
mDB = marvel + "databases/" # location of DB' that store metadata for comics
dbString = "*library.sqlite" # Search string for grabbing tge correct db
tmpPath = local + "sources/" # Folder used for processing
dstPath = local + "cbz" # Folder where finished comics are stored
dbLocal = local + "library.sqlite" # Name given to local copy of the metadata DB
errors = [] # Error Logging

def copySource(mSrc, tmpPath, db=0, symlinks=False, ignore=None):
## copies directory of folders and returns the count
    names = os.listdir(mSrc) # /../pages
    if ignore is not None:
        ignored_names = ignore(mSrc, names) 
    else: 
        ignored_names = set() 

    if not os.path.isdir(tmpPath):
        os.makedirs(tmpPath)

    for name in names:
        if name in ignored_names: 
            continue
        srcname = os.path.join(mSrc, name) 
        dstname = os.path.join(tmpPath, name)
        try: 
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)    
            elif os.path.isdir(srcname): 
                copytree(srcname, dstname) 
            else: 
                copy2(srcname, dstname)

        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except Error as err:
            errors.extend(err.args[0])
    try: 
        copystat(mSrc, tmpPath) 
   # except WindowsError:
       # pass
    except OSError as why: 
        errors.extend((mSrc, tmpPath, str(why)))    
    

    if db == 1:
        dbPath = copyDB(dbString, mDB, local)
    changeAccess(a=0)
    return

def copyDB(pattern, src, dst):
# function for locating a specific file
    changeAccess(a=1)
    result = []
    errors = []
    global local
    for files in os.listdir(src):
        if fnmatch.fnmatch(files, pattern):
            result.append(files)

    if len(result) == 1:
        dbName = str(result[0])
        try:
            copy2(src + dbName, dst + "library.sqlite")
            
            
        except (IOError, os.error) as why:
            errors.append((src + dbName, dst, str(why)))
        except Error as err:
            errors.extend(err.args[0])
        return 

    else:
        return result       

def processFolders(comicPath, dbPath):
    c = dbconn(dbPath)
    for f in os.listdir(comicPath):
        path = comicPath + f
        c.execute("Select title from book Where digital_id=?", (f,))
        new_name = c.fetchone()
        new_path = comicPath + new_name[0]
        os.rename(comicPath + f, new_path)
    return 

def processPages(tmpDir):
    comics = os.listdir(tmpDir)
    for c in comics:
        src = tmpDir + c
        pages = os.listdir(src)
        cnt = len(pages)
        if cnt > 10:
            for p in pages:
                pageO = src + "/" + p
                pageN = src + "/0" + p
                cov = src + "/000.jpg"
                if p == "cov.jpg":
                    os.rename(pageO, cov)
                else:
                   os.rename(pageO, pageN)           
        else:
            rmtree(src)
    return

def finalizeConvert(tmpDir, destDir):
    folders = os.listdir(tmpDir)
    for c in folders:
        comic = tmpDir + c
        zip = archiver(comic, comic)
        cbzFile = comic + ".cbz"
        os.rename(zip, cbzFile)
        move(cbzFile, destDir)
        rmtree(comic)

def archiver(rootdir, arcName):
    return make_archive(arcName, "zip", rootdir)

def dbconn(dbpath):
# Funtion to help with connecting to sqlite DB's
    db = dbpath
    con = lite.connect(db) 
    cur = con.cursor()
    return cur

def changeAccess(a=0):
# Function used to change file permissions
    if a == 1:
        call(["su", "-c", "am", "force-stop", "com.marvel.unlimited"]) # stops marvel app process
        call(["su","-c", "chmod", "-R", "777", "/data/data/com.marvel.unlimited/databases"]) 
        call(["su","-c", "chmod", "-R", "777", "/data/data/com.marvel.unlimited/files/reader"])
        return 0
    elif a == 0:
        call(["su", "-c", "am", "force-stop", "com.marvel.unlimited"]) # Stops Marvel app process
        call(["su","-c", "chmod", "-R", "600", "/data/data/com.marvel.unlimited/databases/*.sqlite"])
        call(["su","-c", "chmod", "-R", "660", "/data/data/com.marvel.unlimited/databases/*.sqlite-journal"])
        call(["su","-c", "chmod", "-R", "660", "/data/data/com.marvel.unlimited/databases/*.db-journal"])
        call(["su","-c", "chmod", "-R", "660", "/data/data/com.marvel.unlimited/databases/*.db"])
        call(["su","-c", "chmod", "-R", "751", "/data/data/com.marvel.unlimited/databases"])
        call(["su","-c", "chmod", "700", "/data/data/com.marvel.unlimited/files/reader/pages/*"])
        call(["su","-c", "chmod", "600", "/data/data/com.marvel.unlimited/files/reader/pages/*/*"])
        call(["su","-c", "chmod", "700", "/data/data/com.marvel.unlimited/files/reader/pages"])
        call(["su","-c", "chmod", "700", "/data/data/com.marvel.unlimited/files/reader"])
        return 0
    else:
        return 1


def main():
### Example Process ###
    changeAccess(a=0)
    copySource(mSrc, tmpPath, db=1)
    changeAccess(a=0)
    processFolders(tmpPath, dbLocal)
    processPages(tmpPath)
    finalizeConvert(tmpPath, dstPath)
    
if __name__ == '__main__': 
      main()