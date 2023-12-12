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


class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=256)
    contents = models.CharField(null=False, max_length=2048)
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
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(null=False, max_length=512)
    reply_to = models.ForeignKey("ArticleComment", null=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def to_dict(self):
        return {
            'id': self.id,
            'article': self.article.to_dict(),
            'belongs_to': self.belongs_to.to_dict(),
            'comment': self.comment,
            'reply_to': self.reply_to.to_dict(),
            'created_at': self.created_at
        }
