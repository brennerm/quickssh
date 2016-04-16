class QuickSSHEntry:
    def __init__(self, hostname, username=None, port=22):
        self.__hostname = hostname
        self.__username = username
        self.__port = port or 22

    def __str__(self):
        return str(self.__username) + '@' + self.__hostname + ':' + str(self.__port)

    def get_connection_string(self, default_user):
        return self.get_user(default_user) + '@' + self.__hostname + ':' + str(self.__port)

    @property
    def hostname(self):
        return self.__hostname

    @property
    def username(self):
        return self.__username

    def get_user(self, default_user):
        return self.__username or default_user

    @property
    def port(self):
        return self.__port

    def to_dict(self):
        return {
            'hostname': self.__hostname,
            'username': self.__username,
            'port': self.__port
        }