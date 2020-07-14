import fnmatch
import os
import shutil
import subprocess
import sys


files = []
filename = ""
x = 0

def getFiles():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.pdf'):
            global x
            x += 1
            file = os.path.splitext(file)[0]
            files.append(file)
    print("PDFs found: {0}".format(x))

def makeTmpDir():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        print("Temporary directory created.")

def convert(file):
    global filename 
    filename = str(file)
    print("Converting {0}...".format(file))
    command = 'magick -density 300 -quality 100 "{}.pdf" "{}.jpg"'.format(file, file)
    #os.system('cmd /k "magick -density 300 -quality 100 "{}.pdf" "{}.jpg""'.format(file, file))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        print("Convertion of file {} done.".format(file))
    else:
        print("Error when trying to convert with ImageMagick.")
        exit(0)

def moveJPGs():
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.jpg"):
            shutil.move(file, "tmp/{0}".format(file))

def archive():
    print("Making archive...")
    for file in os.listdir('tmp'):
        if fnmatch.fnmatch(file, '*.jpg'):
            shutil.make_archive(filename, "zip", "tmp")
            print("Archive done.")
            break
        else:
            print("No jpgs found. Aborting")
            exit(0)

def zipToCbr():
    print("Start converting zips to CBR...")
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.zip"):
            base = os.path.splitext(file)[0]
            os.rename(file, base + ".cbr")
            print("{} converted to CBR".format(base))

def cbzToCbr():
    print("Start converting CBZ to CBR...")
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.cbz"):
            base = os.path.splitext(file)[0]
            os.rename(file, base + ".cbr")
            print("{} converted to CBR".format(base))

def deleteTempJPG():
    for file in os.listdir("tmp"):
        os.remove(os.path.join("tmp", file))

#Actual script
getFiles()
makeTmpDir()

for file in files:
    convert(file)
    moveJPGs()
    archive()
    deleteTempJPG()
    print(file + " converted to zip.")

zipToCbr()
cbzToCbr()

shutil.rmtree("tmp")
print("Temporary folder cleaned. Process completed.")
