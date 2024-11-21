import uuid

from flask import request
from App.database import db
from sqlalchemy import CheckConstraint
from App.models import application

# categories list for possible job categories
categories = [
    'Software Engineer', 'Database Manager', 'Programming', 'Web Design', 'Cyber Security', 
    'Big Data', 'Algorithms', 'N/A']

class Listing(db.Model):
    listing_id = db.Column(db.String, primary_key=True)  # Unique identifier
    title = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(500))
    company_id = db.Column(db.String, db.ForeignKey('company.company_id'), nullable=False)  # Foreign key to Company
    salary = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)
    remote = db.Column(db.Boolean, default=False)
    ttnational = db.Column(db.Boolean, default=False)
    desired_candidate = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(120), nullable=False)
    job_category = db.Column(db.String(180), nullable=False,default='N/A')
    request = db.Column(db.String())


    # requests for deletion?----- Don't take out this comment yet... ~Tamia
    #Done by admin who approves
    approved = db.Column(db.Boolean, default=False)

    # Relationship with applications (1-to-many)
    applications = db.relationship('Application', backref='listing', lazy=True, cascade="all, delete-orphan")

    # Foreign key to the Company table
    company_id = db.Column(db.String, db.ForeignKey('company.company_id'), nullable=False)

    # Relationship with Company (M-1)
    company = db.relationship('Company', back_populates='listing')


    __table_args__ = (
        CheckConstraint(position.in_(['Full-time', 'Part-time', 'Contract', 'Internship', 'Freelance']), name = 'check_position_value'),
        CheckConstraint(request.in_(['Delete', 'Edit', 'None']), name = 'check_request_value'),
    )
    
    def __init__(self, listing_id, title, description, company_id, salary, position, remote, ttnational, desired_candidate, area):
        self.listing_id = listing_id
        self.title = title
        self.description = description
        self.company_id = company_id

        if job_categories is None:
            self.job_category = 'N/A'
        else:
            self.validate_and_set_categories(job_categories)

        self.salary = salary
        self.position = position
        self.remote = remote
        self.ttnational = ttnational
        self.desired_candidate = desired_candidate
        self.area = area
        self.approved = False
        self.request = 'None'

    def get_company(self):
        return self.company

    # methods to support adding, removing, validating the job categories
    def validate_and_set_categories(self, job_categories):
        valid_categories = [category for category in job_categories if category in categories]
        self.job_category = '|'.join(valid_categories)

    def get_categories(self):
        return self.job_category.split('|')

    def get_applicants(self):
        return self.applications

    def add_category(self, category):
        categories = self.get_categories()
        if category not in categories:
            categories.append(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' already exists.")

    def remove_category(self, category):
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' does not exist.")

        
    # Possible Controller could be implemented
    def submit_application(self, alumini_id,date_applied,listing_id):
        new_application = application.Application(
            application_id = str(uuid.uuid4()),
            listing_id = self.listing_id,
            alumini_id = alumini_id,
            date_applied = date_applied,
        )
        
        # Add to the database session
        db.session.add(new_application)
        db.session.commit()

        return {
            "message": "Application submitted successfully.",
            "application_id": new_application.application_id
        }


    def get_json(self):
        return {
            'listing_id': self.listing_id,
            'title': self.title,
            'description': self.description,
            'company_id': self.company_id,
            'salary': self.salary,
            'position': self.position,
            'remote': self.remote,
            'ttnational': self.ttnational,
            'desired_candidate': self.desired_candidate,
            'area': self.area,
            'jobCategories': (self.get_categories),
            'applications': [self.applications.get_json() for application in self.applications],         
}
