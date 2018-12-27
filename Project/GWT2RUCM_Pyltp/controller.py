import
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from response import backgroundresponse,gwtresponse,rucmresponse
from support.nlpsupport import NLPExecutor
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


nlp = NLPExecutor(r'../stanford-corenlp-full-2018-10-05')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             # filename = secure_filename(file.filename)
#             file.save(os.path.abspath('.')+'\\upload')
#             # .save(os.path.abspath('.').join(app.config['UPLOAD_FOLDER'], file.filename))
#             return redirect(url_for('uploaded_file', filename=file.filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form action="" method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''

# 等过段时间可以改成Ajax版本


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/import_background', methods=['POST'])
def import_background():
    # 调用导入领域背景
    file = request.files['file']
    return render_template('index.html')


@app.route('/import_GWT', methods=['POST'])
def import_gwt():
    # 调用导入gwt
    file = request.files['file']
    return render_template('index.html')


@app.route('/Translation', methods=['POST'])
def translation():
    # 调用控制器的生成 RUCM
    return render_template('index.html', message='转化成功')


if __name__ == '__main__':
    app.run()
