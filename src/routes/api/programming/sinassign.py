from flask import request
from flask_restful import Resource
from flasgger import swag_from

class SingleProgrammingAssignment(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']
    
    @swag_from({
        "description": "Gets a specific assignment from this school quarter.",
        "operationId": "getProgrammingAssignment",
        "tags": ["Programming"],
        "parameters": [
          {
            "allowEmptyValue": False,
            "description": "Session ID",
            "in": "query",
            "name": "id",
            "required": True,
            "type": "integer"
          },
          {
            "allowEmptyValue": False,
            "description": "Name of the assignment you're fetching",
            "in": "path",
            "name": "Assignment name",
            "required": True,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Returned a programming assignment"
          }
        },
        "summary": "Gets a single programming assignment"
    })
    def get(self, name: str):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            assignment = sess.getProgrammingAssignment(name)
            
            return {
                "assignment": assignment
            }
        else:
            return self.returnNonTwoHunderdCode(401)