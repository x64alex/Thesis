class Constants(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
            cls.instance._constants = {}
        return cls.instance

    def set_constant(self, key, value):
        self._constants[key] = value

    def get_constant(self, key):
        return self._constants.get(key)

constants = Constants()
constants.set_constant("path","./SentimentAnalysis")