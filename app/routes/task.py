from __future__ import annotations

from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import Length
from app.models import Content, Repository, Task
from app.routes.todo import CreateTodoForm
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from werkzeug.wrappers import Response

bp = Blueprint(
    name="task",
    import_name=__name__,
)


class CreateTaskForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[Length(min=4, max=20, message="Task name must be 4-20 characters")],
        name="name",
    )
    description = StringField(
        "Description",
        validators=[
            Length(
                max=255,
                message="Task description cannot be longer than 255 characters.",
            )
        ],
        name="description",
    )


@bp.route("/repository/<repository_id>/<content_id>/<task_id>", methods=["GET", "POST"])
@login_required
def task(repository_id: str, content_id: str, task_id: str) -> Response | str:
    task = Task.get_by_id(int(task_id))
    repository = Repository.get_by_id(repository_id)
    content = Content.get_by_id(content_id)
    todo_form = CreateTodoForm()
    return render_template(
        "task/task.html",
        task=task,
        todo_form=todo_form,
        content=content,
        repository=repository,
    )


@bp.route("/repository/<repository_id>/<content_id>", methods=["GET", "POST"])
@login_required
def add_task(repository_id: str, content_id: str) -> Response | str:

    form = CreateTaskForm()
    repository = Repository.get_by_id(repository_id)
    content = Content.get_by_id(content_id)

    if form.validate_on_submit():
        task = Task.add(
            name=form.name.data,
            description=form.description.data,
            content_id=content.id,
        )
        if task is None:
            return "Failed to create task", 500

    return redirect(
        url_for(
            "repository.repository", repository_id=repository.id, content=content.id
        )
    )
