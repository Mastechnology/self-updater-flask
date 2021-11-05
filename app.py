# Ilk başta flask kütüphanemizi çağırıyoruz.
from flask import Flask, redirect, url_for, request, render_template, jsonify
import sqlite3
import subprocess

global imlec

# Flask yapıcısının adını alır.
# geçerli modül (__name__) argüman olarak.
app = Flask(__name__)

# Flask sınıfının route() işlevi bulunmaktadır,
# uygulamaya hangi URL'nin araması gerektiğini söyler.
@app.route("/", methods=["POST", "GET"])
# '/' URL, index() işlevine bağlıdır.
def index():
    global imlec

    # render_template ile beraber gönderilecek örnek bir değişken tanımladık.
    thisVersion = ""

    # request metodu olarak post metodu kullanılmış mı diye bakıyoruz.
    if request.method == "POST":

        # eğer about isminde butona tıklandıysa
        if request.form["submit_button"] == "about":
            print("about_page")
            return render_template("about.html")

        # eğer mfg isminde butona tıklandıysa
        elif request.form["submit_button"] == "mfg":
            print("index_page_with_html")
            database_connect = sqlite3.connect("neka_sla.db")
            imlec = database_connect.cursor()
            imlec.execute(
                """
                        SELECT version FROM Version_Tag;
                        """
            )
            files = imlec.fetchall()

            for file in files:
                thisVersion = file[0]
                print(file[0])
                thisVersion = thisVersion[1:]
            return render_template("index.html", thisVersion=thisVersion)

    # normal açarken bu sayfa
    return render_template("index.html")

#burada şuanki versiyonu hakkkında bilgi alıyoruz.
@app.route("/getTheVersion", methods=["GET", "POST"])
def getTheVersion():
    global imlec
    thisVersion = ""
    #veri tabanımıza bağlanıyoruz ilk başta.
    database_connect = sqlite3.connect("neka_sla.db")
    imlec = database_connect.cursor()
    imlec.execute(
        """
                SELECT version FROM Version_Tag;
                """
    )
    files = imlec.fetchall()

    for file in files:
        thisVersion = file[0]
        print(file[0])
        thisVersion = thisVersion[1:]
        #değerimizi bu şekilde alıp front-end'e yönlendiriyoruz.
    return jsonify(thisVersion=thisVersion)

#bununla beraber başka bir python script'imizi çalıştırıyoruz.
@app.route("/updating", methods=["GET", "POST"])
def updating():
    #ilk front-end'den versiyon değerimizi alıyoruz.
    newVersion = str(request.args.get("newVersion", 0, type=str))
    print(newVersion)
    #sonrasında o değerle beraber kodumuzu çalıştırıyoruz ve güncellemeye başlıyoruz.
    subprocess.call(f"python3 updateToNew.py v{newVersion} &", shell=True)
    return jsonify(newVersion=newVersion)


# ana sürücü işlevi
if __name__ == "__main__":
    # Flask sınıfının run() yöntemi uygulamayı çalıştırır
    # yerel geliştirme sunucusunda.
    app.run(host="0.0.0.0", port="8000", threaded=True)
