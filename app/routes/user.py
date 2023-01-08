from __future__ import annotations

from flask import (
    Blueprint,
    Response,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import User, Repository

bp = Blueprint(
    name="user",
    import_name=__name__,
)


class SearchUserForm(FlaskForm):
    name = StringField("Name", name="name")

    def validate(self) -> bool:
        if not super().validate():
            return False
        try:
            user = User.is_username_available(self.name.data)
        except Exception as e:
            print(e)
        print(f"JESTEM {user}")
        if user:
            msg = "User not found"
            self.name.errors.append(msg)
            return False
        return True


PASSWORD_VALIDATORS = [
    DataRequired(message="Password is required."),
    Length(min=8, message="Password must be at least 8 characters long."),
]

EMAIL_VALIDATORS = [
    DataRequired(message="Email address is required."),
    Email(message="Please enter valid email address."),
    Length(max=50, message="Email address too long."),
]


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", name="old_password")
    new_password = PasswordField(
        "New password", validators=PASSWORD_VALIDATORS, name="new_password"
    )
    # def validate(self):
    #     if not super().validate():
    #         return False
    #     if current_user.check_password(self.old_password.data):


@bp.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
def show_user(user_id: str) -> str:
    user = User.get_by_id(user_id)
    password_form = ChangePasswordForm()
    if password_form.validate_on_submit():
        if user.check_password(password_form.old_password.data):
            user.change_password(password_form.new_password.data, user.id)
            session["password_message"] = ["Password changed"]
            return redirect(url_for("user.show_user", user_id=user_id))
        session["password_message"] = ["Incorrect password"]
        return redirect(url_for("user.show_user", user_id=user_id))

    return render_template("user/user.html", user=user, password_form=password_form)


@bp.route("/user/search", methods=["GET", "POST"])
@login_required
def search() -> str:
    search_form = SearchUserForm()
    users = User.get_all_users()
    if search_form.validate_on_submit():
        user = User.get_by_username(search_form.name.data)

        return redirect(url_for("user.show_user", user_id=user.id))

    return render_template("user/search.html", search_form=search_form, users=users)

@bp.route("/user/<user_id>/<repository_id>/add", methods=["GET", "POST"])
@login_required
def add_user_to_repository(user_id: str, repository_id: str) -> str:
    user = User.get_by_id(user_id)
    repository = Repository.get_by_id(repository_id)
    repository.add_user(user)
    return redirect(url_for("user.show_user", user_id=user.id))
    
# @bp.route("user/<user_id>/password", methods=["GET", "POST"])
# @login_required
# def change_password(user_id) -> str:
#     user = User.get_by_id(user_id)
#     if user.check_password()
