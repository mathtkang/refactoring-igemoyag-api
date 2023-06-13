from django.db import models
from django.contrib.auth.models import AbstractUser

from pills.models import Pill
from common.models import CommonModel


"""
[AbstractUser에서 기본적으로 제공하는 필드]
* id (pk, not null, int)
* username (not null, char)
* email (char-emailField)
* password (not null)
* last_login (not null, dateTime)
* date_joined (not null, dateTime)
"""


class User(AbstractUser):
    """User model Definition"""

    email = models.EmailField(
        verbose_name="email",
        max_length=256,
        unique=True,
    )
    username = models.CharField(
        max_length=128,
        unique=True,
    )


class Favorite(models.Model):
    """before name is UserPill"""
    """
    - User's Favorite model Definition
    - 'User' and 'Pill' connection model
    """
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="favorite",
    )
    pill = models.ForeignKey(
        "pills.Pill",
        on_delete=models.CASCADE,
        related_name="favorite",
    )


class SearchHistory(CommonModel):
    """
    - User's search history model Definition
    - 'User' and 'Pill' connection model
    """
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="search_history",
    )
    pill = models.ForeignKey(
        "pills.Pill",
        on_delete=models.CASCADE,
        related_name="search_history",
    )