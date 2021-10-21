import shutil
import subprocess
import os
import sys
import sqlite3

updateVersion = sys.argv[1]
global imlec

profileArray = []
database_connect = sqlite3.connect("neka_sla.db")
imlec = database_connect.cursor()

imlec.execute(f"""UPDATE Version_Tag SET version = '{updateVersion}' WHERE id = 1;""")
files = imlec.fetchall()
database_connect.commit()
database_connect.close()


print("I am child! " + updateVersion)
os.system("pkill -f app.py")
# ilk once bir isimleri ayarliyoruz.
dukkan = os.getcwd()
cwd = os.getcwd().split("/")[1:]
pwd = ""
for c in range(len(cwd) - 1):
    pwd += "/" + cwd[c]

print(cwd)
print(pwd)

try:
    os.mkdir(f"{pwd}/.programFiles")
except:
    print("File Exists!")


# gerekli dosyalari bir saklayacagiz.
original = f"{dukkan}/.programFiles/encrypted.txt"
target = f"{pwd}/.programFiles/encrypted.txt"
shutil.copyfile(original, target)
original = f"{dukkan}/.programFiles/key.key"
target = f"{pwd}/.programFiles/key.key"
shutil.copyfile(original, target)
original = f"{dukkan}/neka_sla.db"
target = f"{pwd}/neka_sla.db"
shutil.copyfile(original, target)
original = f"{dukkan}/updateToNew.py"
target = f"{pwd}/updateToNew.py"
shutil.copyfile(original, target)

# suanki bulundugumuz dosyayi siliyoruz
try:
    shutil.rmtree(dukkan)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


# yeni dosyayi indiriyoruz
def git(*args):
    return subprocess.check_call(["git"] + list(args))


os.chdir(pwd)
git(
    "clone",
    "https://github.com/Mastechnology/self-updater-flask.git",
    "-b",
    updateVersion,
)

try:
    os.mkdir(f"{pwd}/.programFiles")
except:
    print("File Exists!")

# gerekli dosyalari geri indiriyoruz ve gereksizleri siliyoruz.
target = f"{dukkan}/.programFiles/encrypted.txt"
original = f"{pwd}/.programFiles/encrypted.txt"
shutil.copyfile(original, target)
target = f"{dukkan}/.programFiles/key.key"
original = f"{pwd}/.programFiles/key.key"
shutil.copyfile(original, target)
target = f"{dukkan}/neka_sla.db"
original = f"{pwd}/neka_sla.db"
shutil.copyfile(original, target)
try:
    shutil.rmtree(f"{pwd}/.programFiles")
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
os.remove(f"{pwd}/neka_sla.db")
os.remove(f"{pwd}/updateToNew.py")

os.chdir(dukkan)
git("checkout", "-b", "main")
subprocess.call("python3 app.py &", shell=True)
