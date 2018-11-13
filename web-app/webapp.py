import glob
import os
import sys
for filename in glob.iglob('**/*', recursive=True):
    if(os.path.isdir(os.getcwd()+"/"+filename)):
        sys.path.append(filename)
from flask import Flask, render_template, session, request, flash, redirect, jsonify, url_for
from accessibility_app.launch_browser import PageParser
from accessibility_app.Verify_Guidelines import Verify_Guidelines
import json
verify_Guidelines = Verify_Guidelines()
from html_parser.Image_html_parser import Image_html_parser
from werkzeug.utils import secure_filename

app = Flask(__name__)
import json

UPLOAD_FOLDER = './static/images/retrieved_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    if request.form['action'] == 'Get Alt Text':
        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_images_and_alt_text()
        if image_details.__len__() == 0:
            flash("no Images found")
            return home()
        return render_template('resultpage-alt.html', data=image_details)
    if request.form['action'] == 'Test Alt Text Relevancy':
        modelValue = request.form['model']
        Threshold = request.form['Threshold']
        width = request.form['width']
        height = request.form['height']
        imageCount = request.form['imageCount']
        if Threshold == '':
            Threshold = 60
        if width == '':
            width = 50
        if height == '':
            height = 50
        if imageCount == '':
            imageCount = 4

        image_details = PageParser("chrome", request.form['test-url'])\
            .launch_browser().get_vision_feedback(modelValue, int(Threshold), int(width), int(height), int(imageCount))
        if image_details.__len__() == 0:
            flash('no Images found')
            return home()
        for image in image_details:
            image_web_entity=[]
            image_entity=[]
            for texts in image["classes"]["possible_texts"]:
                if "(Web-Entity)" in texts["Entity"]:
                    texts["Entity"]=texts["Entity"].replace("(Web-Entity)","")
                    image_web_entity.append(texts)
                else:
                    image_entity.append(texts)
            image["classes"]["image_web_entity"]=image_web_entity
            image["classes"]["image_entity"]=image_entity
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

    if request.args.get("Threshold"):
        Threshold = int(request.args.get("Threshold"))
    else:
        Threshold = 30

    if request.args.get("Model"):
        Model = request.args.get("Model")
    else:
        Model = "DenseNet"
    if request.form.get("custommodel"):
        CustomModel = request.form.get("custommodel")
    else:
        CustomModel = None
    if request.form.get("customjsonfile"):
        CustomJsonPath = request.form.get("Model")
    else:
        CustomJsonPath = None

    result = verify_Guidelines.ExtractClasses(
        url, alt, vicinity_text, Threshold, Model,CustomModel, CustomJsonPath)
    result["text_classes"] = list(result["text_classes"])
    return jsonify(result)


@app.route('/api/upload_image_get_relevancy', methods=['POST'])
def upload_file():
    # checking if the file is present or not.
    if 'file' not in request.files:
        return {"error": "No file found"}
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file successfully saved")

        # print(dir(request))
    url = "local://"+file.filename
    alt = request.form.get("alt")
    if request.form.get("vicinity"):
        vicinity_text = request.form.get("vicinity")
    else:
        vicinity_text = ""

    if request.form.get("Threshold"):
        Threshold = int(request.form.get("Threshold"))
    else:
        Threshold = 30

    if request.form.get("Model"):
        Model = request.form.get("Model")
    else:
        Model = "DenseNet"
    if request.form.get("custommodel"):
        CustomModel = request.form.get("custommodel")
    else:
        CustomModel = None
    if request.form.get("customjsonfile"):
        CustomJsonPath = request.form.get("Model")
    else:
        CustomJsonPath = None

    result = verify_Guidelines.ExtractClasses(
        url, alt, vicinity_text, Threshold, Model, CustomModel, CustomJsonPath)
    result["text_classes"] = list(result["text_classes"])
    return jsonify(result)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)
