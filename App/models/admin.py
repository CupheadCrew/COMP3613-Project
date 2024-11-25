from App.database import db
from .user import User


class Admin(User):
    # id = db.Column(db.Integer, primary_key = True)
    adminID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    adminPassword = db.Column(db.String, db.ForeignKey('user.password'), primary_key=True)


  #   __mapper_args__ = {
  #     'polymorphic_identity': 'admin',
  # }

    def __init__(self, username, password, email):
        super().__init__(username, password, email)