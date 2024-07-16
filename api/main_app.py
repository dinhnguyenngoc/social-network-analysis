import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)


@app.route('/')
def home():
    return 'xin chào bạn đến với nhóm 9 - hệ cơ sở dữ liệu'

@app.route('/getprediction',methods=['POST'])
def getprediction():    

    input = [float(x) for x in request.form.values()]
    final_input = [np.array(input)]

    return 'xin chào bạn đến với python'
   

if __name__ == "__main__":
    app.run(debug=True)