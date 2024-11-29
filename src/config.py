import json

class Config():
    def __init__(self, configPath):
        with open(configPath, 'r') as f:
            self.__data = json.loads(f.read())
        
    def getServerURL(self) -> str:
        return self.__data['server_url']
    
    def getIPPort(self) -> tuple[str, int]:
        return self.__data['bind_address'], self.__data['port']
    
    def getFirefoxBinary(self) -> str:
        return self.__data['firefox_binary']
    
    def getDelays(self) -> tuple[int, int, float]:
        return self.__data['time_delay_gyarab'], self.__data['time_delay_google'], self.__data['time_offset_google']