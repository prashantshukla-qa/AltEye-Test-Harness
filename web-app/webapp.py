import glob
import os
import sys
for filename in glob.iglob('**/*', recursive=True):
     if(os.path.isdir(os.getcwd()+"/"+filename)):
         sys.path.append(filename)
from flask import Flask, render_template, session, request, flash, redirect, jsonify
from accessibility_app.launch_browser import PageParser
from accessibility_app.Verify_Guidelines import Verify_Guidelines
import json


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

@app.route('/api/get_alt_relevancy/', methods=['GET'])
def get_Alt_relevancy():
    verify_Guidelines=Verify_Guidelines()
    url=request.args.get('url')
    alt=request.args.get("alt")
    if request.args.get("vicinity"): 
        vicinity_text=request.args.get("vicinity") 
    else: vicinity_text=""
    if request.args.get("method"):
         method=request.args.get("method")
    else: method="googleAPI"
    if request.args.get("Threshold"): 
        Threshold=request.args.get("Threshold") 
    else: Threshold=30
    if request.args.get("Model"): 
        Model=request.args.get("Model") 
    else:
         Model="DenseNet"
    result=verify_Guidelines.ExtractClasses(url, alt,vicinity_text,method,Threshold,Model)
    result["text_classes"]=list(result["text_classes"])
    return jsonify(result)
    



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=False)
