from flask import Flask,request,jsonify,render_template
from flask_restful import Api,Resource
from pymongo import MongoClient
import copy
from bson import json_util
import json

client=MongoClient("mongodb://db:27017")
db=client.directorsDB
directorCollection = db['director']

app=Flask(__name__)

api=Api(app)


import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def geturl_fordata():
    newcontent=[]
    #import pdb;pdb.set_trace()
    data=directorCollection.find()
    if not data:
       return None
    for item in data:
        #item.pop('_id')
        new_item={}
        new_item['_id']=str(item['_id'])
        new_item["url"]="http://10.193.113.101/directors/{}".format(item["name"])
        new_item['name']=item['name']
        new_item['movies']=item['movies']
        newcontent.append(new_item)
    return newcontent



class Directors(Resource):
    def get(self):
        new_storecontents = geturl_fordata()
        if not new_storecontents:
            return {'status':404}
        return jsonify({"directors":[ x for x in new_storecontents]})

    def post(self):
        data=request.get_json()
        #import pdb;pdb.set_trace()
        new_director={
            "name":data['name'],
            "movies":[]
        }
        directorCollection.insert_one(new_director)    
        #return {"status":200,"data":json.dumps(new_director, indent=4, default=json_util.default)}
        return {'status':201}


class Director(Resource):

    def get(self,name):
        director=directorCollection.find_one({'name':name})
        if not director:
           return {'status':404}
        new_director={}
        new_director['name']=director['name']
        new_director['movies']=director['movies']
        #new_director['_id']=
        
        return jsonify({"stauts":200,"data":new_director})

    def post(self,name):
        item=request.get_json()
        movie=item['movie']
        directorCollection.update({'name':name},{'$push':{'movies':movie}})
        return jsonify({"status":'201'})





api.add_resource(Directors,'/directors')

api.add_resource(Director,"/directors/<string:name>")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

