class Properties(object):
    __instance = None
    __properties = None

    def __init__(self, yaml = None):
        if Properties.__instance is None:
            Properties.__instance = self
            if Properties.__properties == None and yaml is not None:
                Properties.__properties = yaml

    @property
    def host(self):
        return self.__properties['host']

    @property
    def username(self):
        return self.__properties['username']
    
    @property
    def password(self):
        return self.__properties['password']

    @property
    def schema(self):
        return self.__properties['schema']

    @property
    def table(self):
        return self.__properties['table']
