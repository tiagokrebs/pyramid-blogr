from pyramid.view import view_config
from ..models.services.blog_record import BlogRecordService
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models.services.user import UserService
from ..forms import RegistrationForm
from ..models.meta import DBSession
from ..models.user import User

@view_config(route_name='home', renderer='pyramid_blogr:templates/index.mako')
def index_page(request):
    return {}

@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)

@view_config(route_name='home', renderer='pyramid_blogr:templates/index.mako')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = BlogRecordService.get_paginator(request, page)
    return {'paginator': paginator}

@view_config(route_name='register', renderer='pyramid_blogr:templates/register.mako')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User()
        new_user.name = form.username.data
        new_user.set_password(form.password.data.encode('utf8'))
        DBSession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}