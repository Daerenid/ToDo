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

from app.models import Repository

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


def rotate_recent_repositories_ids(
    recent_repositories: list[str], repository_id: str
) -> list[str]:
    """
    Add repository_id to the list of repositories recently visited by current_user.
    If repository_id is already in the list, move it up the list.
    """
    if repository_id not in recent_repositories:
        if len(recent_repositories) >= RECENT_REPOSITORY_QUEUE_SIZE:
            del recent_repositories[-1]
    else:
        recent_repositories.remove(repository_id)

    recent_repositories.insert(0, repository_id)

    return recent_repositories


@bp.route("/repositories")
@login_required
def repositories() -> str:

    # Get recent repositories (make sure current_user has access to them)
    cookie_name = get_recent_repositories_cookie_name()
    recent_ids = get_recent_repositories_ids(cookie_name)
    recent_repositories = get_recent_repositories(recent_ids)

    return render_template(
        "repository/repositories.html",
        recent_repositories=recent_repositories,
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
    print("jestem tu")
    repository = Repository.get_by_id(repository_id)
    return render_template("repository/edit.html", repository=repository)


@bp.route("/repository/<repository_id>")
@login_required
def repository(repository_id: str) -> str:
    print("jestem tu 2")
    repository = Repository.get_by_id(repository_id)

    return render_template(
        "repository/repository.html",
        repository=repository,
        participants=repository.participants,
    )
