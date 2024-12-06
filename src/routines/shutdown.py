import sys
import os
import pickle, json
from datetime import datetime
from seleniumrequests import Firefox
from deprecated import deprecated


class Shutdown:
    def __init__(self, sm):
        self.sm = sm

    @deprecated(reason="Saving browser sessions is probably the biggest security hole one could've introduced into this project. Use performShutdownSafe instead.")
    def performShutdown(self, signum, frame):
        print("Shutting down...")

        session_list = self.sm.getAllSessions()
        for entry in session_list:
            for session in entry.values():
                browser: Firefox = session.browser
                os.chdir("..")

                if not os.path.isdir(os.path.join(".", "sessions")):
                    os.mkdir("sessions")

                os.chdir(os.path.join(".", "sessions"))

                if not os.path.isdir(os.path.join(".", f"{session.id}")):
                    os.mkdir(f"{session.id}")
                
                os.chdir(f"{session.id}")

                with open("cookies.pkl", "wb") as cookies:
                    pickle.dump(browser.get_cookies(), cookies)

                local_storage = browser.execute_script("return window.localStorage;")
                with open("local_storage.json", "w") as localStorage:
                    localStorage.write(json.dumps(local_storage))

                session_storage = browser.execute_script("return window.sessionStorage;")
                with open("session_storage.json", "w") as sessionStorage:
                    sessionStorage.write(json.dumps(session_storage))

                with open("MANIFEST.json", "w") as manifest:
                    manifest.write(json.dumps({
                        "id": session.id,
                        "mail": session.mail,
                        "date_of_suspension": datetime.now().isoformat(),
                        "browser": {
                            "config_path": session.config.configPath,
                            "current_url": browser.current_url,
                            "options": {
                                "binary_location": session.browser_options.binary_location
                            }
                        }
                    }, indent=4))

                browser.quit()

        sys.exit(0)

    def performShutdownSafe(self, signum, frame):
        print("Shutting down...")
        sys.exit(0)