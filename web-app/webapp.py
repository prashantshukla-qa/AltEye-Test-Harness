import os
from flask import Flask, render_template, session, request, flash, redirect
from accessibility_app.launch_browser import PageParser
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from  Verify_Guidelines import Verify_Guidelines
import glob

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('homepage.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and \
            request.form['username'].lower() == 'admin':
        session['logged_in'] = True
        return redirect("/", code=302)
    else:
        flash('wrong username or password!')
    return home()


@app.route('/search', methods=['POST'])
def search_weburl():
    for files in glob.glob("web-app/static/images/retrieved_images/*"):
        os.unlink(files)

    data_dictionary=[]
    image_details = PageParser("chrome", request.form['test-url']) \
        .getImagesAndAltText()
    
    i=0
    for image_detail in image_details:
        verify_guidelines=Verify_Guidelines.Verify_Guidelines()
        classes=verify_guidelines.ExtractClasses(image_details[image_detail]["src"],image_details[image_detail]["alt"],image_details[image_detail]["vicinity_text"])
        data_dictionary.append({"imageinfo": image_details, "classes":classes})
        image_details[image_detail]["classes"]=classes 
    print(image_details)
    return render_template('resultpage.html', data=image_details)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True)
