from flask import Flask, request, redirect, url_for
from flask_restful import Api
from flasgger import Swagger
import re
from datetime import datetime

from config import Config
from sessionmanager import SessionManager
from session import Session

from routes.api.auth import Auth
from routes.api.user.fullname import FullName
from routes.api.user.userclass import UserClass
from routes.api.seminars import Seminars
from routes.api.programming.sinassign import SingleProgrammingAssignment
from routes.api.programming.mulassign import MultipleProgrammingAssignments
from routes.api.programming.totalgrade import TotalGrade

class Server(Flask):
    def __init__(self, config: Config):
        super().__init__(__name__)
        self.api = Api(self)

        self.app_config = config
        self.sm = SessionManager(config)
        
        self.before_request(self.beforeRequest)

        # Initializing Swagger
        self.swag = Swagger(self, template=config.getSwaggerInfo())
        self.add_url_rule('/', view_func=lambda: redirect(url_for('flasgger.apidocs')))

        self.api.add_resource(Auth, '/api/auth', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(FullName, '/api/user/fullName', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(UserClass, '/api/user/class', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(Seminars, '/api/seminars', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(MultipleProgrammingAssignments, '/api/programming', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(SingleProgrammingAssignment, '/api/programming/<name>', resource_class_kwargs={"session_manager": self.sm})
        self.api.add_resource(TotalGrade, '/api/programming/totalGrade', resource_class_kwargs={"session_manager": self.sm})

    def beforeRequest(self):
        if request.path == "/api/auth":
            if not all(["email" in request.args.keys(), "password" in request.args.keys()]):
                return self.returnNonTwoHunderdCode(400)
        
        elif "/flasgger_static/" in request.path:
            print("Accessing API docs")
        
        elif "/apidocs" in request.path:
            print("Accessing API docs")

        elif "/" in request.path:
            print("Accessing API docs")

        else:
            if "id" in request.args.keys():
                if not self.sm.getSessionByID(int(request.args['id'])):
                    return self.returnNonTwoHunderdCode(401)
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