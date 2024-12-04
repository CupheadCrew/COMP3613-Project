from App.database import db
from sqlalchemy import CheckConstraint

# categories list for possible job categories
categories = [
    'Software Engineer', 'Database Manager', 'Programming', 'Web Design', 'Cyber Security', 
    'Big Data', 'Algorithms', 'N/A']

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False, unique=True)
    description = db.Column(db.String(500))
    job_category = db.Column(db.String(120))
    salary = db.Column(db.Integer(), nullable=False)
    position = db.Column(db.String(), nullable=False)
    remote = db.Column(db.Boolean, default=False)
    ttnational = db.Column(db.Boolean, default=False)
    desiredcandidate = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(120), nullable=False)
    seen = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)
    #attributes to help with checking approval

    
    
    # requests for deletion?----- Don't take out this comment yet... ~Tamia
    request = db.Column(db.String())

    # set up relationship with Company (M-1)
    company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    companies = db.relationship('Company', back_populates='listings', overlaps="company")

    # Define relationship to applications..... ~Tamia
    #[-----------HERE----------]
    

    __table_args__ = (
        CheckConstraint(position.in_(['Full-time', 'Part-time', 'Contract', 'Internship', 'Freelance']), name = 'check_position_value'),
        CheckConstraint(request.in_(['Delete', 'Edit', 'None']), name = 'check_request_value'),
    )

    

    def toggle(self):
        self.approved = not self.approved
        db.session.add(self)
        db.session.commit()

    def __init__(self, title, description, company_name, job_categories, salary,
                position, remote, ttnational, desiredcandidate, area, seen, approved):
        self.title = title
        self.description = description
        self.company_name = company_name

        if job_categories is None:
            self.job_category = 'N/A'
        else:
            self.validate_and_set_categories(job_categories)

        self.salary = salary
        self.position = position
        self.remote = remote
        self.ttnational = ttnational
        self.desiredcandidate = desiredcandidate
        self.area = area
        self.seen = seen
        self.approved = approved

        self.request = 'None'

    def get_company(self):
        return self.company_name

    # methods to support adding, removing, validating the job categories
    def validate_and_set_categories(self, job_categories):
        valid_categories = [category for category in job_categories if category in categories]
        self.job_category = '|'.join(valid_categories)

    def get_categories(self):
        return self.job_category.split('|') if self.job_category else []

    def get_applicants(self):
        return self.applicant

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

    def get_json(self):
        return{
            'id': self.id,
            'title':self.title,
            'description':self.description,
            'company_name':self.company_name,
            'job_category':self.get_categories(),
            'salary':self.salary,
            'position':self.position,
            'remote':self.remote,
            'ttnational':self.ttnational,
            'desiredcandidate':self.desiredcandidate,
            'area':self.area,
            'seen':self.seen,
            'approved':self.approved
        }