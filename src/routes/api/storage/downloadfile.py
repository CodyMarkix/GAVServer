from flask import request, current_app
from flask_restful import Resource
from flasgger import swag_from

class DownloadFile(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "Gets all the files in the user's storage.",
        "operationId": "login",
        "tags": ["Storage"],
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
            "description": "Returned a list of files."
          }
        },
        "summary": "Gets the user's files."
    })
    def get(self, file_name: str):
        sess = self.sm.getSessionByID(int(request.args['id']))
        file = sess.downloadFiles([file_name])

        return {
            
        }