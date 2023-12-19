from datetime import datetime
from coupans_manager.models import User, Coupan
from flask import abort, render_template, flash, redirect, url_for, request
from coupans_manager.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    CoupanForm,
)
from coupans_manager import app, bcrypt, db
from flask_login import login_required, login_user, current_user, logout_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/coupans")
def show_coupans():
    coupans_list = Coupan.query.all()
    return render_template("coupans.html", coupans=coupans_list, title="ALL COUPANS")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        user_1 = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user_1)
        db.session.commit()

        flash(f"Your Account is created", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user_1 = User.query.filter_by(email=form.email.data).first()

        if user_1 and bcrypt.check_password_hash(user_1.password, form.password.data):
            login_user(user_1, form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Unsuccessful login attempt.Check details", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been  updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)


@app.route("/coupan/new", methods=["GET", "POST"])
@login_required
def new_coupan():
    form = CoupanForm()
    if form.validate_on_submit():
        coupan_1 = Coupan(
            title=form.title.data,
            code=form.code.data,
            platform_apply=form.platform_apply.data,
            platform_get=form.platform_get.data,
            expiry_date=form.expiry_date.data,
            details=form.details.data,
            author=current_user,
        )
        db.session.add(coupan_1)
        db.session.commit()

        flash("New Coupan Added", "success")
        return redirect(url_for("show_coupans"))

    return render_template(
        "create_coupan.html", title="New Coupan", form=form, legend="CReate COupan"
    )


@app.route("/coupan/<int:coupan_id>")
def coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    return render_template(
        "coupan.html",
        title=coupan_1.title,
        coupan=coupan_1,
    )


@app.route("/coupan/<int:coupan_id>/update", methods=["GET", "POST"])
@login_required
def update_coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    if coupan_1.author != current_user:
        abort(403)
    form = CoupanForm()

    if form.validate_on_submit():
        coupan_1.title = form.title.data
        coupan_1.code = form.code.data
        coupan_1.platform_apply = form.platform_apply.data
        coupan_1.platform_get = form.platform_get.data
        coupan_1.details = form.details.data
        coupan_1.date_posted = datetime.utcnow()
        db.session.commit()
        flash("Coupans details Updated", "success")
        return redirect(url_for("coupan", coupan_id=coupan_1.id))
    elif request.method == "GET":
        form.title.data = coupan_1.title
        form.code.data = coupan_1.code
        form.platform_apply.data = coupan_1.platform_apply
        form.platform_get.data = coupan_1.platform_get
        form.expiry_date.data = coupan_1.expiry_date
        form.details.data = coupan_1.details

    return render_template(
        "create_coupan.html", title="Update Coupan", form=form, legend="Update COupan"
    )
