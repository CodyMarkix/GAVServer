import json

class Config():
    def __init__(self, configPath):
        self.configPath = configPath
        
        with open(configPath, 'r') as f:
            self.__data = json.loads(f.read())
        
    def getServerURL(self) -> str:
        """
        OPTION: URL for Gyarab Výuka, https://vyuka.gyarab.cz by default
        """
        return self.__data['server_url']
    
    def getIPPort(self) -> tuple[str, int]:
        """
        OPTION: IP address to bind the web server to + the port
        """
        return self.__data['bind_address'], self.__data['port']
    
    def getFirefoxBinary(self) -> str:
        """
        OPTION: Location where Firefox is installed
        """
        return self.__data['firefox_binary']
    
    def getHeadlessMode(self) -> bool:
        """
        OPTION: Should Firefox be set to headless mode or not? Heavily reccomended to set to `true` on servers
        """
        return self.__data['headless_mode']
    
    def getDelays(self) -> tuple[int, int, float]:
        """
        OPTION: Delays for the webdriver between actions
        """
        return self.__data['time_delay_gyarab'], self.__data['time_delay_google'], self.__data['time_offset_google']