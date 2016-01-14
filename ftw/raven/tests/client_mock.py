from ftw.raven import client


class ClientMock(object):

    def __init__(self, dsn=None, raise_send_errors=False, transport=None,
                 install_sys_hook=True, **options):
        self.dsn = dsn
        self.captureException_calls = []

    def captureException(self, exc_info=None, **kwargs):
        kwargs.update({'exc_info': exc_info})
        self.captureException_calls.append(kwargs)

    @classmethod
    def install(klass):
        client.raven_client_class = klass


class CrashingClientMock(ClientMock):

    def __init__(self, *args, **kwargs):
        super(CrashingClientMock, self).__init__(*args, **kwargs)
        self.crashes = 0

    def captureException(self, exc_info=None, **kwargs):
        self.crashes += 1
        raise Exception('Not going to happen.')
