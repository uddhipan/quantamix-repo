from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app, make_response)
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from ttb import db
from ttb.models import Post, User, Comment
from ttb.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

@posts.route("/post/<int:id>", methods=['GET', 'POST'])
@login_required
def new_post(id):
    form = PostForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        post = Post(city=form.city.data,
                    category=form.category.data,
                    story_line=form.story_line.data,
                    story_text=form.story_text.data,
                    youtube_link=form.youtube_link.data,
                    Protagonist= user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/postn/<int:post_id>",  methods=['GET', 'POST'])
def postn(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          Protagonist=current_user._get_current_object() )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(url_for('posts.postn', post_id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    return render_template('post.html', story_line=post.story_line, posts=[post],post=post, form=form,
                              comments=comments, pagination=pagination)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.city = form.city.data
        post.category = form.category.data
        post.story_line = form.story_line.data
        post.story_text = form.story_text.data
        post.youtube_link = form.youtube_link.data
        db.session.commit()
        flash(' post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.city.data = post.city
        form.category.data = post.category
        form.story_line.data = post.story_line
        form.story_text.data = post.story_text
        form.youtube_link.data = post.youtube_link
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required

def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('  post has been deleted!', 'success')
    return redirect(url_for('main.home'))
