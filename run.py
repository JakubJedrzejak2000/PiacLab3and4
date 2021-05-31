import azure as azure
from flask import Flask, render_template, url_for, abort, make_response, request
import smtplib
import keyring

app = Flask(__name__)


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


@app.route('/contact', methods=['GET', 'POST'])
def form():
    nickname = request.form.get("nickname")
    email = request.form.get("email")
    text = "From:<pythoncloudjakub@gmail.com>\nTo:<" + str(email) + ">\nSubject:Wiadomosc\nWitaj " + str(
        nickname) + "~!\nTwoja wlasna wiadomosc!\n" + request.form.get("text")
    print(text)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("pythoncloudjakub@gmail.com", keyring.get_password("test", "pythoncloudjakub@gmail.com"))
    server.sendmail("pythoncloudjakub@gmail.com", email, text)
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
