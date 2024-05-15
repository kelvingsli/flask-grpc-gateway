class LoginUserDto():
    id = None
    email = ''
    first_name = ''
    last_name = ''

    def __init__(self, id, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

class CreateUserReqDto():
    email = ''
    first_name = ''
    last_name = ''
    password = ''

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class UserDto():
    id = None
    email = ''
    first_name = ''
    last_name = ''

    def __init__(self, id, email, first_name, last_name):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name