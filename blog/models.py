from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, null=False, unique=True)
    body = models.TextField()
    pub_date = models.DateField(auto_now=False, null=False, auto_now_add=False)
    published = models.BooleanField()
    slug = models.CharField(max_length=200, null=False, unique=True)

    def __unicode__(self):
        return self.title
