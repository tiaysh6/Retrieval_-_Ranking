from flask import Flask, request, make_response
import tempfile
from getCollectionList import getCollection
from creatreCollection import createCollection
from query import getResult
from flask import jsonify
from PyPDF2 import PdfReader


app=Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_pdf():
  # Check if a file was uploaded
  if 'file' not in request.files:
    return make_response("No file uploaded!", 400)

  # Get the uploaded file
  uploaded_file = request.files['file']
  print(uploaded_file)
  reader=PdfReader(uploaded_file)
  print(reader.getNumPages())
  createCollection(uploaded_file,"tmp")

#   # Check if the file is a PDF
#   if uploaded_file.filename.lower().endswith(".pdf") is False:
#     return make_response("Only PDF files allowed!", 400)

#   # Create a secure filename using tempfile module

#   with tempfile.NamedTemporaryFile(dir="tmp", suffix=".pdf", delete=False) as temp_file:
#    filename = temp_file.name
#     # Save the file to the temporary location
#    uploaded_file.save(filename)

# #   # Success message (you can add further processing logic here)
  return f"File uploaded successfully: c"
    

@app.before_request 
def before():
    print("This runs before anything")

@app.route('/collections/')
def getNames():
    return jsonify(getCollection())

@app.route('/query/<string:query>/<string:collection_name>')
def getQuery(query,collection_name):
    result= getResult(query, collection_name)
    return jsonify(result)

@app.route('/create/<string:path>/<string:collection_name>')
def makeCollection(path,collection_name):
    result=createCollection(path,collection_name)
    return jsonify(result)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=105)
    


