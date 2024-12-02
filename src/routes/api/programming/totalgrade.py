from flask import request
from flask_restful import Resource
from flasgger import swag_from

class TotalGrade(Resource):
    def __init__(self, **kwargs):
        self.sm = kwargs['session_manager']
    
    def get(self):
        """
        Gets the total grade

        ---
        tags:
          - Programming
        description: Gets the total grade for programming. Includes total points, average percentage and grade.
        operationId: getProgrammingTotalGrade
        parameters:
          - name: id
            in: query
            description: Session ID
            required: true
            type: integer
            allowEmptyValue: false
          - name: ngrok-skip-browser-warning
            in: header
            description: Mainly for the demos on this doc page
            required: false
            allowEmptyValue: true
        responses:
          200:
            description: Got the total grade for programming.
        """
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            total_grade = sess.getProgrammingTotalGrade(sess.getCurrentSemester(sess.getSchoolYearByTime()))

            return total_grade
        else:
            return self.returnNonTwoHunderdCode(401)