from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required
from flask_smorest import Blueprint, abort
from freenit.api.methodviews import MethodView
from freenit.schemas.paging import PageInSchema, paginate

from ..models.blog import Blog
from ..models.user import User
from ..schemas.blog import BlogPageOutSchema, BlogSchema

from werkzeug.utils import secure_filename
from flask import request, current_app, send_from_directory, url_for
import os
import socket

blueprint = Blueprint('blogs', 'blogs')

@blueprint.route('', endpoint='list')
class BlogListAPI(MethodView):
    @jwt_optional
    @blueprint.arguments(PageInSchema(), location='headers')
    @blueprint.response(BlogPageOutSchema)
    def get(self, pagination):
        """List blog posts"""
        user_id = get_jwt_identity()
        if user_id is None:
            query = Blog.select().where(Blog.published)
        else:
            query = Blog.select()
        return paginate(query, pagination)

    @jwt_required
    @blueprint.arguments(PageInSchema(), location='headers')
    @blueprint.arguments(BlogSchema)
    @blueprint.response(BlogPageOutSchema)
    def post(self, pagination, args):
        """Create blog post"""
        blog = Blog(**args)
        blog.date = datetime.utcnow()
        user_id = get_jwt_identity()
        try:
            user = User.get()
        except User.DoesNotExist:
            abort(404, message='User not found')
        try:
            Blog.find(
                blog.date.year,
                blog.date.month,
                blog.date.day,
                blog.slug,
            )
            abort(409, message='Post with the same title already exists')
        except Blog.DoesNotExist:
            blog.author = user
            blog.save()

        if user_id is None:
            query = Blog.select().where(Blog.published)
        else:
            query = Blog.select()

        return paginate(query, pagination)


@blueprint.route('/<year>/<month>/<day>/<slug>', endpoint='detail')
class BlogAPI(MethodView):
    @blueprint.response(BlogSchema)
    def get(self, year, month, day, slug):
        """Get blog post details"""
        try:
            blog = Blog.find(year, month, day, slug)
        except Blog.DoesNotExist:
            abort(404, message='No such blog')
        except ValueError:
            abort(409, message='Multiple blogs found')
        return blog

    @jwt_required
    @blueprint.arguments(BlogSchema(partial=True))
    @blueprint.response(BlogSchema)
    def patch(self, args, year, month, day, slug):
        """Edit blog post details"""
        try:
            blog = Blog.find(year, month, day, slug)
        except Blog.DoesNotExist:
            abort(404, message='No such blog')
        except ValueError:
            abort(409, message='Multiple blogs found')
        for field in args:
            setattr(blog, field, args[field])
        blog.save()
        return blog

    @jwt_required
    @blueprint.response(BlogSchema)
    def delete(self, year, month, day, slug):
        """Delete blog post"""
        try:
            blog = Blog.find(year, month, day, slug)
        except Blog.DoesNotExist:
            abort(404, message='No such blog')
        except ValueError:
            abort(409, message='Multiple blogs found')
        blog.delete_instance()
        return blog


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png',
                              'jpg',
                              'jpeg',
                              'gif',
                              'svg'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('images/<path>', endpoint='detail')
class BlogAPI(MethodView):
    def get(self, path):
        directory = current_app.config['PROJECT_ROOT']+'/static/images/blog/'
        return send_from_directory(filename=path,
                            directory=directory)

@blueprint.route('/images', endpoint='upload_thumbnail')
class BlogAPI(MethodView):

    def post(self):
        """Upload an image for the blog"""
        if 'file' not in request.files:
            abort(400, message='File not attached in request.')

        file = request.files['file']

        if file.filename == '':
            abort(400, message='File empty in request.')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_path = current_app.config['PROJECT_ROOT']
            path = f'{base_path}/static/images/blog'

            hostname = socket.gethostname()

            file.save(os.path.join(path, filename))

            if current_app.config['DEBUG'] == True:
                return {'link': f'http://localhost:5000/api/v0/blogs/images/{filename}'}

            return {'link': f'{hostname}/api/v0/blogs/images/{filename}'}
        else:
            abort(400, message='File not valid in request.')
