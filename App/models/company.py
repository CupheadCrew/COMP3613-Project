from App.database import db
from .user import User

class Company(User):
    company_id = db.Column(db.String, primary_key=True)  
    company_name = db.Column(db.String, unique=True, nullable=False)
    company_address = db.Column(db.String(120))
    contact = db.Column(db.String())
    website = db.Column(db.String(120))

    listings = db.relationship('Listing', backref='company', lazy=True, cascade="all, delete-orphan")
    applications = db.relationship('Application', backref='company', lazy=True, cascade="all, delete-orphan")
    employee_id = db.Column(db.String, db.ForeignKey('employee.id'))


    employee = db.relationship('Employee', backref='company', uselist=False)

    def __init__(self, username, password, email, company_id, company_name, company_address, contact, website,employee_id):
        super().__init__(username, password, email)
        self.company_id = company_id
        self.company_name = company_name
        self.company_address = company_address
        self.contact = contact
        self.website = website
        self.employee_id= employee_id

    def submit(self, listing):
        db.session.add(listing)
        db.session.commit()

    def get_listings(self):
        return [listing.get_json() for listing in self.listings]
    
    def view_notifications(self, notifications):
        return [notification.get_json() for notification in notifications]
    
    def delete_listing(self, listing):
        if listing in self.listings:
            db.session.delete(listing)
            db.session.commit()
        else:
            raise ValueError(f"Listing {listing.title} does not belong to this company.")


    def get_json(self):
        return {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'email': self.email,
            'company_address': self.company_address,
            'contact': self.contact,
            'website': self.website,
            'listings': [listing.get_json() for listing in self.listings]
        }
