import json
import requests
import base64
import pdb
import os
import tempfile
from flask import Flask, request 
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

pdf_slicer = "https://pdf-slicer-service.gallodigital.com/pdf_to_jpgs"

@app.route("/check")
def check():
    return json.dumps({})

@app.route("/img_to_text", methods = ['POST'])
def img_to_text():
    dpi = request.args.get("dpi", default=200)
    include_jpgs = request.args.get("jpgs", default=False)
    image_data = request.data 

    with tempfile.TemporaryDirectory() as dirpath:
        filename = dirpath + "/img"  
        outputname= dirpath + "0" 
        out = { 'page_count': 1, 'pages': [] }
        page_d  = {}
        page_d['image_raw'] = base64.encodebytes(image_data).decode('ascii') 
        with open(filename, "wb") as page_image_out:
            page_image_out.write(image_data)
            cmd = 'tesseract ' + filename + " " + outputname + " --dpi " + str(dpi)
            os.system(cmd)
            with open(outputname + ".txt", 'r') as f_out:
                page_d['text'] = f_out.read() 
        out['pages'].append(page_d) 
        return json.dumps(out)

@app.route("/pdf_to_text", methods = ['POST'])
def pdf_to_text():
    dpi = request.args.get("dpi", default=200)
    include_jpgs = request.args.get("jpgs", default=False)
    pdf_data = request.data 
    response = requests.post(pdf_slicer, data=pdf_data, params={"dpi": dpi})
    image_data = (response.json())

    with tempfile.TemporaryDirectory() as dirpath:
        filename = lambda page: dirpath + str(page) +'.jpg'
        outputname= lambda page: dirpath + str(page)
        out = {} 
        out['page_count'] = image_data['page_count']
        out['pages'] = []
        for i in range(image_data['page_count']):
            image_raw = image_data['pages'][i]
            page_d = { }
            if include_jpgs:
                page_d['image_raw'] = image_raw 
            with open(filename(i), "wb") as page_image_out:
                page_image_out.write(base64.b64decode(image_raw))
                cmd = 'tesseract ' + filename(i) + " " + outputname(i) + " --dpi " + str(dpi)
                os.system(cmd)
                with open(outputname(i) + ".txt", 'r') as f_out:
                    page_d['text'] = f_out.read() 
            out['pages'].append(page_d)
        return json.dumps(out)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
