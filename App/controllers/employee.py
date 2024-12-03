from App.models import User, Alumni, Admin, Employee
from App.database import db


def add_employee(username, password, email, employee_id, first_name, last_name, department):

        # Check if there are no other users with the same username or email values in any other subclass
        if (
            Alumni.query.filter_by(username=username).first() is not None or
            Admin.query.filter_by(username=username).first() is not None or
            #Company.query.filter_by(username=username).first() is not None or

            #Company.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None or
            Alumni.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newEmployee = Employee(username, password, email, employee_id, first_name, last_name, department)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newEmployee)
            db.session.commit()  # Commit to save the new  to the database
            return newEmployee
        except:
            db.session.rollback()
            return None

def get_all_employees():
    return db.session.query(Employee).all()

def get_all_employees_json():
    employees = get_all_employees()
    if not employees:
        return []
    employees = [employee.get_json() for employee in employees]
    return employees

def get_employee(employee_id):
    return Employee.query.filter_by(employee_id=employee_id).first()

