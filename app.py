
# Ilk başta flask kütüphanemizi çağırıyoruz.
from flask import Flask, redirect, url_for, request, render_template

 
# Flask yapıcısının adını alır.
# geçerli modül (__name__) argüman olarak.
app = Flask(__name__)
 
# Flask sınıfının route() işlevi bulunmaktadır,
# uygulamaya hangi URL'nin araması gerektiğini söyler.
@app.route('/', methods = ['POST', 'GET'])
# '/' URL, index() işlevine bağlıdır.
def index():
    
    #render_template ile beraber gönderilecek örnek bir değişken tanımladık.
    name = "mfg"
    
    #request metodu olarak post metodu kullanılmış mı diye bakıyoruz.
    if request.method == 'POST':
        
        #eğer about isminde butona tıklandıysa
        if request.form['submit_button'] == 'about':
            print("about_page")
            return render_template("about.html")
        
        #eğer mfg isminde butona tıklandıysa
        elif request.form['submit_button'] == 'mfg':
            print("index_page_with_html")
            return render_template("index.html", name = name)
    
    #normal açarken bu sayfa
    return render_template("index.html")

# ana sürücü işlevi
if __name__ == '__main__':
    # Flask sınıfının run() yöntemi uygulamayı çalıştırır
    # yerel geliştirme sunucusunda.
    app.run()