from django.db import models
import uuid


# class Oauth(models.Model):

#     """OAuth2 Model Definition"""
#     # ref. About Composite Primary Keys, PostgreSQL and Django
#     #   - https://www.crunchydata.com/blog/composite-primary-keys-postgresql-and-django
#     #   - https://everyevery-blog.tumblr.com/post/29123180487/django-orm%EC%97%90%EC%84%9C-composite-primary-key-%EC%82%AC%EC%9A%A9

#     # [question] uuidfield
#     uid = models.UUIDField(
#         # primary_key=True, 
#         default=uuid.uuid4,
#         editable=False,
#         unique=False,
#         max_length=128,
#     )
#     provider_type = models.CharField(
#         # primary_key=True,
#         unique=False,
#         max_length=128,
#     )
#     user = models.ForeignKey(
#         "users.User",
#         on_delete=models.CASCADE,
#         related_name="oauth",
#     )
    
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["uid", "provider_type"],
#                 name="unique_OAuth2_as_uid_and_provider_type"
#             )
#         ]
#     # ref. UniqueConstraint: https://docs.djangoproject.com/en/3.2/ref/models/constraints/#uniqueconstraint
#     # ref. About related_name: https://velog.io/@brighten_the_way/Django%EC%99%80-Reverse-relations%EA%B3%BC-Relatedname