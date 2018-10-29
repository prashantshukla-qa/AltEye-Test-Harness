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
verify_Guidelines = Verify_Guidelines()
from html_parser.Image_html_parser import Image_html_parser

app = Flask(__name__)
import json


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
    print(request.form)
    if request.method == 'GET':
        return home()
    # if "wikipedia" not in request.form['test-url']:
    #     flash('This demo works only on Wikipedia!!!')
    #     return home()
    if request.form['action'] == 'Get Alt Text':
        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_images_and_alt_text()
        if image_details.__len__() == 0:
            flash("no Images found")
            # flash('Either \'infobox\' or \'image in infobox\' \
            #     is absent from the webpage!!!')
            return home()
        return render_template('resultpage-alt.html', data=image_details)
    if request.form['action'] == 'Test Alt Text Relevancy':
        modelValue= request.form['model']
        methodValue=request.form['method']
        Threshold=request.form['Threshold']
        width=request.form['width']
        height=request.form['height']
        if Threshold=='':Threshold=50
        if width=='':width=50
        if height=='':height=50

        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_vision_feedback(modelValue,Threshold,methodValue,width,height)
        if image_details.__len__() == 0:
            flash('no Images found')
            return home()
        return render_template('resultpage.html', data=image_details)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


@app.route('/api/get_alt_relevancy/', methods=['GET'])
def get_Alt_relevancy():
    # print(dir(request))
    url = request.args.get('url')
    alt = request.args.get("alt")
    if request.args.get("vicinity"):
        vicinity_text = request.args.get("vicinity")
    else:
        vicinity_text = ""

    if request.args.get("method"):
        method = request.args.get("method")
    else:
        method = "googleAPI"

    if request.args.get("Threshold"):
        Threshold = int(request.args.get("Threshold"))
    else:
        Threshold = 30

    if request.args.get("Model"):
        Model = request.args.get("Model")
    else:
        Model = "DenseNet"

    result = verify_Guidelines.ExtractClasses(
        url, alt, vicinity_text, method, Threshold, Model)
    result["text_classes"] = list(result["text_classes"])
    return jsonify(result)


@app.route('/api/get_alt_relevancy/', methods=['POST'])
def get_Alt_relevancy_via_source():
    # print(dir(request))
    jsonContent = request.data
    body = json.loads(jsonContent)
    url = body['url']
    html_content = body['html_content']
    if body["method"]:
        method = body["method"]
    else:
        method = "googleAPI"

    if body["Threshold"]:
        Threshold = int(body["Threshold"])
    else:
        Threshold = 30

    if body["Model"]:
        Model = body["Model"]
    else:
        Model = "DenseNet"
    list_of_alt_vicinity_data = Image_html_parser(
        html_content).get_Images_alt_vicinity()
    list_of_alt_vicinity_data = [ url+x[0] for x in list_of_alt_vicinity_data]
    for img_data in list_of_alt_vicinity_data:
        result = verify_Guidelines.ExtractClasses(
            img_data[0], img_data[1], img_data[2], method, Threshold, Model)
        result["text_classes"] = list(result["text_classes"])
    return jsonify(result)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)
