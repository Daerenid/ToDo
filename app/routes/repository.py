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

from app.models import Repository, User

bp = Blueprint(
    name="repository",
    import_name=__name__,
)

RECENT_REPOSITORY_QUEUE_SIZE = 5

def get_recent_repositories(recent_repositories_ids: list[str]) -> list[Repository]:
    """
    Get all the recent repositories current_user has access to.
    Requires request context to get current_user.
    """
    return [
        repository
        for recent_id in recent_repositories_ids
        for repository in current_user.repositories
        if repository.id == recent_id
    ]

@bp.route("/repositories")
@login_required
def repositories() -> str:

    return render_template(
        "repository/repositories.html",
        owned_repositories=current_user.owned_repositories,
        repositories=current_user.repositories,
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
    description = StringField(
        "Description",
        validators=[
            Length(
                max=2048,
                message="repository description cannot be longer than 2048 characters.",
            ),
        ],
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

        return redirect(url_for("repository.repository", repository_id=repository.id))

    return render_template("repository/create.html", create_repository_form=form)


@bp.route("/repository/<repository_id>/edit")
@login_required
def edit_repository(repository_id: str) -> str:

    repository = Repository.get_by_id(repository_id)
    return render_template("repository/edit.html", repository=repository)


@bp.route("/repository/<repository_id>")
@login_required
def repository(repository_id: str) -> str:
    repository = Repository.get_by_id(repository_id)

    return render_template(
        "repository/repository.html",
        repository=repository,
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

