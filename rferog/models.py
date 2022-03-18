from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class Post(models.Model):
    votes = models.IntegerField()
    title = models.TextField()
    author = models.CharField(max_length=100)
    content = models.TextField()
    parent_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)

class Comment(models.Model):
    parent_comment_id = models.CharField(max_length=100, null=True)
    content = models.TextField()
    author = models.CharField(max_length=100)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ('id',)
