from App.database import db
from .user import User


class Admin(User):

    def __init__(self, username, password, email):
        super().__init__(username, password, email)