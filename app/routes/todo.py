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

from app.models import Content, Repository, Task, Todo

bp = Blueprint(
    name="todo",
    import_name=__name__,
)

class CreateTodoForm(FlaskForm):
    description = StringField(
        "Description",
        validators=[Length(max=255, message="Todo description cannot be longer than 255 characters")]
    )
    
@bp.route("/repository/<repository_id>/<content_id>/<task_id>/add-todo", methods=["GET", "POST"])
@login_required
def create(task_id: str, repository_id: str, content_id: str) -> str:
    todo_form = CreateTodoForm()
    task = Task.get_by_id(task_id)
    todo = Todo.add(
        description = todo_form.description.data, 
        task_id = task_id
        )
    return redirect(url_for("task.task", 
                            task_id=task.id, 
                            content_id=content_id, 
                            repository_id=repository_id
                            ))

@bp.route("/repository/<repository_id>/<content_id>/<task_id>/<todo_id>/complete", methods=["GET", "POST"])
@login_required
def complete(task_id : str, repository_id : str, content_id : str, todo_id : str) -> str:
    todo = Todo.get_by_id(todo_id)
    if todo is not None:
        todo.set_complete(current_user)
    return redirect(url_for("task.task", 
                        task_id=task_id, 
                        content_id=content_id, 
                        repository_id=repository_id
                        ))
@bp.route("/repository/<repository_id>/<content_id>/<task_id>/<todo_id>/uncomplete", methods=["GET", "POST"])
@login_required
def uncomplete(task_id : str, repository_id : str, content_id : str, todo_id : str) -> str:
    todo = Todo.get_by_id(todo_id)
    if todo is not None:
        todo.set_uncomplete()
    return redirect(url_for("task.task", 
                        task_id=task_id, 
                        content_id=content_id, 
                        repository_id=repository_id
                        ))
    
@bp.route("/repository/<repository_id>/<content_id>/<task_id>/<todo_id>/delete", methods=["GET", "POST"])
@login_required
def delete(task_id : str, repository_id : str, content_id : str, todo_id : str) -> str:
    todo = Todo.delete_by_id(todo_id)
    print('succres')
    return redirect(url_for("task.task", 
                        task_id=task_id, 
                        content_id=content_id, 
                        repository_id=repository_id
                        ))