from flask import Flask, request
from config import Config
from sessionmanager import SessionManager
from datetime import datetime

class Server(Flask):
    def __init__(self, config: Config):
        super().__init__(__name__)
        self.sm = SessionManager(config)

        self.add_url_rule('/auth', view_func=self.viewLogin)
        self.add_url_rule('/fullName', view_func=self.getUserFullName)
        self.add_url_rule('/seminars', view_func=self.getSeminars)

    def viewLogin(self):
        args = request.args
        sess = self.sm.addSession(args['email'], args['password'])

        return {
            "message": "Authenticated successfuly!",
            "sessionID": sess[0],
            "timeToWait": sess[1]
        }

    def getUserFullName(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            name = sess.getUserFullName()
            print(name, len(name))
            
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
            return {
                "code": "401 Unauthorized",
                "message": "Provide a session ID",
                "date": datetime.date(datetime.now()).isoformat() + "_" + datetime.time(datetime.now()).isoformat()
            }, 401
        
    def getSeminars(self):
        if request.args['id']:
            sess = self.sm.getSessionByID(int(request.args['id']))
            seminars = sess.getSeminars()

            return {
                "seminars": seminars
            }
        else:
            return {
                "code": "401 Unauthorized",
                "message": "Provide a session ID",
                "date": datetime.date(datetime.now()).isoformat() + "_" + datetime.time(datetime.now()).isoformat()
            }, 401