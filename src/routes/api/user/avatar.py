from flask import request, make_response
from flask_restful import Resource
from flasgger import swag_from

class Avatar(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "Fetches the user's school Google account profile picture.",
        "operationId": "getUserGoogleAvatar",
        "tags": ["User info"],
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
                "allowEmptyValue": True,
                "description": "Mainly for the demos on this doc page",
                "in": "header",
                "name": "ngrok-skip-browser-warning",
                "required": "false"
            }
        ],
        "responses": {
            "200": {
                "description": "Got the user's profile picture."
            }
        },
        "summary": "Gets the user avatar"
    })
    def get(self):
        sess = self.sm.getSessionByID(int(request.args['id']))
        avatar = sess.getUserGoogleAvatar()

        res = make_response(avatar)
        res.content_type = "image/png"

        return res