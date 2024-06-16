from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.AIMS.login_management import role_required
from app.models import Post, Comment
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length
from app import db

rental_information_exchange = Blueprint('rental_information_exchange', __name__)

@rental_information_exchange.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # 每頁顯示的最大文章數量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items
    return render_template('RIMS/forum.html', posts=posts, pagination=pagination)

@rental_information_exchange.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()

    if request.method == 'POST':
        content = request.form['commentContent']
        new_comment = Comment(text=content, user_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('rental_information_exchange.post', post_id=post_id))
    return render_template('RIMS/post.html', post=post, comments=comments)

@rental_information_exchange.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            text=form.text.data,
            image_urls=form.image_urls.data,
            user_id=current_user.id  # 假設你有使用 Flask-Login 並且 current_user 已經登錄
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('rental_information_exchange.index'))  # 假設你有一個 index 視圖
    return render_template('RIMS/newpost.html', form=form)


@rental_information_exchange.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    post = Post.query.get_or_404(post_id)

    # 確保當前用戶是文章的作者
    if current_user.id != post.user_id:
        flash('You are not authorized to edit this post', 'danger')
        return redirect(url_for('rental_information_exchange.post', post_id=post_id))

    form = EditPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('rental_information_exchange.post', post_id=post_id))
    
    # 預填充表單字段
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text

    return render_template('RIMS/editpost.html', form=form, post=post)

class PostForm(FlaskForm):
    title = StringField('文章標題', validators=[DataRequired(), Length(max=50)])
    text = TextAreaField('文章內容', validators=[DataRequired()])
    image_urls = TextAreaField('圖檔路徑', validators=[Length(max=200)])
    submit = SubmitField('新增')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    text = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')