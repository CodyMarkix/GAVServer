#!/usr/bin/env python
import signal
import sys

from config import Config
from server import Server
from routines.startup import Startup
from routines.shutdown import Shutdown

class Main:
    @staticmethod
    def main():
        st = Startup()
        st.performStartup()

        if st.checkConditions():
            configuration = Config(sys.argv[1])
            server = Server(configuration)
            sh = Shutdown(server.sm)
            signal.signal(signal.SIGINT, sh.performShutdown)
            signal.signal(signal.SIGTERM, sh.performShutdown)

            st.resumeSavedSessions(server.sm)
            try:
                if __name__ == "__main__":
                    server.run(port=configuration.getIPPort()[1], host=configuration.getIPPort()[0])
            except KeyboardInterrupt:
                sh.performShutdown() # try/except works as a fallback
                sys.exit(1)
        else:
            print("FATAL: Unhandled exception, bailing out!")
            sys.exit(127)

Main.main()
