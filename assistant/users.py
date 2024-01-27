from django.contrib.auth.models import User


# Create user and save to the database
def create_user():
    user = User.objects.create_user('266640', '266640@email.com', 'mypassword')

    # Update fields and then save again
    user.first_name = 'Kacper'
    user.last_name = 'Bartoha'
    user.save()


def get_user(request, id : str = '266640'):
    if not User.objects.filter(username=id).exists():
        create_user()
    return User.objects.get(username=id)
