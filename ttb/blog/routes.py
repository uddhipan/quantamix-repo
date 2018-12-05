from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app, make_response)
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from ttb import db
from ttb.models import Blog, User, BlogComment
from ttb.blog.forms import BlogForm, BlogCommentForm
from datetime import datetime

blog = Blueprint('blog', __name__)

@blog.route("/blogview")
def blog_view():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.blog_date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('blogview.html', blogs=blogs, current_time=datetime.utcnow())


@blog.route("/blog/<int:id>", methods=['GET', 'POST'])
@login_required
def new_blog(id):
    form = BlogForm()
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        blog = Blog(blog_city=form.blog_city.data,
                    blog_category=form.blog_category.data,
                    blog_story_line=form.blog_story_line.data,
                    blog_story_text=form.blog_story_text.data,
                    blog_youtube_link=form.blog_youtube_link.data,
                    blog_author= user)
        db.session.add(blog)
        db.session.commit()
        flash('Your blog post has been created and it will be reviewed by a moderator!', 'success')
        return redirect(url_for('blog.blog_view'))
    return render_template('create_blog.html', title='New Blog',
                           form=form, legend='New Blog')


@blog.route("/blogn/<int:blog_id>",  methods=['GET', 'POST'])
def blogn(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    form = BlogCommentForm()
    if form.validate_on_submit():
        blogcomment = BlogComment(body=form.body.data,
                          blog=blog,
                          blog_author=current_user._get_current_object() )
        db.session.add(blogcomment)
        db.session.commit()
        flash('Your blog comment has been published.', 'success')
        return redirect(url_for('blog.blogn', blog_id=blog.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (blog.blogcomments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = blog.blogcomments.order_by(BlogComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    blogcomments = pagination.items

    return render_template('blog.html', blog_story_line=blog.blog_story_line, blogs=[blog],blog=blog, form=form,
                              blogcomments=blogcomments, pagination=pagination)


@blog.route("/blog/<int:blog_id>/update", methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.blog_city = form.blog_city.data
        blog.blog_category = form.blog_category.data
        blog.blog_story_line = form.blog_story_line.data
        blog.blog_story_text = form.blog_story_text.data
        blog.blog_youtube_link = form.blog_youtube_link.data
        db.session.commit()
        flash(' Blog post has been updated!', 'success')
        return redirect(url_for('blog.blogn', blog_id=blog.id))
    elif request.method == 'GET':
        form.blog_city.data = blog.blog_city
        form.blog_category.data = blog.blog_category
        form.blog_story_line.data = blog.blog_story_line
        form.blog_story_text.data = blog.blog_story_text
        form.blog_youtube_link.data = blog.blog_youtube_link
    return render_template('create_blog.html', title='Update Blog',
                           form=form, legend='Update Blog')


@blog.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required

def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog post has been deleted!', 'success')
    return redirect(url_for('blog.blog_view'))
