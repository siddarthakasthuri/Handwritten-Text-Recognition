import os
from flask import Flask, render_template, request, url_for # type: ignore
from model import Model, DecoderType
from main import infer, char_list_from_file

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'  # Directory to save uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/')
def index():
    return render_template('design.html')

@app.route('/submit_image', methods=['POST', 'GET'])
def submitForm():
    reg = None
    img_url = None
    if request.method == 'POST':
        img = request.files['image']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save(file_path)
        
        model = Model(char_list_from_file(), DecoderType.BestPath, must_restore=True)
        result = infer(model, file_path)
        reg = str(result[0])
        
        img_url = url_for('static', filename=f'uploads/{img.filename}')
    
    return render_template('index.html', res=reg, img_url=img_url)

if __name__ == '__main__':
    app.run(debug=True)