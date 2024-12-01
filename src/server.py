from flask import Flask, request
from config import Config
from sessionmanager import SessionManager
from session import Session
from datetime import datetime

class Server(Flask):
    def __init__(self, config: Config):
        super().__init__(__name__)
        self.sm = SessionManager(config)

        self.add_url_rule('/auth', view_func=self.viewLogin, methods=['POST'])
        self.add_url_rule('/user/fullName', view_func=self.getUserFullName)
        self.add_url_rule('/user/class', view_func=self.getUserClass)
        self.add_url_rule('/seminars', view_func=self.getSeminars)
        self.add_url_rule('/programming', view_func=self.getProgrammingAssignments)
    
    def viewLogin(self):
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
        if request.args['id']:
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
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getUserClass(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            user_class = sess.getClass()

            return {
                "class": user_class
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getSeminars(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            seminars = sess.getSeminars()

            return {
                "seminars": seminars
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def getProgrammingAssignments(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            assignments = sess.getProgrammingExcercises(Session.getCurrentSemester(Session.getSchoolYearByTime()))

            return {
                "assignments": assignments
            }
        else:
            return self.returnNonTwoHunderdCode(401)
        
    def returnNonTwoHunderdCode(self, res_code: int) -> tuple[dict, int]:
        match res_code:
            case 400:
                return {
                    "code": "400 Bad Request",
                    "message": "Request parameters malformed",
                    "message_cz": "Parametry žádosti deformovaný",
                    "date": datetime.now()
                }, 400
            
            case 401:
                return {
                    "code": "401 Unauthorized",
                    "message": "Provide a session ID",
                    "message_cz": "Poskytněte ID relace.",
                    "date": datetime.now()
                }, 401
            
            case 403:
                return {
                    "code": "403 Forbidden",
                    "message": "You do not have permission to request this data.",
                    "message_cz": "Nemáte povolen přístup k těmto datům.",
                    "date": datetime.now()
                }, 403
            
            case 405:
                return {
                    "code": "405 Forbidden",
                    "message": "Wrong request method",
                    "message_cz": "Špatná metoda žádosti",
                    "date": datetime.now()
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
                    "date": datetime.now()
                }, 500