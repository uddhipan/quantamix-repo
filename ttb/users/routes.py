from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from ttb import db, bcrypt
from datetime import datetime
from ttb.models import (User, Post, Follow, Role, Permission, Address, Occupation, Links, Intrest, Achievement, Events, Travel, Special_event, Media, Sponsership, Language)
from ttb.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, AchievementForm, EventsForm, TravelForm, Special_eventForm,SponsershipForm,
                              LanguageForm, RequestResetForm, ResetPasswordForm, AddressForm, OccupationForm, LinksForm, IntrestForm, MediaForm)
from ttb.users.utils import save_picture, send_reset_email
from ttb.decorators import admin_required, permission_required


users = Blueprint('users', __name__)

@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@users.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@users.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('please complete your profile in profile section after login', 'warning')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account/<int:id>", methods=['GET', 'POST'])
@login_required
def account(id):
    form = UpdateAccountForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.email = form.email.data
        user.about_me= form.about_me.data
        user.education_level = form.education_level.data
        user.gender = form.gender.data
        user.contact_number = form.contact_number.data
        user.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user', id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.about_me.data = user.about_me
        form.education_level.data = user.education_level
        form.gender.data = user.gender
        form.contact_number.data = user.contact_number
        form.date_of_birth.data = user.date_of_birth
    image_file = url_for('static', filename='profile_pics/' + user
        .image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, user=user)


@users.route("/address/<int:id>", methods=['GET', 'POST'])
@login_required
def address(id):
    form = AddressForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        address = Address(street=form.street.data,
                    city=form.city.data,
                    zip_code=form.zip_code.data,
                    country=form.country.data,
                    Protagonist= user)
        db.session.add(address)
        db.session.commit()
        flash('Your address has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', user=user.id))
    return render_template('address.html', title='Address',
                           form=form, legend='Address'  )

@users.route("/Occupation/<int:id>", methods=['GET', 'POST'])
@login_required
def occupation(id):
    form = OccupationForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        occupation = Occupation(occupation_name=form.occupation_name.data,
                    occupation_company=form.occupation_company.data,
                    occupation_start_date=form.occupation_start_date.data,
                    occupation_end_date=form.occupation_end_date.data,
                    Protagonist= user)
        db.session.add(occupation)
        db.session.commit()
        flash('Your occupation has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('occupation.html', title='occupation',
                           form=form, legend='occupation'  )

@users.route("/links/<int:id>", methods=['GET', 'POST'])
@login_required
def links(id):
    form = LinksForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        links = Links(facebook_id=form.facebook_id.data,
                    twitter_id=form.twitter_id.data,
                    instagram_id=form.instagram_id.data,
                    snapchat_id=form.snapchat_id.data,
                    Protagonist= user)
        db.session.add(links)
        db.session.commit()
        flash('Your social links has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('links.html', title='social links',
                           form=form, legend='links'  )

@users.route("/intrest/<int:id>", methods=['GET', 'POST'])
@login_required
def intrest(id):
    form = IntrestForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        intrest = Intrest(intrest_type=form.intrest_type.data,
                    Protagonist= user)
        db.session.add(intrest)
        db.session.commit()
        flash('Your intrest has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('intrest.html', title='Interest',
                           form=form, legend='Interest'  )

@users.route("/achievement/<int:id>", methods=['GET', 'POST'])
@login_required
def achievement(id):
    form = AchievementForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        achievement = Achievement(
                    medal_count=form.medal_count.data,
                    timestamp=form.timestamp.data,
                    Protagonist= user)
        db.session.add(achievement)
        db.session.commit()
        flash('Your Achievement has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('achievement.html', title='Achievement',
                           form=form, legend='Achievement'  )

@users.route("/events/<int:id>", methods=['GET', 'POST'])
@login_required
def events(id):
    form = EventsForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        events = Events(event_name=form.event_name.data,
                    event_description=form.event_description.data,
                    event_location=form.event_location.data,
                    event_start_date=form.event_start_date.data,
                    event_end_date=form.event_end_date.data,
                    event_status=form.event_status.data,
                    Protagonist= user)
        db.session.add(events)
        db.session.commit()
        flash('Your Event has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('event.html', title='Events',
                           form=form, legend='Event'  )

@users.route("/travel/<int:id>", methods=['GET', 'POST'])
@login_required
def travel(id):
    form =TravelForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        travel = Travel(place=form.place.data,
                    start_date=form.start_date.data,
                    end_date=form.end_date.data,
                    Protagonist= user)
        db.session.add(travel)
        db.session.commit()
        flash('Your Travel designation has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('travel.html', title='Travel',
                           form=form, legend='Travel'  )

@users.route("/special_event/<int:id>", methods=['GET', 'POST'])
@login_required
def special_event(id):
    form =Special_eventForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        special_event = Special_event(life_event=form.life_event.data,
                    life_event_start_date=form.life_event_start_date.data,
                    life_event_end_date=form.life_event_end_date.data,
                    Protagonist= user)
        db.session.add(special_event)
        db.session.commit()
        flash('Your Special event n has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('special_event.html', title='Special event',
                           form=form, legend='Special event'  )

@users.route("/media/<int:id>", methods=['GET', 'POST'])
@login_required
def media(id):
    form =MediaForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(id)
        picture_file = save_picture(form.image.data)
        media = media( 
                          
                     media_name = picture_file,
                    media_format=form.media_format.data,
                    Protagonist= user)
        db.session.add(media)
        db.session.commit()
        media_name = url_for('static', filename='pictures/' + user.media_name)
        flash('Your  image  has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('media.html', title='upload',
                            form=form, legend='Add image '  )


@users.route("/language/<int:id>", methods=['GET', 'POST'])
@login_required
def language(id):
    form = LanguageForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        language =  Language(language=form.language.data,
                    language_accuracy=form.language_accuracy.data,
                    Protagonist= user)
        db.session.add(language)
        db.session.commit()
        flash('Your Language has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('language.html', title=' Language',
                           form=form, legend=' Languages'  )

@users.route("/sponsership/<int:id>", methods=['GET', 'POST'])
@login_required
def sponsership(id):
    form = SponsershipForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        sponsership = Sponsership(sponser_type=form.sponser_type.data,
                    sponser_name=form.sponser_name.data,
                    sponsership_start_date=form.sponsership_start_date.data,
                    sponsership_end_date=form.sponsership_end_date.data,
                    Protagonist= user)
        db.session.add(sponsership)
        db.session.commit()
        flash('Your Sponsership has been updated sucessfully!', 'success')
        return redirect(url_for('users.user', id=user.id))
    return render_template('sponsership.html', title='Sponsership',
                           form=form, legend='Sponsership'  )



@users.route("/user/<int:id>", methods=['GET', 'POST'])
def user(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(id=id).first_or_404()
    user_id = user.id
    sponsership = Sponsership.query.filter_by(user_id=id).first()
    special_event = Special_event.query.filter_by(user_id=id).first()
    achievement = Achievement.query.filter_by(user_id=id).first()
    intrest = Intrest.query.filter_by(user_id=id).first()
    links = Links.query.filter_by(user_id=id).first()
    languages = Language.query.filter_by(user_id=id).first()
    address = Address.query.filter_by(user_id=id).first()
    occupation = Occupation.query.filter_by(user_id=id).first()     
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    posts = Post.query.filter_by(Protagonist=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user.html', image_file=image_file, posts=posts, user=user, achievement=achievement, sponsership=sponsership, address=address, links=links, occupation=occupation, languages=languages, intrest=intrest, special_event=special_event)





@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)




@users.route('/follow/<int:id>')
@login_required
def follow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash(('User not found','warning'))
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('You are already following this user', 'warning')
        return redirect(url_for('users.home', id=id))
    if user == current_user:
        flash(('You cannot follow yourself!', 'warning'))
        return redirect(url_for('main.home', id=id))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following this user' , 'success' )
    return redirect(url_for('users.user', id=id))




@users.route('/unfollow/<int:id>')
@login_required
def unfollow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash(('User  not found.', 'warning'))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash(('You cannot unfollow yourself!', 'warning'))
        return redirect(url_for('users.home', id=id))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following this user anymore', 'danger'  )
    return redirect(url_for('users.user', id=id))

@users.route('/followers/<int:id>')
def followers(id):
    user = User.query.filter_by(id=username).first()
    if user is None:
        flash('Invalid user', 'warning')
        return redirect(url_for('users.user'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='followers', pagination=pagination,
                           follows=follows)


@users.route('/followed_by/<int:id>')
def followed_by(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('users.user'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='followed_by', pagination=pagination,
                           follows=follows)
