from App.database import db
from .user import User

class Alumni(User):
    alumni_id = db.Column(db.Integer, nullable = False, unique = True)
    contact = db.Column(db.String(30), nullable = False)
    firstname = db.Column(db.String(120), nullable = False)
    lastname = db.Column(db.String(120), nullable = False)
    job_category = db.Column(db.String(120))



    # Define relationship to listings
    listing = db.relationship('Listing', secondary='alumni_listings', back_populates='applicant')
    listingsApplied = listing.Listing()



    # relationship to listings to receive notifications?
    subscribed = db.Column(db.Boolean, default=False)


    # need to add in columns for:
    # -contact info i.e phone number
    contact = db.Column(db.String(30), nullable = False)

    #name
    firstname = db.Column(db.String(120), nullable = False)
    lastname = db.Column(db.String(120), nullable = False)

    # Skills
    skills = db.Column(db.String(1200), nullable = False)

    # Experience
    experience = db.Column(db.String(1200), nullable = False)

    # Nationality
    nationality = db.Column(db.String(120), nullable = False)



    # relationship with files?
    # files = db.relationship('File', back_populates='alumni', lazy=True)

    # categories = ['Software Engineering', 'Database', 'Programming', 'N/A']
    categories = []
    for i in categories:
        categories[i] = listing.categories[i]

    
    job_category = db.Column(db.String(120))


    def __init__(self, username, password, email, alumni_id, contact, firstname, lastname):
        super().__init__(username, password, email)
        self.alumni_id = alumni_id
        self.job_category = None
        self.subscribed = False
        self.contact = contact
        self.firstname = firstname
        self.lastname = lastname


    def get_categories(self):
        return self.job_category.split('|') if self.job_category else []

    def add_category(self, category):
        self.job_category = category

    def remove_category(self, category):
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' does not exist.")

    def get_alumni_id(self):
        return self.alumni_id

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'alumni_id': self.alumni_id,
            'subscribed': self.subscribed,
            'job_category': self.job_category,
            'contact':self.contact,
            'firstname':self.firstname,
            'lastname':self.lastname
        }