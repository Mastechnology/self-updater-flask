import shutil
import os

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
original = f"{dukkan}/test.py"
target = f"{pwd}/test.py"
shutil.copyfile(original, target)

# suanki bulundugumuz dosyayi siliyoruz
try:
    shutil.rmtree(dukkan)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


def git(*args):
    return subprocess.check_call(["git"] + list(args))


os.chdir(pwd)
git("clone", "https://github.com/Mastechnology/self-updater-flask.git", "-b", "v0.6.2")

# os.chdir(f"{dukkan[:7]}")
