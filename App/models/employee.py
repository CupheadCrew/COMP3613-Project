from App.database import db
from .user import User

class Employee(User):
    employee_id = db.Column(db.Integer, unique=True, nullable=False)

    first_name = db.Column(db.String(120), nullable=True)

    last_name = db.Column(db.String(120), nullable=True)

    department = db.Column(db.String(120), nullable=True)

def __init__(self,username, password, email, employee_id, first_name, last_name, department):
        super().__init__(username, password, email)
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        # self.subscribed = subscribed

def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'employeeid': self.employee_id,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'department': self.department
        #     'subscribed': self.subscribed
            
        }
    


def get_eployee_id(self):
        return self.employee_id

