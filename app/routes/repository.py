from __future__ import annotations

from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import Length

from app.models import Repository, User
from app.routes.task import CreateTaskForm

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from werkzeug.wrappers import Response

bp = Blueprint(
    name="repository",
    import_name=__name__,
)


class CreateRepositoryForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            Length(
                min=4, message="repository name must be at least 4 characters long."
            ),
            Length(
                max=255, message="repository name cannot be longer than 255 characters."
            ),
        ],
        name="name",
    )
    description = TextAreaField(
        "Description",
        validators=[
            Length(
                max=2048,
                message="repository description cannot be longer than 2048 characters.",
            ),
        ],
    )


@bp.route("/repositories")
@login_required
def repositories() -> Response | str:
    create_repository_form = CreateRepositoryForm()
    return render_template(
        "repository/repositories.html",
        create_repository_form=create_repository_form,
        repositories=current_user.repositories,
    )


@bp.route("/create-repository", methods=["GET", "POST"])
@login_required
def create() -> Response | str:

    form = CreateRepositoryForm()
    if form.validate_on_submit():
        repository = Repository.add(
            name=form.name.data, description=form.description.data, owner=current_user
        )

        if repository is None:
            return "Failed to create repository.", 500

    return redirect(
        url_for(
            "repository.repositories",
            repositories=current_user.repositories,
        )
    )


@bp.route("/repository/<repository_id>/edit")
@login_required
def edit_repository(repository_id: str) -> Response | str:
    repository = Repository.get_by_id(repository_id)
    return render_template("repository/edit.html", repository=repository)


@bp.route("/repository/<repository_id>")
@login_required
def repository(repository_id: str) -> Response | str:
    repository = Repository.get_by_id(repository_id)
    task_form = CreateTaskForm()
    return render_template(
        "repository/repository.html",
        repository=repository,
        task_form=task_form,
        participants=repository.participants,
    )


@bp.route("/repository/<repository_id>/user/delete/<user_id>", methods=["GET", "POST"])
@login_required
def delete_user(user_id: str, repository_id: str) -> str:
    user = User.get_by_id(user_id)
    repository = Repository.get_by_id(repository_id)
    if current_user == repository.owner:
        if user in repository.participants:
            repository.remove_participant(user)
    return redirect(url_for("repository.repository", repository_id=repository.id))
