from flask import request
from flask_restful import Resource
from flasgger import swag_from

class FullName(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "Gets the user's full name, including any middle names in an array.",
        "operationId": "getUserFullName",
        "tags": ["User info"],
        "parameters": [
          {
            "allowEmptyValue": False,
            "description": "Session ID",
            "in": "query",
            "name": "id",
            "required": True,
            "type": "integer"
          }
        ],
        "responses": {
          "200": {
            "description": "Returned full name."
          }
        },
        "summary": "Get the user's full name"
    })

    def get(self):
        sess = self.sm.getSessionByID(int(request.args['id']))
        name = sess.getUserFullName()
        
        if len(name) == 2:
            return {
                "firstName": name[0],
                "lastName": name[1]
            }
        else:
            return {
                "firstName": name[0],
                "middleNames": name[1:][:-1],
                "lastName": name[-1]
            }