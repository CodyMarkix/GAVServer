#!/usr/bin/env python
import json
import shutil
import sys, os
import webbrowser

from config import Config
from server import Server

class Main:
    @staticmethod
    def main():
        if not shutil.which('geckodriver'):
            print("FATAL: Please install geckodriver!")
            webbrowser.open_new_tab("https://pypi.org/project/selenium/#description")
            sys.exit(2)

        try:
            if len(sys.argv) > 1:
                if os.path.isfile(sys.argv[1]):
                        configuration = Config(sys.argv[1])
                        server = Server(configuration)
                        server.run(port=configuration.getPort())
                else:
                    with open(sys.argv[1], 'w') as f:
                        f.write(json.dumps({"server_url": "https://vyuka.gyarab.cz", "login_email": "", "login_pass": ""}, indent=4))
                    print("Config file created! Please fill out your credentials.")
                    sys.exit(0)
            else:
                raise FileNotFoundError()
            
        except FileNotFoundError:
            print("Please specify a configuration file! Bailing out...")
            sys.exit(2)


if __name__ == "__main__":
    Main.main()