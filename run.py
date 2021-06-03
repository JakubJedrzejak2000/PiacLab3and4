import sys

from flask import Flask, render_template, url_for, abort, make_response, request
import keyring
from flask_mail import Mail, Message

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
        return render_template('contact.html')
    except:
        print(sys.exc_info()[0])


if __name__ == '__main__':
    app.run(host="0.0.0.0")
