from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from ml.model_ml import vgg16 ,inception


app = Flask(__name__)
app = Flask(__name__,static_url_path='', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif','jfif'}

global BG_COLOR
BG_COLOR = {}
BG_COLOR['Green'] = 'green'
BG_COLOR['Light'] = 'yellow'
BG_COLOR['Medium'] = 'brown'
BG_COLOR['Dark'] = 'dark'


global file_uploaded
file_uploaded =  False
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def remove_file() : 
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    

@app.route('/', methods=['POST','GET'])
def index():
    res = {}
    if request.method == 'POST':
        if 'file' not in request.files:
            return ('No file part')
            
        file = request.files['file']
        if file.filename == '':
            return ('No selected file')
           
        if file and allowed_file(file.filename):
            remove_file()
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            new_filename = f"{"testing"}.{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            file_path  = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            result_vgg16 , percentage_vgg16 = vgg16(file_path)
            result_inception, percentage_inception = inception(file_path)
            res['image'] = 'uploads/'+ new_filename
            res['percentage_vgg16'] = "{:.2f}".format(percentage_vgg16)+ "%"
            res['bg_vgg16'] = BG_COLOR[result_vgg16]
            res['result_vgg16'] = result_vgg16
            res['percentage_inception'] = "{:.2f}".format(percentage_inception) + "%"
            res['result_inception'] = result_inception
            res['bg_inception'] = BG_COLOR[result_inception]
       
            return render_template('index.html' , data = res)
    else : 
        return render_template('index.html' , data = False )


if __name__ == '__main__':
    app.run(debug=True)
