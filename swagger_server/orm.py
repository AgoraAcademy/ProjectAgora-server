from sqlalchemy import create_engine, Column, DateTime, String, Integer, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Learner_db(Base):
    __tablename__ = 'learner'
    id = Column(Integer, primary_key=True)
    givenName = Column(String(120), nullable=False)
    familyName = Column(String(120), nullable=False)
    nickname = Column(String(120), nullable=False)
    isMentor = Column(Boolean, nullable=False)
    gender = Column(String(120), nullable=False)
    ethnicity = Column(String(120), nullable=False)
    birthday = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    mainPersonalIdType = Column(String(120), nullable=False)
    mainPersonalId = Column(String(120), nullable=False)
    dateOfRegistration = Column(String(120), nullable=False)
    reasonOfRegistration = Column(String(120), nullable=False)
    previousStatus = Column(String(120), nullable=False)
    dateOfLeave = Column(String(120), nullable=False)
    reasonOfLeave = Column(String(120), nullable=False)
    destinationOfLeave = Column(String(120), nullable=False)
    mentorship = Column(String(5000), nullable=False)
    salaryCard = Column(String(120), nullable=False)
    custodianInfo = Column(String(5000), nullable=False)
    emergentContact = Column(String(5000), nullable=False)
    contactInfo = Column(String(5000), nullable=False)
    medicalInfo = Column(String(5000), nullable=False)
    notes = Column(String(5000), nullable=False)

    def __repr__(self):
        return '<Learner %r %r >' % (self.familyName, self.givenName)


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
