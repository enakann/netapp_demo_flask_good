from flask import Flask,render_template,send_file
import os
from pymongo import MongoClient

client=MongoClient("mongodb://db:27017")
db=client.directorsDB
directorCollection = db['director']


app=Flask(__name__,template_folder='template')
@app.route('/')
def web_home():
    #index_path = os.path.join(app.static_folder, "index2.html")
    directors=[]
    data=directorCollection.find()
    for item in data:
        new_item={}
        new_item['name']=item['name']
        new_item['movies']=item['movies']
        directors.append(new_item)    
    return render_template("index.html",directors=directors)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
