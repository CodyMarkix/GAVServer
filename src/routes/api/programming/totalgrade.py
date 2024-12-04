from flask import request
from flask_restful import Resource
from flasgger import swag_from

class TotalGrade(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']
    
    @swag_from({
        "description": "Gets the total grade for programming. Includes total points, average percentage and grade.",
        "operationId": "getProgrammingTotalGrade",
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
                "allowEmptyValue": True,
                "description": "Mainly for the demos on this doc page",
                "in": "header",
                "name": "ngrok-skip-browser-warning",
                "required": "false"
            }
        ],
        "responses": {
            "200": {
                "description": "Got the total grade for programming."
            }
        },
        "summary": "Gets the total grade"
    })
    def get(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            total_grade = sess.getProgrammingTotalGrade(sess.getCurrentSemester(sess.getSchoolYearByTime()))

            return total_grade
        else:
            return self.returnNonTwoHunderdCode(401)