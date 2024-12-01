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
        sessions_dir = os.path.join(".." if sys.argv[0][-3:] == ".py" else ".", "sessions")

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

                    sm.addSession(manifest['mail'], "[REDACTED]", cookies, local_storage, session_storage)

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

        if len(sys.argv) > 1:
            try:
                if sys.argv[1][-4:] == "json":
                    self.conditions['configFileArgumentGiven'] = True
                    
                    if os.path.isfile(sys.argv[1]):
                        with open(sys.argv[1], 'r') as f:
                            json.loads(f.read())
                        self.conditions['configFilePresent'] = True
                    else:
                        raise Exception()
                        

                else:
                    print("FATAL: Not a json file")
                    sys.exit(2)
            except Exception:
                f.close()
                with open(sys.argv[1], 'w') as new_f:
                    new_f.write(json.dumps({
                            "server_url": "https://vyuka.gyarab.cz",
                            "bind_address": "0.0.0.0",
                            "port": 8080,
                            "firefox_binary": "C:\\Program Files\\Mozilla Firefox\\firefox.exe" if os.name == 'nt' else "/usr/bin/firefox",
                            "headless_mode": True,
                            "time_delay_gyarab": 0.7,
                            "time_delay_google": 2,
                            "time_offset_google": 0.25
                        }, indent=4))
                    print("Config file created! Please check the file to ensure the values are set as you want them.")
                    sys.exit(0)
        else:
            print("FATAL: Please provide a config file")
            sys.exit(2)
            

    def checkConditions(self) -> bool:
        num_of_trues = 0
        for x in self.conditions.values():
            if x:
                num_of_trues += 1
        
        if num_of_trues == len(self.conditions.values()):
            return True
        else:
            return False