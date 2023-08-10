from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)


class Post(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Unpublished', 'Unpublished')
    )

    name = models.CharField('Title', max_length=80)
    description = models.TextField('Description', null=True)
    photo = models.ImageField('Image', upload_to='photo_post/', null=True, blank=True)
    status = models.CharField('Post status', max_length=200, choices=STATUS_CHOICES, default="Published")
    likes = models.IntegerField('Like', default=0)
    # M2O
    creator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,  # необязательно в БД
        blank=False,  # обязательно в Django
        verbose_name="Post author",
        related_name="posts"  # default == post_set
    )

    category = models.ManyToManyField(
        to='Category',
        blank=True,
        verbose_name='Categories',
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.name} - {self.status}'


class Category(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )

    name = models.CharField('Category', max_length=50)
    rating = models.PositiveSmallIntegerField('Rating', choices=RATING_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} - {self.rating}'


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    comment_text = models.TextField()
    likes_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']

    def __str__(self):
        return self.comment_text[:20]


class Short(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Posted by',
        related_name='short'
    )
    short_file = models.FileField('Short', upload_to='short_file_post/')
    views_qty = models.PositiveIntegerField('Views', default=0)
    created_at = models.DateTimeField('Upload data', auto_now_add=True)

    class Meta:
        verbose_name = 'Short'
        verbose_name_plural = 'Shorts'

    def __str__(self):
        return f'{self.short_file} - {self.created_at}'


class SavedPost(models.Model):
    user = models.OneToOneField(verbose_name='User', to=User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, verbose_name='saved post', related_name='saved_post')

    class Meta:
        verbose_name = 'saved post'
        verbose_name_plural = 'saved posts'

    def __str__(self):
        return f'{self.user}'







