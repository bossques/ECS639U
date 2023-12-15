from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField(unique=True, max_length=128)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(AbstractUser):
    profile_image = models.ImageField(null=True)
    date_of_birth = models.DateField(default=now)
    email = models.EmailField(unique=True)
    favourite_categories = models.ManyToManyField(ArticleCategory, related_name="favourite_by", default=[])

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_image': str(self.profile_image) if self.profile_image else None,
            'date_of_birth': self.date_of_birth,
            'favourite_categories': list(self.favourite_categories.values('id', 'name'))
        }


class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=256)
    contents = models.CharField(null=False, max_length=4096)
    created_at = models.DateTimeField(default=now)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category.to_dict(),
            'title': self.title,
            'contents': self.contents,
            'created_at': self.created_at
        }


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment = models.CharField(null=False, max_length=512)
    reply_to = models.ForeignKey("ArticleComment", null=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def to_dict(self, exclude_article: bool = True):
        data = {
            'id': self.id,
            'belongs_to': self.belongs_to.to_dict(),
            'comment': self.comment,
            'reply_to': self.reply_to.to_dict() if self.reply_to else None,
            'created_at': self.created_at
        }
        if not exclude_article:
            data['article'] = self.article.to_dict()

        return {key: value for key, value in data.items() if value is not None}
