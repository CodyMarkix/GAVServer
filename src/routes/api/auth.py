from flask import request, current_app
from flask_restful import Resource
from flasgger import swag_from

class Auth(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "<br/>",
        "operationId": "login",
        "parameters": [
          {
            "allowEmptyValue": False,
            "description": "Authenticatee's e-mail",
            "in": "query",
            "name": "E-mail",
            "required": True,
            "type": "string"
          },
          {
            "allowEmptyValue": False,
            "description": "Authenticatee's password",
            "in": "query",
            "name": "Password",
            "required": True,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Succesfully authenticated and the API has returned a session ID. Expires after a week."
          }
        },
        "summary": "Authentication to the API.",
        "tags": [
          "authentication"
        ]
    })
    def post(self):
        if request.method == "POST":
            args = request.args
            
            for entry in self.sm.getAllSessions():
                for session in entry.values():
                    if args['email'] == session.mail:
                        return {
                            "message": "Already authenticated!",
                            "sessionID": session.id
                        }

            sess = self.sm.addSession(args['email'], args['password'])

            return {
                "message": "Authenticated successfuly!",
                "sessionID": sess[0]
            }
        else:
            return current_app.returnNonTwoHunderdCode(405)