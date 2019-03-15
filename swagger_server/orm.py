from sqlalchemy import create_engine, Column, DateTime, String, Integer, Boolean, DECIMAL, JSON
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Learner_db(Base):
    __tablename__ = 'learner'
    id = Column(Integer, primary_key=True)
    openid = Column(String(120), nullable=False)
    validated = Column(Boolean, nullable=False)
    isAdmin = Column(Boolean, nullable=False)
    givenName = Column(String(120), nullable=False)
    familyName = Column(String(120), nullable=False)
    nickname = Column(String(120), nullable=True)
    isMentor = Column(Boolean, nullable=False)
    gender = Column(String(120), nullable=False)
    ethnicity = Column(String(120), nullable=False)
    birthday = Column(String(120), nullable=False)
    status = Column(String(120), nullable=False)
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
    custodianInfo = Column(JSON, nullable=True)
    emergentContact = Column(JSON, nullable=False)
    contactInfo = Column(JSON, nullable=False)
    medicalInfo = Column(JSON, nullable=False)
    notes = Column(JSON, nullable=True)

    def __repr__(self):
        return '<Learner %r %r >' % (self.familyName, self.givenName)


class Project_db(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    status = Column(String(10), nullable=False)
    createdTime = Column(String(120), nullable=False)
    createdByID = Column(Integer)
    createdBy = Column(String(120), nullable=False)
    relatedCourseId = Column(Integer)
    relatedCourse = Column(String(120), nullable=False)
    projectTerm = Column(String(120), nullable=False)
    projectTermLength = Column(DECIMAL(5, 2))
    projectStartDate = Column(String(120), nullable=False)
    averageIntendedCreditHourPerWeek = Column(DECIMAL(5, 2))
    totalIntendedCreditHour = Column(DECIMAL(10, 2))
    projectMentorID = Column(Integer)
    projectMentor = Column(String(120), nullable=True)
    averageGuidingHourPerWeek = Column(DECIMAL(5, 2))
    projectMeta = Column(JSON, nullable=True)
    projectApprovalInfo = Column(JSON, nullable=True)
    content = Column(JSON, nullable=True)
    conclusionInfo = Column(JSON, nullable=True)
    lastUpdatedTime = Column(String(120), nullable=True)


def init_db(uri):
    # ssl_args = {'ssl': {'ca': './config/amazon-rds-ca-cert.pem'}}
    # engine = create_engine(uri, convert_unicode=True, connect_args=ssl_args)
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
