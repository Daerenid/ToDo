from __future__ import annotations

from flask import (
    Blueprint,
    Response,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import Length

from app.models import Content, Repository, Task

bp = Blueprint(
    name="task",
    import_name=__name__,
)

RECENT_TASK_QUEUE_SIZE = 5


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
                message="Task description cannot be longer than 2048 characters.",
            )
        ],
        name="description",
    )


@bp.route("/repository/<repository_id>/<content_id>/<task_id>", methods=["GET", "POST"])
@login_required
def task(repository_id, content_id, task_id) -> str:
    task = Task.get_by_id(int(task_id))
    return render_template("task/task.html", task=task)


@bp.route("/repository/<repository_id>/<content_id>", methods=["GET", "POST"])
@login_required
def add_task(repository_id, content_id) -> str:

    form = CreateTaskForm()
    repository = Repository.get_by_id(repository_id)
    content = repository.contents[int(content_id) - 1]

    if form.validate_on_submit():
        task = Task.add(
            name=form.name.data,
            description=form.description.data,
            content_id=content.id,
        )
        if task is None:
            return "Failed to create task", 500

        return redirect(url_for("repository.repository", repository_id=repository.id))

    return render_template(
        "task/create.html",
        create_task_form=form,
        repository=repository,
        content=content,
    )
