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
from sqlalchemy.sql import func
from wtforms.fields import StringField
from wtforms.validators import Length

from app.models import Daily

bp = Blueprint(
    name="daily",
    import_name=__name__,
)


class CreateDailyForm(FlaskForm):
    description = StringField(
        "Description",
        validators=[
            Length(
                min=10,
                max=2048,
                message="Daily description must be 10-2048 characters.",
            ),
        ],
    )


@bp.route("/daily")
def daily() -> Response | str:
    if current_user.is_authenticated == False:
        return redirect(url_for("auth.login"))
    create_daily_form = CreateDailyForm()
    return render_template(
        "daily/daily.html",
        current_user=current_user,
        create_daily_form=create_daily_form,
    )


@bp.route("/daily/create", methods=["POST"])
def create() -> Response | str:
    form = CreateDailyForm()
    if form.validate_on_submit():
        daily = Daily.add(description=form.description.data, user_id=current_user.id)
        if daily is None:
            return "Failed to create daily", 500
        return redirect(url_for("daily.daily"))

    return render_template(
        "daily/daily.html", current_user=current_user, create_daily_form=form
    )


@bp.route("/daily/delete/<id>", methods=["GET"])
def delete(id) -> Response | str:
    daily = Daily.get_by_id(id)
    if daily is not None:
        Daily.delete_daily(daily.id)
    return redirect(url_for("daily.daily"))


@bp.route("/daily/complete/<id>", methods=["GET"])
def complete(id) -> Response | str:
    daily = Daily.get_by_id(id)
    if daily is not None:
        daily.set_complete()
    return redirect(url_for("daily.daily"))
