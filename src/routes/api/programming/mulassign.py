from flask import request
from flask_restful import Resource
from flasgger import swag_from

class MultipleProgrammingAssignments(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']

    @swag_from({
        "description": "Gets all the programming assignments from this school quarter.",
        "operationId": "getProgrammingAssignments",
        "tags": ["Programming"],
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
            "description": "Returned assignments in programming classes"
          }
        },
        "summary": "Gets all programming assignments"
    })
    def get(self):
        sess = self.sm.getSessionByID(int(request.args['id']))
        assignments = sess.getProgrammingAssignments(sess.getCurrentSemester(sess.getSchoolYearByTime()))

        return {
            "assignments": assignments
        }