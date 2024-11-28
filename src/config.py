import json

class Config():
    def __init__(self, configPath):
        with open(configPath, 'r') as f:
            self.__data = json.loads(f.read())
        
    def getServerURL(self) -> str:
        return self.__data['server_url']
    
    def getUserCredentials(self) -> tuple[str, str]:
        name: str = self.__data['login_email']
        upass: str = self.__data['login_password']
        return (name, upass)
    
    def getPort(self) -> int:
        return self.__data['port']