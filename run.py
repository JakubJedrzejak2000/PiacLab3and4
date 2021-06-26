import os
import sys

from flask import Flask, render_template, url_for, abort, make_response, request, redirect, session
from flask_mail import Mail, Message
from AzureDB import AzureDB
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import logout_user, LoginManager, login_user

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pythoncloudjakub@gmail.com'
app.config['MAIL_PASSWORD'] = 'nwwyjeatddpyobbs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

google_blueprint = make_google_blueprint(
    client_id="260667272711-bsngqdtnmr7coe9tl7tcd86bkt6sah5j.apps.googleusercontent.com",
    client_secret="DAxRqSE0KKl5BNSo6T8AJ_PE"
)

github_blueprint = make_github_blueprint(
    client_id="036ec94f9eeed8ddd604",
    client_secret="cfc95a239f7a5961587739b896d2e0b01b80cda1"
)
app.register_blueprint(google_blueprint, url_prefix='/login')
app.register_blueprint(github_blueprint, url_prefix='/login')


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
    return render_template("layout.html", )


@app.route('/guestbook', methods=['POST'])
def guestsform():
    with AzureDB() as a:
        a.azureAddData(request.form.get("nickname"), request.form.get("content"), request.form.get("date"))
    return redirect('guestbook')


@app.route('/guests')
def guestbook():
    if github.authorized or google.authorized:
        login = True
    else:
        login = False
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("guests.html", data=data, login=login)


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


@app.route('/logingithub')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return redirect(url_for('home'))
        return "<h1>Błąd!</h1>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/logingoogle')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

