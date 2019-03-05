from sqlalchemy import create_engine, Column, DateTime, String, Integer, Boolean, UnicodeText, DECIMAL
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Learner_db(Base):
    __tablename__ = 'learner'
    id = Column(Integer, primary_key=True)
    openid = Column(String(120), nullable=False)
    validated = Column(Boolean, nullable=False)
    isAdmin = Column(Boolean, nullable=False),
    isCommitteeOfAcademics = Column(Boolean, nullable=False)
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
    custodianInfo = Column(UnicodeText, nullable=True)
    emergentContact = Column(UnicodeText, nullable=False)
    contactInfo = Column(UnicodeText, nullable=False)
    medicalInfo = Column(UnicodeText, nullable=False)
    notes = Column(UnicodeText, nullable=True)

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
    projectMentor = Column(String(120), nullable=False)
    averageGuidingHourPerWeek = Column(DECIMAL(5, 2))
    projectMeta = Column(UnicodeText, nullable=True)
    projectApprovalInfo = Column(UnicodeText, nullable=True)
    content = Column(UnicodeText, nullable=True)
    conclusionInfo = Column(UnicodeText, nullable=True)
    lastUpdatedTime = Column(String(120), nullable=True)


def init_db(uri):
    ssl_args = {'ssl': {'ca': '../config/amazon-rds-ca-cert.pem'}}
    engine = create_engine(uri, convert_unicode=True, connect_args=ssl_args)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
