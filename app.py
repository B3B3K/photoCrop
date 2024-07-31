from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
lete = ""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_letter', methods=['POST'])
def ask_letter():
    letter = request.form.get('letter')
    if not letter or len(letter) != 1:
        return redirect(url_for('index'))
    isExist = os.path.exists("harf/"+letter)
    global lete
    lete = letter
    if not isExist:
       os.makedirs("harf/"+letter)
    return redirect(url_for('upload_image'))

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_image'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('upload_image'))
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
            file.save(filepath)
            return redirect(url_for('display_image'))
    return render_template('upload.html')

@app.route('/display_image')
def display_image():
    return render_template('display.html')




def jpgs(let):
    folder_path = "harf/"+let
    png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    
    if not png_files:
        return "0"
    else:
        # Find all .jpg files and extract their numeric values
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
        if jpg_files:
            # Extract numeric values from filenames
            jpg_numbers = [(f, int(re.search(r'(\d+)', f).group())) for f in jpg_files]
            # Sort by numeric value and select the last one
            jpg_files_sorted = sorted(jpg_numbers, key=lambda x: x[1])
            return str(jpg_files_sorted[-1][0])
        else:
            return "0"



def crop_coords(x,y):
    im = Image.open("static/uploads/uploaded_image.jpg").convert('L')
    x = int(x)
    y = int(y)
    im = im.crop((x, y, x + 20, y + 28))
    global lete
    fin = jpgs(lete).replace(".jpg","")
    print(fin)
    fin = str(int(fin) + 1)
    directory = "harf/"+lete+"/"+fin
    im.save(directory+".jpg")


@app.route('/click_coords', methods=['POST'])
def click_coords():
    x = request.form.get('x')
    y = request.form.get('y')
    if x and y:
        global lete
        print(f"Coordinates: x={x}, y={y}")
        crop_coords(x,y)
    return '', 204




if __name__ == '__main__':
    app.run(debug=True)
