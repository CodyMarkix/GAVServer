import shutil
import webbrowser
import sys, os
import json
import pickle

class Startup:
    conditions = {
        "installedGeckoDriver": False,
        "configFileArgumentGiven": False,
        "configFilePresent": False
    }

    def __init__(self):
        pass

    def resumeSavedSessions(self, sm):
        sessions_dir = os.path.join("..", "sessions")

        if os.path.exists(sessions_dir):
            if len(os.listdir(sessions_dir)) > 0:
                for dir in os.listdir(sessions_dir):
                    os.chdir(os.path.join(sessions_dir, dir))
                    
                    with open((os.path.join(".", 'cookies.pkl')), 'rb') as cookie_file:
                        cookies = pickle.loads(cookie_file.read())
                    
                    with open(os.path.join(".", 'local_storage.json'), 'r') as ls_file:
                        local_storage = json.loads(ls_file.read())

                    with open(os.path.join(".", 'session_storage.json'), 'r') as sst_file:
                        session_storage = json.loads(sst_file.read())
                    
                    with open(os.path.join(".", 'MANIFEST.json'), 'r') as manifest_file:
                        manifest = json.loads(manifest_file.read())

                    sm.addSession(manifest['mail'], "[REDACTED]", cookies, local_storage, session_storage, manifest['id'])

                    os.chdir("..")
            else:
                return

    def performStartup(self):
        if shutil.which('geckodriver'):
            self.conditions['installedGeckoDriver'] = True
            
        else:
            print("FATAL: Please install geckodriver!")
            webbrowser.open_new_tab("https://pypi.org/project/selenium/#description")
            sys.exit(2)

        try:
            with open(os.path.join("..", "config.json"), 'r') as f:
                json.loads(f.read())
                self.conditions['configFileArgumentGiven'] = True  
                self.conditions['configFilePresent'] = True
        except Exception:
            f.close()
            with open(os.path.join("..", "config.json"), 'w') as new_f:
                new_f.write(json.dumps({
                    "server_url": "https://vyuka.gyarab.cz",
                    "bind_address": "127.0.0.1",
                    "port": 8054,
                    "firefox_binary": "C:\\Program Files\\Mozilla Firefox\\firefox.exe" if os.name == 'nt' else "/usr/bin/firefox",
                    "headless_mode": True,
                    "time_delay_gyarab": 0.7,
                    "time_delay_google": 2,
                    "time_offset_google": 0.25,
                    "swagger_info": {
                        "swagger": "2.0",
                        "info": {
                            "title": "GAV Server",
                            "description": "API for https://vyuka.gyarab.cz",
                            "contact": {
                                "name": "Your contact",
                                "url": "https://your.contact.com"
                            },
                            "license": {
                                "name": "GNU GPLv3",
                                "url": "https://www.gnu.org/licenses/gpl-3.0.en.html"
                            },
                            "version": "v1"
                        },
                        "host": "127.0.0.1",
                        "basePath": "/",
                        "schemes": ["http", "https"],
                        "produces": ["application/json"]
                    },
                    "swagger_config": {
                        "headers": [
                        ],
                        "specs": [
                            {
                                "endpoint": "apispec_1",
                                "route": "/apispec_1.json",
                                "rule_filter": True,
                                "model_filter": True
                            }
                        ],
                        "specs_route": "/",
                        "ui_params": {
                            "supportedSubmitMethods": []
                        }
                    }
                }, indent=4))
                print("Config file created! Please check the file to ensure the values are set as you want them.")
                sys.exit(0)
        

    def checkConditions(self) -> bool:
        num_of_trues = 0
        for x in self.conditions.values():
            if x:
                num_of_trues += 1
        
        if num_of_trues == len(self.conditions.values()):
            return True
        else:
            return False