from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

repositoryuser = db.Table('repositoryuser',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('repository_id', db.Integer, db.ForeignKey('repository.id'))
)

class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104))

    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'))
    tasks = db.relationship('Task', backref='content', lazy=True)


class Repository(db.Model):
    __tablename__ = 'repository'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104))

    contents = db.relationship('Content', backref='repository', lazy=True)

    def add_contents(self, content):
        self.contents.append(content)
        db.session.add(content)
        db.session.commit()
    
    def get_repository(id):
        return Repository.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    repositories = db.relationship(
        'Repository', secondary=repositoryuser,
        primaryjoin=(repositoryuser.c.user_id == id),
        secondaryjoin=(repositoryuser.c.repository_id == Repository.id),
        backref=db.backref('repositoryuser', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def add_repository(self, repository):
        self.repositories.append(repository)
        db.session.add(repository)
        db.session.commit()

    def add_user(self):
        db.session.add(self)
        db.session.commit()


    def get_repositories(self):
        result = Repository.query.join(repositoryuser, (
            repositoryuser.c.repository_id == Repository.id
        )).filter(repositoryuser.c.user_id == self.id)
        if len(result.all()) < 1:
            return None
        return result.all()

    def __repr__(self):
        return f'<User: {self.username}>'
    

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1048))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.Boolean)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


    def __repr__(self):
        return f'<Task: {self.id}, description: {self.description}, created_at: {self.created_at}>'
    

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104))
    description = db.Column(db.String(1048))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime,  index=True, default=datetime.utcnow)
    status = db.Column(db.Boolean)
    # status2 = db.Column(db.Boolean)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))

    todos = db.relationship('Todo', backref='task', lazy=True)

    def get_task(id):
        return Task.query.get(int(id))


    def add_todo(self, todo):        
        self.todos.append(todo)
        db.session.add(todo)
        db.session.commit()


