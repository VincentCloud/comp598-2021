login_url = "/login"


def get_user(request):
    username = request.get_argument('username')
    password = request.get_argument('password')

    if username == 'nyc' and password == 'iheartnyc':
        return 1

    return None
