from django.contrib.auth.models import User
from django.db import transaction


@transaction.atomic
def register_user(*, username, password, email=""):
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
