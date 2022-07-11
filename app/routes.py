from app import app
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, NewRepository, NewTask, NewContent,  NewTodo
from app.models import User, Repository, Content, Todo, Task
from datetime import datetime

@app.route('/')
def inde2():
    return render_template('views/homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.get_repositories() == None:
           return redirect(url_for('new_user')) 
        repositories = current_user.get_repositories()
        print(repositories[0].id)
        return redirect(url_for('content'))
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Niepoprawny login lub hasło')
            return redirect(url_for('login'))
        login_user(user)   
        repositories = current_user.get_repositories()
        if user.get_repositories() == None:
            return redirect(url_for('new_user'))

        return redirect(url_for('content'))
    return render_template('views/login.html', form=form)

@app.route('/new-user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        repository = Repository(name=request.form['name'])
        current_user.add_repository(repository)
        print(f'Dodano repozytorium {request.form["name"]}, dla użytkownika {current_user.username}')
        return redirect(url_for('home', id=repository.id))
    return render_template('views/new_user.html', user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     if current_user.get_repositories() == None:
    #        return redirect(url_for('new_user')) 
    #     repositories = current_user.get_repositories()
    #     return redirect(url_for('home', id=repositories[0].id))

    form = RegistrationForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User(username=username, email=email)
        user.set_password(password)
        user.add_user()
        login_user(user)
        print(f'User: {username}, {email} added')
        return redirect(url_for('conent'))

    return render_template('views/register.html', form=form)

@app.route('/content/repository/<id>', methods=['GET', 'POST'])
@app.route('/content/repositories', methods=['GET', 'POST'])
def repository(id=None):
    repositories = current_user.get_repositories()
    
    # repository = Repository.get_repository(id)
    if id:
        repository = Repository.get_repository(id)
        return render_template('views/repository.html',
            user=current_user, 
            repositories=repositories,
            repository=repository
        )
    return render_template('views/repositories.html',
        user=current_user, 
        repositories=repositories,
    )

# @app.route('/content/repositories', methods=['GET', 'POST'])
# def repositories():
#     repositories = current_user.get_repositories()
#     return render_template('views/repositories.html',
#         user=current_user, 
#         repositories=repositories,
# )


@app.route('/content', methods=['GET', 'POST'])
def content():
    # repository_form = NewRepository()
    # content_form = NewContent()
    # todo_form = NewTodo()
    # task_form = NewTask()
    # task_form = NewTask()

    repositories = current_user.get_repositories()
    # repository = Repository.get_repository(id)
    # contents = repository.contents

    # if repository_form.validate_on_submit() and repository_form.rep_submit.data:
    #     rep = Repository(name=repository_form.name.data)
    #     current_user.add_repository(rep)
    #     return redirect(url_for('content', id=id))

    # if content_form.validate_on_submit() and content_form.cont_submit.data:
    #     con = Content(name=content_form.name.data, repository_id=repositories[0])
    #     repository.add_contents(con)
    #     return redirect(url_for('content', id=id))

    # if todo_form.validate_on_submit() and todo_form.todo_submit.data:
    #     print(todo_form.task_id.data)
    #     todo = Todo(description=todo_form.description.data, created_at=datetime.now(), status=0, task_id=request.form.get('task_id'))
    #     task = Task.get_task(request.form.get())
    #     task.add_todo(todo)
    #     return redirect(url_for('content', id=id))

    # if task_form.validate_on_submit() and task_form.task_submit.data:
    #     pass


    return render_template('homepage.html',
        user=current_user, 
        # contents=contents,
        repositories=repositories,
        # repository_form = repository_form,
        # content_form = content_form,
        # repository = repository,
        # todo_form = todo_form,
        # task_form = task_form
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')