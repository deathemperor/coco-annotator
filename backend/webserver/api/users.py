from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restplus import Namespace, Resource, reqparse

from database import UserModel
from config import Config
from ..util.query_util import fix_ids
from ..util.pagination_util import Pagination

import logging
import datetime
logger = logging.getLogger('gunicorn.error')

api = Namespace('user', description='User related operations')

register = reqparse.RequestParser()
register.add_argument('username', required=True, location='json')
register.add_argument('password', required=True, location='json')
register.add_argument('email', location='json')
register.add_argument('name', location='json')

login = reqparse.RequestParser()
login.add_argument('password', required=True, location='json')
login.add_argument('username', required=True, location='json')

set_password = reqparse.RequestParser()
set_password.add_argument('password', required=True, location='json')
set_password.add_argument('new_password', required=True, location='json')

user_stats = reqparse.RequestParser()
user_stats.add_argument('start_date', required=True)
user_stats.add_argument('end_date', required=True)

user_images = reqparse.RequestParser()
user_images.add_argument('date', required=False)
user_images.add_argument('status', required=False)

page_data = reqparse.RequestParser()
page_data.add_argument('page', default=1, type=int)
page_data.add_argument('limit', default=20, type=int)

@api.route('/')
class User(Resource):
    @login_required
    def get(self):
        """ Get information of current user """
        if Config.LOGIN_DISABLED:
            return current_user.to_json()

        user_json = fix_ids(current_user)
        del user_json['password']

        return {'user': user_json}


@api.route('/password')
class UserPassword(Resource):

    @login_required
    @api.expect(register)
    def post(self):
        """ Set password of current user """
        args = set_password.parse_args()

        if check_password_hash(current_user.password, args.get('password')):
            current_user.update(password=generate_password_hash(args.get('new_password'), method='sha256'), new=False)
            return {'success': True}

        return {'success': False, 'message': 'Password does not match current passowrd'}, 400


@api.route('/register')
class UserRegister(Resource):
    @api.expect(register)
    def post(self):
        """ Creates user """

        users = UserModel.objects.count()

        if not Config.ALLOW_REGISTRATION and users != 0:
            return {'success': False, 'message': 'Registration of new accounts is disabled.'}, 400

        args = register.parse_args()
        username = args.get('username')

        if UserModel.objects(username__iexact=username).first():
            return {'success': False, 'message': 'Username already exists.'}, 400

        user = UserModel()
        user.username = args.get('username')
        user.password = generate_password_hash(args.get('password'), method='sha256')
        user.name = args.get('name')
        user.email = args.get('email')
        if users == 0:
            user.is_admin = True
        user.save()

        login_user(user)

        user_json = fix_ids(current_user)
        del user_json['password']

        return {'success': True, 'user': user_json}


@api.route('/login')
class UserLogin(Resource):
    @api.expect(login)
    def post(self):
        """ Logs user in """
        args = login.parse_args()
        username = args.get('username')

        user = UserModel.objects(username__iexact=username).first()
        if user is None:
            return {'success': False, 'message': 'Could not authenticate user'}, 400

        if check_password_hash(user.password, args.get('password')):
            login_user(user)

            user_json = fix_ids(current_user)
            del user_json['password']
            
            logger.info(f'User {current_user.username} has LOGIN')

            return {'success': True, 'user': user_json}

        return {'success': False, 'message': 'Could not authenticate user'}, 400


@api.route('/logout')
class UserLogout(Resource):
    @login_required
    def get(self):
        """ Logs user out """
        logger.info(f'User {current_user.username} has LOGOUT')
        logout_user()
        return {'success': True}

@api.route('/stats')
class UserImages(Resource):
    def get(self):
        users = UserModel.objects().only('id', 'username', 'name', 'online', 'is_admin', 'last_seen').all()
        
        stats = []
        for user in users:
            user['completed_images_total'] = user.images.filter(
                                annotated=True,
                                status__completed=True,
                                status__completedBy=user.id).count()
            user['verified_images_total'] = user.images.filter(
                                annotated=True,
                                status__verified=True,
                                status__completedBy=user.id).count()
            user['rejected_images_total'] = user.images.filter(
                                annotated=True,
                                status__rejected=True,
                                status__completedBy=user.id).count()
            stats.append(fix_ids(user))
        
        return stats

@api.route('/<string:username>/stats')
class UserStats(Resource):
    def get(self, username):
        user = UserModel.objects(username=username).only('id', 'name', 'username', 'is_admin', 'last_seen').first()
        if user is None:
            return {'success': False, 'message': 'Could not find user'}, 404
        
        args = user_stats.parse_args()
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        images = user.images.filter(
          annotated=True,
          # status__completed=True,
          status__completedBy=user.id,
          status__completedDate__gte=start,
          status__completedDate__lte=end)

        user['stats'] = {}
        for image in images:
          day = image.status['completedDate'].strftime('%Y%m%d')
          if not day in user['stats']:
            user['stats'][day] = {
              'completedCount': 0,
              'verifiedCount': 0,
              'rejectedCount': 0,
              'day': image.status['completedDate'].strftime('%Y-%m-%d')
            }
          if image.status['completedDate']:
            user['stats'][day]['completedCount'] += 1
          if 'verifiedDate' in image.status:
            user['stats'][day]['verifiedCount'] += 1
          if 'rejectedDate' in image.status:
            user['stats'][day]['rejectedCount'] += 1

        # user.images.filter(annotated=True, status__completed=True, status__completedBy=user.id)

        return fix_ids(user)

@api.route('/<string:username>/images')
class UserImages(Resource):
    def get(self, username):
        args = user_images.parse_args()
        date = args.get('date')
        status = args.get('status')
        if status is None:
          status = 'completed'
        logger.info(status)

        args = page_data.parse_args()
        limit = args['limit']
        page = args['page']

        user = UserModel.objects(username=username).first()
        if user is None:
            return {'success': False, 'message': 'Could not find user'}, 404
        
        if date:
            start = datetime.datetime.strptime(date, '%Y-%m-%d')
            end = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=1)
            images = user.images.filter(
                      annotated=True,
                      # status__completed=True,
                      status__rejected=True,
                      status__completedBy=user.id,
                      status__completedDate__gte=start,
                      status__completedDate__lte=end
                    ).only(
                      'id', 'dataset_id', 'path', 'file_name', 'annotating', 'annotated', 'num_annotations', 'status'
                    )
        else:
            images = user.images.filter(
                annotated=True,
                # status__completed=True, 
                status__completedBy=user.id,
                **{'{}__{}'.format('status' , status): True}
              ).only(
                'id', 'dataset_id', 'path', 'file_name', 'annotating', 'annotated', 'num_annotations', 'status'
              )
        pagination = Pagination(len(images), limit, page)
        images = fix_ids(images[pagination.start:pagination.end])
        return {
            "pagination": pagination.export(),
            "page": page,
            "images": images
        }