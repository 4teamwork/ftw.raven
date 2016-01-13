

class ClientMock(object):

    def __init__(self, dsn):
        self.dsn = dsn
        self.captureException_calls = []

    def captureException(self, exc_info=None, **kwargs):
        kwargs.update({'exc_info': exc_info})
        self.captureException_calls.append(kwargs)
