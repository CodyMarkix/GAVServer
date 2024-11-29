import json

class Config():
    def __init__(self, configPath):
        with open(configPath, 'r') as f:
            self.__data = json.loads(f.read())
        
    def getServerURL(self) -> str:
        return self.__data['server_url']
    
    def getPort(self) -> int:
        return self.__data['port']
    
    def getFirefoxBinary(self) -> str:
        return self.__data['firefox_binary']