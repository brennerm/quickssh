import uuid


class QuickSSHEntry:
    def __init__(self, hostname, username=None, port=None):
        self.__id = str(uuid.uuid4())
        self.__hostname = hostname
        self.__username = username or None
        self.__port = port or None

    def __str__(self):
        return str(self.__username) + '@' + self.__hostname + ':' + str(self.__port)

    def __eq__(self, other):
        if not isinstance(other, QuickSSHEntry):
            return False

        if self.__id != other.id:
            return False
        return True

    def get_connection_string(self, default_user):
        return self.get_user(default_user) + '@' + self.__hostname + ':' + (self.port or '22')

    @property
    def id(self):
        return self.__id

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, value):
        self.__hostname = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value or None

    def get_user(self, default_user):
        return self.__username or default_user

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value or None

    def to_dict(self):
        return {
            'hostname': self.__hostname,
            'username': self.__username,
            'port': self.__port
        }