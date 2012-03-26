class Bus():
    _collection = 'bus'

    def __init__(self, code=None, no=None, route=None):
        self.code = code
        self.no = no
        self.route = route

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__
