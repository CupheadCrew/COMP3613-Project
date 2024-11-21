from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .user import User

class Employee(User):
    employee_id = db.Column(db.String, unique=True, nullable=False)

    employee_name = db.Column(db.String(120), nullable=False)

    employee_password = db.Column(db.String(120), nullable=False)


def __init__(self, employee_id, employee_name, employee_password):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.set_password(employee_password)

def get_json(self):
        return{
            'id': self.employee_id,
            'name': self.employee_name,
            
        }
    
def get_name(self):
        return self.employee_name

def set_password(self, password):
        """Create hashed password."""
        self.employee_password = generate_password_hash(password, method='sha256')
    
def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.employee_password, password)
