from __main__ import db


class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    givenName = db.Column(db.String(120), nullable=False)
    familyName = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(120), nullable=False)
    isMentor = db.Column(db.Boolean, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    ethnicity = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mainPersonalIdType = db.Column(db.String(120), nullable=False)
    mainPersonalId = db.Column(db.String(120), nullable=False)
    dateOfRegistration = db.Column(db.String(120), nullable=False)
    reasonOfRegistration = db.Column(db.String(120), nullable=False)
    previousStatus = db.Column(db.String(120), nullable=False)
    dateOfLeave = db.Column(db.String(120), nullable=False)
    reasonOfLeave = db.Column(db.String(120), nullable=False)
    destinationOfLeave = db.Column(db.String(120), nullable=False)
    mentorship = db.Column(db.String(5000), nullable=False)
    salaryCard = db.Column(db.String(120), nullable=False)
    custodianInfo = db.Column(db.String(5000), nullable=False)
    emergentContact = db.Column(db.String(5000), nullable=False)
    contactInfo = db.Column(db.String(5000), nullable=False)
    medicalInfo = db.Column(db.String(5000), nullable=False)
    notes = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return '<User %r %r >' % (self.familyName, self.givenName)