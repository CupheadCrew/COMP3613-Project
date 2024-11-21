from App.database import db

class Application (db.Model):
    application_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    date_applied = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign Key to Alumni
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    
    # Relationship to Alumni and Listing needed 

    def __init__(self, date_applied, alumni_id, listing_id):
        self.date_applied = date_applied
        self.alumni_id = alumni_id
        self.listing_id = listing_id