from flask import request, current_app
from flask_restful import Resource
from flasgger import swag_from

class UserClass(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "<br/>",
        "operationId": "getUserClass",
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
            "description": "Returned class"
          }
        },
        "summary": "Gets user's class."
    })
    def get(self):
        if 'id' in request.args.keys():
            sess = self.sm.getSessionByID(int(request.args['id']))
            user_class = sess.getClass()

            return {
                "class": user_class
            }
        else:
            return current_app.returnNonTwoHunderdCode(401)