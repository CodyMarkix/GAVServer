from flask import Flask, request, redirect, url_for
from flasgger import Swagger
from config import Config
from sessionmanager import SessionManager
from session import Session
from datetime import datetime
import re

class Server(Flask):
    def __init__(self, config: Config):
        super().__init__(__name__)
        self.app_config = config
        self.sm = SessionManager(config)
        
        # self.before_request(self.beforeRequest)

        # Initializing Swagger
        self.swag = Swagger(self, template=config.getSwaggerInfo())
        self.add_url_rule('/', view_func=lambda: redirect(url_for('flasgger.apidocs')))

        self.add_url_rule('/api/auth', view_func=self.viewLogin, methods=['POST'])
        self.add_url_rule('/api/user/fullName', view_func=self.getUserFullName)
        self.add_url_rule('/api/user/class', view_func=self.getUserClass)
        self.add_url_rule('/api/seminars', view_func=self.getSeminars)
        self.add_url_rule('/api/programming', view_func=self.getProgrammingAssignments)
        self.add_url_rule('/api/programming/<name>', view_func=self.getProgrammingAssignment)
        self.add_url_rule('/api/programming/totalGrade', view_func=self.getProgrammingTotalGrade)

    def beforeRequest(self):
        if re.match(r"/api/(?!auth|docs|flasgger_static).*", request.path): # https://regex101.com/r/kErJo7/1
            if "id" in request.args.keys():
                if not self.sm.getSessionByID(request.args['id']):
                    return self.returnNonTwoHunderdCode(401)
            else:
                return self.returnNonTwoHunderdCode(401)
        else:
            if not all(["email" in request.args.keys(), "password" in request.args.keys()]):
                return self.returnNonTwoHunderdCode(400)
            

    
    def viewLogin(self):
        """
        Authentication to the API.

        ---
        tags:
          - Authentication
        description: Logs into Gyarab Výuka and returns an ID for the session. Done via e-mail and password. This route is most likely going to be remade or deprecated.
        operationId: login
        parameters:
          - name: E-mail
            in: query
            description: Authenticatee's e-mail
            required: true
            type: string
            allowEmptyValue: false
          - name: Password
            in: query
            description: Authenticatee's password
            required: true
            type: string
            allowEmptyValue: false
          - name: ngrok-skip-browser-warning
            in: header
            description: Mainly for the demos on this doc page
            required: false
            allowEmptyValue: true
        responses:
          200:
            description: Succesfully authenticated and the API has returned a session ID. Expires after a week.
        """
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
            return self.returnNonTwoHunderdCode(405)

    def getUserFullName(self):
        """
        Get the user's full name

        ---
        tags:
          - User info
        description: Returns the full name including any middle names
        operationId: getUserFullName
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
            description: Returned full name.
        """
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

    def getUserClass(self):
        """
        Gets user's class.

        ---
        tags:
          - User info
        description: Gets the user's current class, including the branch. (A, B, C, D, E, F)
        operationId: getUserClass
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
            description: Returned class
        """
        if 'id' in request.args.keys():
            sess = self.sm.getSessionByID(int(request.args['id']))
            user_class = sess.getClass()

            return {
                "class": user_class
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getSeminars(self):
        """
        Gets all seminars
        
        ---
        tags:
          - Seminars
        description: Returns all seminars, if the user is enrolled in any. Returns empty object otherwise
        operationId: getSeminars
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
            description: Returns seminars
        """
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            seminars = sess.getSeminars()

            return {
                "seminars": seminars
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getProgrammingAssignments(self):
        """
        Gets all programming assignments

        ---
        tags:
          - Programming
        description: If the user is enrolled in the programming branch (E, F), returns all programming assignments the user has ever recieved.
        operationId: getProgrammingAssignments
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
            description: Returned assignments in programming classes
        """
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            assignments = sess.getProgrammingAssignments(Session.getCurrentSemester(Session.getSchoolYearByTime()))

            return {
                "assignments": assignments
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getProgrammingAssignment(self, name: str):
        """
        Gets a single programming assignment

        ---
        tags:
          - Programming
        description: Returns a single programming assignment, searched based on the name. (Excludes type)
        operationId: getProgrammingAssignment
        parameters:
          - name: id
            in: query
            description: Session ID
            required: true
            type: integer
            allowEmptyValue: false
          - name: Assignment name
            in: path
            description: Name of the assignment you're fetching
            required: true
            type: string
            allowEmptyValue: false
          - name: ngrok-skip-browser-warning
            in: header
            description: Mainly for the demos on this doc page
            required: false
            allowEmptyValue: true
        responses:
          200:
            description: Returned a programming assignment
        """
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            assignment = sess.getProgrammingAssignment(name)
            
            return {
                "assignment": assignment
            }
        else:
            return self.returnNonTwoHunderdCode(401)
    
    def getProgrammingTotalGrade(self):
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
            total_grade = sess.getProgrammingTotalGrade(Session.getCurrentSemester(Session.getSchoolYearByTime()))

            return total_grade
        else:
            return self.returnNonTwoHunderdCode(401)

    def returnNonTwoHunderdCode(self, res_code: int) -> tuple[dict, int]:
        match res_code:
            case 400:
                return {
                    "code": "400 Bad Request",
                    "message": "Request parameters malformed",
                    "message_cz": "Parametry žádosti deformovaný",
                    "date": datetime.now().isoformat()
                }, 400
            
            case 401:
                return {
                    "code": "401 Unauthorized",
                    "message": "Provide a valid session ID",
                    "message_cz": "Poskytněte validní ID relace.",
                    "date": datetime.now().isoformat()
                }, 401
            
            case 403:
                return {
                    "code": "403 Forbidden",
                    "message": "You do not have permission to request this data.",
                    "message_cz": "Nemáte povolen přístup k těmto datům.",
                    "date": datetime.now().isoformat()
                }, 403
            
            case 405:
                return {
                    "code": "405 Forbidden",
                    "message": "Wrong request method",
                    "message_cz": "Špatná metoda žádosti",
                    "date": datetime.now().isoformat()
                }
            
            case 500:
                return {
                    "code": "500 Internal server error",
                    "message": "Please report this issue with the date of the incident to one of these platforms.",
                    "message_cz": "Prosím nahlašte tuto chybu s datem chyby na jedno z těchto míst.",
                    "contact_methods": [
                        {"github": "https://github.com/CodyMarkix/GAVServer/issues"},
                        {"e-mail": "marek.plasek.s@gyarab.cz"}
                    ],
                    "date": datetime.now().isoformat()
                }, 500