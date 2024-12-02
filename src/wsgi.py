from config import Config
from server import Server
from routines.startup import Startup
from routines.shutdown import Shutdown
import os
import signal

# Initialize the application
st = Startup()
st.performStartup()

if st.checkConditions():
    configuration = Config(os.path.join("..", "config.json"))  # Replace with your actual configuration file or logic
    
    app = Server(configuration)

    sh = Shutdown(app.sm)
    signal.signal(signal.SIGINT, sh.performShutdown)
    signal.signal(signal.SIGTERM, sh.performShutdown)
    
    st.resumeSavedSessions(app.sm)
else:
    raise RuntimeError("Failed to meet startup conditions")