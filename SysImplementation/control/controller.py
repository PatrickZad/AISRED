from flask import Flask,request,render_template
from response import *

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    //TODO
@app.route('/importBackground',methods=['POST'])
def importBackground():
    //TODO
@app.route('/importGWT',methods=['POST'])
def importGWT():
    //TODO
@app.route('/selectGWTs',methods=['GET'])
def selectGWTs():
    //TODO
@app.route('/readyToTransform',methods=['POST']):
def transform():
    //TODO
if __name__=='__main__':
    app.run()