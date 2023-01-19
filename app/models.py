"""
ORM models.

Models implement only the most basic functionality.
More complex queries are implemented in the methods
responsible for given functionality.
"""

from __future__ import annotations

from typing import Optional

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

association_user_repository = db.Table(
    "user_repository",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("repository_id", db.Integer, db.ForeignKey("repository.id")),
)


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now())

    # Relation with daily
    dailys = db.relationship("Daily", backref="User", lazy=True)

    # Relations with repository
    owned_repositories = db.relationship("Repository", back_populates="owner")
    repositories = db.relationship(
        "Repository",
        secondary=association_user_repository,
        back_populates="participants",
    )

    @classmethod
    def add(cls, email: str, username: str, password: str) -> User:
        user = cls(
            email=email,
            username=username,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get_all_users(cls) -> list:
        users = User.query.all()
        return users

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id: str) -> Optional[User]:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username: str) -> Optional[User]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def is_email_available(cls, email: str) -> bool:
        return cls.get_by_email(email) is None

    @classmethod
    def is_username_available(cls, username: str) -> bool:
        return cls.query.filter_by(username=username).first() is None

    def change_password(self, password: str) -> None:
        self.password == generate_password_hash(password, method="sha256")
        db.session.commit()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"<User: {self.username}>"


class Repository(db.Model):  # type: ignore
    __tablename__ = "repository"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104), nullable=False)
    description = db.Column(db.String(1048), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    last_modified = db.Column(db.DateTime, server_default=func.now())

    # Relation with Content
    contents = db.relationship("Content", backref="repository", lazy=True)

    # Relations with User
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=None)
    owner = db.relationship("User", back_populates="owned_repositories")
    participants = db.relationship(
        "User", secondary=association_user_repository, back_populates="repositories"
    )

    @classmethod
    def add(cls, name: str, description: Optional[str], owner: User) -> Repository:
        repository = cls(name=name, description=description, owner_id=owner.id)
        # Make sure owner is also a participant in the repository
        repository.participants.append(owner)

        db.session.add(repository)

        # Create basic content view
        content_done = Content.add("Done", repository.id)
        content_todo = Content.add("ToDo", repository.id)
        content_in_progress = Content.add("In progress", repository.id)

        repository.contents.append(content_done)
        repository.contents.append(content_todo)
        repository.contents.append(content_in_progress)

        db.session.commit()

        return repository

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Repository]:
        return cls.query.get(id)

    def add_contents(self, content: Content) -> None:
        self.contents.append(content)
        db.session.commit()

    def add_user(self, user: object):
        self.participants.append(user)
        db.session.commit()

    def remove_participant(self, user: object) -> None:
        self.participants.remove(user)
        db.session.commit()


class Content(db.Model):  # type: ignore
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104), nullable=False)

    # Relation with repository
    repository_id = db.Column(db.Integer, db.ForeignKey("repository.id"))

    # Relation with tasks
    tasks = db.relationship("Task", backref="content", lazy=True)

    @classmethod
    def add(cls, name: str, repository_id: int) -> Content:
        content = cls(name=name, repository_id=repository_id)

        db.session.add(content)
        db.session.commit()

        return content

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Content]:
        return cls.query.get(id)

    def add_tasks(self, task: Task) -> None:
        self.tasks.append(task)
        db.session.commit()


class Task(db.Model):  # type: ignore
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(104), nullable=False)
    description = db.Column(db.String(1048), nullable=False)
    created_at = db.Column(db.DateTime, index=True, server_default=func.now())
    completed_at = db.Column(db.DateTime, index=True, server_default=func.now())
    status = db.Column(db.Boolean, default=False)

    # Relations with content
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))

    # Relations with todos
    todos = db.relationship("Todo", backref="task", lazy=True)

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Task]:
        return cls.query.get(id)

    @classmethod
    def add(cls, name: str, description: str, content_id: int) -> Task:
        task = cls(name=name, description=description, content_id=content_id)

        db.session.add(task)
        db.session.commit()

        return task

    def add_todo(self, todo: Todo) -> None:
        self.todos.append(todo)
        db.session.commit()


class Todo(db.Model):  # type: ignore
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1048), nullable=False)
    created_at = db.Column(db.DateTime, index=True, server_default=func.now())
    completed_at = db.Column(db.DateTime, default=None)
    status = db.Column(db.Boolean, default=False)

    # Relation with user
    completed_by = db.Column(db.String(1048), default=False)

    # Relation with task
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

    @classmethod
    def add(cls, description: str, task_id: int) -> Task:
        todo = cls(description=description, task_id=task_id)

        db.session.add(todo)
        db.session.commit()

        return todo

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Todo]:
        return cls.query.get(id)

    @classmethod
    def delete_by_id(cls, id: str) -> None:
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    def set_complete(self, user: object) -> None:
        self.status = True
        self.completed_at = func.now()
        self.completed_by = user.username
        db.session.commit()

    def set_uncomplete(self) -> None:
        self.status = False
        self.completed_at = None
        self.user = None
        db.session.commit()


class Daily(db.Model):
    __tablename__ = "daily"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1048), nullable=False)
    created_at = db.Column(db.DateTime, index=True, server_default=func.now())
    completed_at = db.Column(db.DateTime, default=None)
    status = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @classmethod
    def add(cls, description: str, user_id: int) -> Daily:
        daily = cls(description=description, user_id=user_id)
        db.session.add(daily)
        db.session.commit()

        return daily

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Daily]:
        return cls.query.get(id)

    @classmethod
    def delete_daily(cls, id: int) -> None:
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    def set_complete(self) -> None:
        self.status = True
        self.completed_at = func.now()
        db.session.commit()
