from sqlalchemy import create_engine, Column, DateTime, String, Integer, Boolean, DECIMAL, JSON, ForeignKey, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Learner_db(Base):
    __tablename__ = 'learner'
    id = Column(Integer, primary_key=True)
    branch = Column(String(45), nullable=True)
    openid = Column(String(120), nullable=False)
    unionid = Column(String(120), nullable=True)
    openidWeApp = Column(String(120), nullable=True)
    sessionKey = Column(String(120), nullable=True)
    validated = Column(Boolean, nullable=False)
    isAdmin = Column(Boolean, nullable=False)
    givenName = Column(String(120), nullable=False)
    familyName = Column(String(120), nullable=False)
    role = Column(String(120), nullable=False)
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
    microsoftAccessToken = Column(String(2000), nullable=True)
    microsoftRefreshToken = Column(String(2000), nullable=True)
    microsoftId = Column(String(120), nullable=True)
    microsoftUserPrincipalName = Column(String(120), nullable=True)

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
    coverImageURL = Column(String(120), nullable=True)


class Course_db(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    status = Column(String(10), nullable=False)
    createdTime = Column(String(120), nullable=False)
    createdByID = Column(Integer)
    createdBy = Column(String(120), nullable=False)
    creditHourPerWeek = Column(DECIMAL(5, 2))
    courseTimeShift = Column(JSON, nullable=True)
    courseLengthInWeeks = Column(Integer)
    courseMeta = Column(JSON, nullable=True)
    content = Column(JSON, nullable=True)
    coverImageURL = Column(String(120), nullable=True)


class Config_db(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    value = Column(JSON, nullable=True)


class BookingNotes_db(Base):
    __tablename__ = 'bookingNotes'
    id = Column(Integer, primary_key=True)
    changekey = Column(String(100), nullable=False)
    bookedByID = Column(Integer, nullable=False)
    bookedByName = Column(String(120), nullable=False)


class PushMessage_db(Base):
    __tablename__ = 'pushMessage'
    id = Column(Integer, primary_key=True)
    messageType = Column(String(10), nullable=False)
    entityId = Column(Integer, nullable=True, comment='信息相关记录id（只记录id数值，不作表关联')
    senderId = Column(Integer, ForeignKey("learner.id"), nullable=False)
    senderDisplayName = Column(String(20), nullable=True)
    recipients = Column(JSON, nullable=True)
    rsvp = Column(JSON, nullable=True)
    sentDateTime = Column(DateTime)
    modifiedDateTime = Column(DateTime)
    expireDateTime = Column(DateTime)
    content = Column(JSON, nullable=True)


class Event_db(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    pushMessageId = Column(Integer, ForeignKey("pushMessage.id"), nullable=True)
    initiatorId = Column(Integer, ForeignKey("learner.id"), nullable=False)
    initiatorDisplayName = Column(String(20), nullable=True)
    eventInfo = Column(JSON, nullable=True)
    invitee = Column(JSON, nullable=True)
    thumbnail = Column(JSON, nullable=True)


class Announcement_db(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, primary_key=True)
    pushMessageId = Column(Integer, ForeignKey("pushMessage.id"), nullable=True)
    initiatorId = Column(Integer, ForeignKey("learner.id"), nullable=False)
    initiatorDisplayName = Column(String(20), nullable=True)
    recipients = Column(JSON, nullable=True)
    sentDateTime = Column(DateTime)
    modifiedDateTime = Column(DateTime)
    expireDateTime = Column(DateTime)
    thumbnail = Column(JSON, nullable=True)
    body = Column(JSON, nullable=True)


def init_db(uri):
    # ssl_args = {'ssl': {'ca': './config/amazon-rds-ca-cert.pem'}}
    # engine = create_engine(uri, convert_unicode=True, connect_args=ssl_args)
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
