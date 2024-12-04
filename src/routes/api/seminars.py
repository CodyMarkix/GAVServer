from flask import request
from flask_restful import Resource
from flasgger import swag_from

class Seminars(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']
    
    @swag_from({
        "description": "Gets seminars the user is enrolled in.",
        "operationId": "getSeminars",
        "tags": ["Seminars"],
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
            "description": "Returns seminars"
          }
        },
        "summary": "Gets all seminars"
    })
    def get(self):
        sess = self.sm.getSessionByID(int(request.args['id']))
        seminars = sess.getSeminars()

        return {
            "seminars": seminars
        }