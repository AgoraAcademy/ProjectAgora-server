from sqlalchemy import create_engine, Column, DateTime, String, Integer, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Learner_db(Base):
    __tablename__ = 'learner'
    id = Column(Integer, primary_key=True)
    openid = Column(String(120), nullable=False)
    validated = Column(Boolean, nullable=False)
    givenName = Column(String(120), nullable=False)
    familyName = Column(String(120), nullable=False)
    nickname = Column(String(120), nullable=True)
    isMentor = Column(Boolean, nullable=True)
    gender = Column(String(120), nullable=False)
    ethnicity = Column(String(120), nullable=False)
    birthday = Column(String(120), nullable=False)
    mainPersonalIdType = Column(String(120), nullable=False)
    mainPersonalId = Column(String(120), nullable=False)
    dateOfRegistration = Column(String(120), nullable=False)
    reasonOfRegistration = Column(String(120), nullable=False)
    previousStatus = Column(String(120), nullable=False)
    dateOfLeave = Column(String(120), nullable=True)
    reasonOfLeave = Column(String(120), nullable=True)
    destinationOfLeave = Column(String(120), nullable=True)
    mentorship = Column(String(1000), nullable=True)
    salaryCard = Column(String(120), nullable=True)
    custodianInfo = Column(String(1000), nullable=True)
    emergentContact = Column(String(1000), nullable=False)
    contactInfo = Column(String(1000), nullable=False)
    medicalInfo = Column(String(1000), nullable=False)
    notes = Column(String(2000), nullable=True)

    def __repr__(self):
        return '<Learner %r %r >' % (self.familyName, self.givenName)


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
