# 1. İlk başta kütüphanelerimizi çağırıyoruz.
import shutil
import subprocess
import os
import sys
import sqlite3

# 2. Kullanıcının vereceği değeri burada değişkene aktarıyoruz.
updateVersion = sys.argv[1]
global imlec


# 3. Kütüphanemize bağlantımızı yapıyoruz.
database_connect = sqlite3.connect("neka_sla.db")
imlec = database_connect.cursor()

# 4. Burada kütüphanemizde versiyonumuzu güncelliyoruz.
# Bu şekilde yeni bir güncelleme gelene kadar bize güncelleme var diye bir şey demeyecek.
imlec.execute(f"""UPDATE Version_Tag SET version = '{updateVersion}' WHERE id = 1;""")
files = imlec.fetchall()
database_connect.commit()
database_connect.close()

# 5. Asıl programımızı kapatarak devam ediyoruz.
os.system("pkill -f app.py")

# 6. Şimdi yükleme işlemlerimizi kolaylaştırmak için yolları değişkenlere atıyoruz.
dukkan = os.getcwd() #Bu asıl adres
cwd = os.getcwd().split("/")[1:] 
pwd = "" #Bu bizim mekanın bulunduğu yol.
for c in range(len(cwd) - 1):
    pwd += "/" + cwd[c]

# 7. Burada silinmemesini istediğimiz bir klasörü mekana kaydedelim diyoruz ve kopyalıyoruz.
try:
    os.mkdir(f"{pwd}/.programFiles")
except:
    print("File Exists!")


# 7.1 Gerekli dediğimiz dosyalarımızı mekana kopyalıyoruz burada. 
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

# 8. Şuan bulunduğumuz dosyayı siliyoruz.
try:
    shutil.rmtree(dukkan)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


# 9. Yeni dosyayı indiriyoruz github'tan, bu fonksiyonun kendisi.
def git(*args):
    return subprocess.check_call(["git"] + list(args))


# 10. Burada yapıyoruz yükleme işlemini.
os.chdir(pwd)
git(
    "clone",
    "https://github.com/Mastechnology/self-updater-flask.git",
    "-b",
    updateVersion,
)

# 11. Dosya içeride yoksa açıyoruz.
try:
    os.mkdir(f"{pwd}/.programFiles")
except:
    print("File Exists!")

# 12. Gerekli dosyalari geri indiriyoruz ve gereksizleri siliyoruz.
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

# 13. Yol değiştiriyoruz ve içeri giriyoruz.
os.chdir(dukkan)

# 14. Burada git checkout yapıyoruz ve işlemler bitiyor.
git("checkout", "-b", "main")

# Burada programımızı tekrardan çalıştırıyoruz. Ekran güncelleyince tamamlanıyor.
subprocess.call("python3 app.py &", shell=True)
