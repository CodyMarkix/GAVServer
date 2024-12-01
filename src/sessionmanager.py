import math
from session import Session
from config import Config
import random
from datetime import datetime
import time

class SessionManager:
    # Funny little note here:
    # When initially sketching out this project,
    # I thought I would store the sessions in a sqlite database.
    # Maybe it was me being sick but I had no idea what made me think this stupidly 💀🙏
    __sessionList = []

    def __init__(self, config: Config) -> None:
        self.config = config

    def addSession(self, mail: str, password: str, cookies: None|dict=None, local_storage: None|dict=None, session_storage: None|dict=None, existing_id: None|int = None):
        if existing_id == None:
            id = random.randint(1000, 2147483647)
        else:
            id = existing_id

        self.__sessionList.append({f"{id}": Session(self.config, mail, password, id, cookies, local_storage, session_storage)})

        return id, 16
    
    def getAllSessions(self) -> list[dict[str, Session]]:
        return self.__sessionList
    
    def getSessionByID(self, id: int) -> Session | None:
        # Sort sessions
        current_sessions = self.__sessionList
        current_sessions_sorted: list[dict[str, Session]] = sorted(current_sessions, key=lambda d: next(iter(d.keys())))

        # Binary search
        low = 0
        high = len(current_sessions_sorted) - 1
        
        while low <= high:
            mid = math.floor((low + high) / 2)

            if int(list(current_sessions_sorted[mid].keys())[0]) == id:
                return current_sessions_sorted[mid][f'{id}']
            
            elif int(list(current_sessions_sorted[mid].keys())[0]) < id:
                low = mid + 1
                continue

            else:
                high = mid - 1
        
        return None

        

