from flask import Flask,request,jsonify,render_template
from flask_restful import Api,Resource
import copy

app=Flask(__name__)

api=Api(app)

storecontents=[
    {
        "name":"QuentinTorantino",
        "movies":["kill bill","reservoir dogs"],
    },
    {
        "name":"David Fincher",
        "movies":["fight club","social network"]
    }
   ]

def geturl_fordata(ls):
    copy_ls=copy.deepcopy(ls)
    newcontent=[]
    for item in copy_ls:
        item["url"]="http://10.193.113.101:5010/directors/{}".format(item["name"])
        newcontent.append(item)
    return newcontent



class Directors(Resource):
    def get(self):
        new_storecontents = geturl_fordata(storecontents)
        return jsonify({"storecontents":[ x for x in new_storecontents]})

    def post(self):
        data=request.get_json()
        #import pdb;pdb.set_trace()
        new_director={
            "name":data['name'],
            "movies":[]
        }
        storecontents.append(new_director)
        return {"status":200,"data":new_director}


class Director(Resource):

    def get(self,name):
        director = [x for x in storecontents if x["name"] == name][0]
        return jsonify({"stauts":200,"data":director})

    def post(self,name):
        item=request.get_json()
        movie=item['movie']
        for dirctr in storecontents:
            if dirctr["name"]==name:
                dirctr["movies"].append(movie)
                return jsonify({"status":200})





api.add_resource(Directors,'/directors')

api.add_resource(Director,"/directors/<string:name>")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5010)

