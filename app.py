from flask import Flask,render_template,request,json,Response,jsonify,send_from_directory,send_file
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename

uploads_dir='uploads'
app = Flask(__name__,template_folder="templates",static_url_path='/static',static_folder='static')

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('',methods=['GET','POST'])
def encrypt_page():
    if request.method=='GET':
        return render_template('encrypt.html')
    if request.method=='POST':
        file=request.files['file']
        key=request.form['key']
        
        file_path=os.path.join(uploads_dir, secure_filename(file.filename))
        temp_file_path=uploads_dir+'/temp/'+ secure_filename(file.filename)
        # temp_file_path_new=uploads_dir+'/'+'decoded_a/'+ secure_filename(file.filename)
        file.save(os.path.join(temp_file_path))

        fin = open(temp_file_path, 'rb') 
      
        image = fin.read() 
        fin.close() 
        
        image = bytearray(image) 
        
        key= int.from_bytes(key.encode('utf-8'), byteorder='big')%256
        
        for index, values in enumerate(image): 
            image[index] = values ^ key 

        fin = open(file_path, 'wb') 
      
        fin.write(image) 
        fin.close() 

        os.remove(temp_file_path)

        return send_file(file_path,as_attachment=True)

@app.route('/decrypt',methods=['GET','POST'])
def decrypt_page():
    if request.method=='GET':
        return render_template('decrypt.html')

if __name__=='__main__':
    app.run(debug=True)