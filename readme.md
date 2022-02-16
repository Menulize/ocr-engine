# OCR Engine
- Python API wrapper around tesseract in combination with a PDF slicer to generate TXT for each page of a PDF
- Can optionally return back JPG with the text for each page

## Usage CURL
```
curl  --request POST --data-binary "@file.pdf" http://localhost:5000/pdf_to_text?dpi=400&jpgs 
```

## Usage Python
```
import requests
import json
import base64
...
with open(filename(i), "rb") as pdf:
  pdf_data = pdf.read()
  response = requests.post(ocr_endpoint, data=pdf_data, params={"dpi": 400 })
  pages_data = response.json()
  for page in pages_data['pages']:
    txt = page['text']
    jpg = base64.b64decode(page['image_raw'])
    # do something ...
   
```

## Output JSON
```
{
  "page_count": 7,
  "pages": [
    {
      "image_raw": base64EncodedJPG,
      "text": "Grilled or Crispy Buffalo Chicken, Romaine, Caesar\nDressing, Parmesan, Crushed Croutons, Duck Fat..."
    },
    ...
  ]
}
```

## Install instructions (Ubuntu)
```
sudo apt-get update
sudo apt-get -y install python3-pip
pip3 install flask waitress
sudo apt-get install -y poppler-utils
sudo add-apt-repository -y ppa:alex-p/tesseract-ocr5
sudo apt install -y tesseract-ocr
```
## Run server
### production
```python3 app.py``` 
### development: 
```flask run```
