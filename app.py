import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextAreaField


import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, SmallInteger, String, Text, text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, Session




app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cristian:123456@127.0.0.1:3306/taskfrea'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://cristian:123456@127.0.0.1:3306/taskfreak')

db.session = Session(engine)

Base = declarative_base()
metadata = Base.metadata

class Priority(Base):
    __tablename__ = 'priority'

    id = Column(Integer, primary_key=True)
    text = Column(String(20), server_default=text("''"))

class FrkCountry(Base):
    __tablename__ = 'frk_country'

    countryId = Column(String(2), primary_key=True, server_default=text("''"))
    name = Column(String(100), nullable=False, server_default=text("''"))

class FrkMember(Base):
    __tablename__ = 'frk_member'

    memberId = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False, server_default=text("''"))
    title = Column(String(20), nullable=False, server_default=text("''"))
    firstName = Column(String(50, convert_unicode=True), nullable=False, server_default=text("''"))
    middleName = Column(String(50, convert_unicode=True), nullable=False, server_default=text("''"))
    lastName = Column(String(50, convert_unicode=True), nullable=False, server_default=text("''"))
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

    # tasks_assigned = relationship("FrkItem")

    # tasks_created = relationship("FrkItem")

    def __repr__(self):
        return '%s' %self.firstName


class FrkItem(Base):
    __tablename__ = 'frk_item'

    itemId = Column(Integer, primary_key=True)
    itemParentId = Column(Integer, server_default=text("'0'"))
    context = Column(String(80), server_default=text("''"))
    title = Column(String(255, convert_unicode=True), nullable=False, server_default=text("''"))
    description = Column(String(convert_unicode=True), nullable=False)
    deadlineDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    expectedDuration = Column(SmallInteger, server_default=text("'0'"))
    showInCalendar = Column(Integer, server_default=text("'0'"))
    showPrivate = Column(Integer, server_default=text("'0'"))

    priority = Column(Integer, db.ForeignKey("priority.id"), nullable=False, server_default=text("'0'"))
    memberId = Column(Integer, db.ForeignKey("frk_member.memberId"), nullable=False, index=True, server_default=text("'0'"))
    authorId = Column(Integer, db.ForeignKey("frk_member.memberId"), nullable=False, server_default=text("'0'"))
    projectId = Column(Integer, db.ForeignKey("frk_project.projectId"), nullable=False, index=True, server_default=text("'0'"))
    # projectId = Column(Integer, nullable=False, index=True, server_default=text("'0'"))

    responsible = db.relationship("FrkMember", backref="tasks_assigned", foreign_keys=memberId)
    author = db.relationship("FrkMember", backref="tasks_created", foreign_keys=authorId)
    project = db.relationship("FrkProject", backref="tasks", foreign_keys=projectId)
    priority_text = db.relationship("Priority", backref="tasks", foreign_keys=priority)

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

    def __repr__(self):
        return self.name


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


Base.metadata.create_all(bind=engine)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'




class UserAdmin(sqla.ModelView):
    def __init__(self, session):
        super(UserAdmin, self).__init__(FrkMember, session)

class TaskAdmin(sqla.ModelView):
    # inline_models = (FrkItem,)
    column_exclude_list = ('context', 'itemParentId', 'expectedDuration', 'showPrivate', 'showInCalendar', ('priority', 'priority.text'))

    column_sortable_list = ('title', ('responsible','responsible.firstName'), ('author','author.firstName'), 'deadlineDate', 'description')

    column_searchable_list = ('title', 'description', 'responsible.firstName', 'author.firstName')

    column_filters = ('title',
                      'description',
                      'responsible',
                      'author')

    form_overrides = dict(description=TextAreaField)

    form_excluded_columns = ('context', 'itemParentId', 'expectedDuration', 'showPrivate', 'showInCalendar')

    form_ajax_refs = {
        'responsible': {
            'fields': (FrkMember.firstName,)
        },
        'author': {
            'fields': (FrkMember.firstName,)
        },
        'project': {
            'fields': {FrkProject.name,}
        }
    }

    def __init__(self, session):
        super(TaskAdmin, self).__init__(FrkItem, session)


# Create admin
admin = admin.Admin(app, name='Example: SQLAlchemy', template_mode='bootstrap3')

# Add views
admin.add_view(TaskAdmin(db.session))
admin.add_view(UserAdmin(db.session))


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))

    # db.metadata.
    # Start app
    app.run(debug=True)
