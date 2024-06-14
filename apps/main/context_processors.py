
# Context processors
def is_user_authenticated(request):
    return {'is_user_authenticated': request.user.is_authenticated}
