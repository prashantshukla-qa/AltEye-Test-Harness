import os
from flask import Flask, render_template, session, request, flash, redirect
from accessibility_app.launch_browser import PageParser

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('homepage.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and\
            request.form['username'].lower() == 'admin':
        session['logged_in'] = True
        return redirect("/", code=302)
    else:
        flash('wrong username or password!')
    return home()


@app.route('/search', methods=['GET', 'POST'])
def search_weburl():
    if request.method == 'GET':
        return home()
    if "wikipedia" not in request.form['test-url']:
        flash('This demo works only on Wikipedia!!!')
        return home()
    if request.form['action'] == 'Get Alt Text':
        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_images_and_alt_text()
        if image_details.__len__() == 0:
            flash('Either \'infobox\' or \'image in infobox\' \
                is absent from the webpage!!!')
            return home()
        return render_template('resultpage-alt.html', data=image_details)
    if request.form['action'] == 'Test Alt Text Relevancy':
        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_vision_feedback()
        if image_details.__len__() == 0:
            flash('Either \'infobox\' or \'image in infobox\' \
                is absent from the webpage!!!')
            return home()
        return render_template('resultpage.html', data=image_details)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=False)
