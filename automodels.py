# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, SmallInteger, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class FrkCountry(Base):
    __tablename__ = 'frk_country'

    countryId = Column(String(2), primary_key=True, server_default=text("''"))
    name = Column(String(100), nullable=False, server_default=text("''"))


class FrkItem(Base):
    __tablename__ = 'frk_item'

    itemId = Column(Integer, primary_key=True)
    projectId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    itemParentId = Column(Integer, nullable=False, server_default=text("'0'"))
    priority = Column(Integer, nullable=False, server_default=text("'0'"))
    context = Column(String(80), nullable=False, server_default=text("''"))
    title = Column(String(255), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)
    deadlineDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    expectedDuration = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    showInCalendar = Column(Integer, nullable=False, server_default=text("'0'"))
    showPrivate = Column(Integer, nullable=False, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    authorId = Column(Integer, nullable=False, server_default=text("'0'"))


class FrkItemComment(Base):
    __tablename__ = 'frk_itemComment'

    itemCommentId = Column(BigInteger, primary_key=True)
    itemId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, server_default=text("'0'"))
    postDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    body = Column(Text, nullable=False)
    lastChangeDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class FrkItemFile(Base):
    __tablename__ = 'frk_itemFile'

    itemFileId = Column(BigInteger, primary_key=True)
    itemId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, server_default=text("'0'"))
    fileTitle = Column(String(200), nullable=False, server_default=text("''"))
    filename = Column(String(127), nullable=False, server_default=text("''"))
    filetype = Column(String(30), nullable=False, server_default=text("''"))
    filesize = Column(BigInteger, nullable=False, server_default=text("'0'"))
    postDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    lastChangeDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    fileTags = Column(String(255), nullable=False, server_default=text("''"))


class FrkItemStatu(Base):
    __tablename__ = 'frk_itemStatus'

    itemStatusId = Column(BigInteger, primary_key=True)
    itemId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    statusDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    statusKey = Column(Integer, nullable=False, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, server_default=text("'0'"))


class FrkMember(Base):
    __tablename__ = 'frk_member'

    memberId = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False, server_default=text("''"))
    title = Column(String(20), nullable=False, server_default=text("''"))
    firstName = Column(String(50), nullable=False, server_default=text("''"))
    middleName = Column(String(50), nullable=False, server_default=text("''"))
    lastName = Column(String(50), nullable=False, server_default=text("''"))
    zipCode = Column(String(20), nullable=False, server_default=text("''"))
    city = Column(String(60), nullable=False, server_default=text("''"))
    stateCode = Column(String(2), nullable=False, server_default=text("''"))
    countryId = Column(String(2), nullable=False, server_default=text("''"))
    phone = Column(String(30), nullable=False, server_default=text("''"))
    mobile = Column(String(30), nullable=False, server_default=text("''"))
    fax = Column(String(30), nullable=False, server_default=text("''"))
    username = Column(String(20), nullable=False, index=True, server_default=text("''"))
    password = Column(String(60), nullable=False, server_default=text("''"))
    salt = Column(String(8), nullable=False, server_default=text("''"))
    autoLogin = Column(Integer, nullable=False, server_default=text("'0'"))
    timeZone = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    expirationDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    lastLoginDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    lastLoginAddress = Column(String(60), nullable=False, server_default=text("''"))
    creationDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    lastChangeDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    visits = Column(Integer, nullable=False, server_default=text("'0'"))
    badAccess = Column(Integer, nullable=False, server_default=text("'0'"))
    level = Column(Integer, nullable=False, server_default=text("'0'"))
    activation = Column(String(16), nullable=False, server_default=text("''"))
    authorId = Column(Integer, nullable=False, server_default=text("'0'"))
    enabled = Column(Integer, nullable=False, server_default=text("'0'"))


class FrkMemberProject(Base):
    __tablename__ = 'frk_memberProject'

    memberId = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    projectId = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    position = Column(Integer, nullable=False, server_default=text("'0'"))


class FrkProject(Base):
    __tablename__ = 'frk_project'

    projectId = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)


class FrkProjectStatu(Base):
    __tablename__ = 'frk_projectStatus'

    projectStatusId = Column(Integer, primary_key=True)
    projectId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    statusDate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    statusKey = Column(Integer, nullable=False, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, server_default=text("'0'"))


class ModNewitem(Base):
    __tablename__ = 'mod_newitems'

    itemId = Column(Integer, primary_key=True)
    projectId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    itemParentId = Column(Integer, nullable=False, server_default=text("'0'"))
    priority = Column(Integer, nullable=False, server_default=text("'0'"))
    context = Column(String(80), nullable=False, server_default=text("''"))
    title = Column(String(255), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)
    deadlineDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    expectedDuration = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    showInCalendar = Column(Integer, nullable=False, server_default=text("'0'"))
    showPrivate = Column(Integer, nullable=False, server_default=text("'0'"))
    memberId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    authorId = Column(Integer, nullable=False, server_default=text("'0'"))
