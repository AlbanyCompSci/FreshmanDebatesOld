from flask             import request
from flask.ext.restful import Resource

#TODO: check return status codes

class ResourceId(Resource):
    def __init__(self, rtype, db):
        self.rtype = rtype
        self.db    = db
    def get(self, rid):
        item = self.db.read(self.rtype, rid)
        if item == None:
            return '', 404
        return item.show()
    def put(self, rid):
        item = self.rtype.read(request.form)
        found = self.db.update(self.rtype, rid, item)
        if not found:
            return '', 404
        return item, 201
    def delete(self, rid):
        found = self.db.delete(self.rtype, rid)
        if not found:
            return '', 404
        return '', 204

class ResourceList(Resource):
    def __init__(self, rtype, db):
        self.rtype = rtype
        self.db    = db
    def get(self):
        return map(lambda i: i.show(), self.db.list(self.rtype))
    def post(self):
        rid = self.db.create(self), 201

def addResource(api, db, rtype, name):
    api.add_resource(ResourceId(rtype, db),   '/' + name)
    api.add_resource(ResourceList(rtype, db), '/' + name + '/<int:rid>')
