import json
import requests
import base64
import pdb
import os
import tempfile
from flask import Flask, request 

app = Flask(__name__)

pdf_slicer = "https://pdf-slicer-service.gallodigital.com/pdf_to_jpgs"

@app.route("/check")
def check():
    return json.dumps({})

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
