import sys

from flask import Flask, render_template, url_for, abort, make_response, request, redirect
from flask_mail import Mail, Message
from AzureDB import AzureDB

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pythoncloudjakub@gmail.com'
app.config['MAIL_PASSWORD'] = 'nwwyjeatddpyobbs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/aboutme")
def aboutme():
    return render_template("aboutme.html")


@app.route("/gallery")
def gallery():
    return render_template('gallery.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/error_not_found")
def error_not_found():
    response = make_response(render_template('template.html', name="ERROR 404"), 404)
    response.headers['X-Something'] = 'A value'
    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/contact', methods=['POST'])
def form():
    try:
        nickname = request.form.get("nickname")
        email = request.form.get("email")
        text = request.form.get("text")
        msg = Message(nickname, sender='pythoncloudjakub@gmail.com', recipients=[email])
        msg.body = text
        mail.send(msg)
        return redirect('contact')
    except:
        print(sys.exc_info()[0])


@app.route('/guestbook')
def guests():
    return render_template("layout.html")


@app.route('/guestbook', methods=['POST'])
def guestsform():
    with AzureDB() as a:
        a.azureAddData(request.form.get("nickname"), request.form.get("content"), request.form.get("date"))
    return redirect('guestbook')

@app.route('/guests')
def guestbook():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("guests.html", data=data)


@app.route('/delguest/<id>', methods=['get'])
def delete(id):
    with AzureDB() as a:
        a.azureDeleteData(id)
    return redirect('/guests')


@app.route('/edycja/<id>', methods=['get'])
def edycja(id):
    with AzureDB() as a:
        data = a.azureGetParticularDate(id)
    return render_template('edit.html', data=data)


@app.route('/edytowanie', methods=['post'])
def edit():
    name = request.form.get("nickname")
    text = request.form.get("text")
    date = request.form.get("date")
    id = request.form.get("id")
    with AzureDB() as a:
        a.azureUpdateData(id, name, text, date)
    return redirect('/guests')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
