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
    STATUS_CHOICES = (('Published', 'Published'),
                      ('Unpublished', 'Unpublished'))

    name = models.CharField('Заголовок', max_length=80, null=True, blank=True)
    description = models.TextField('Описание', null=True)
    photo = models.ImageField('Фотография', upload_to='photo_post/', null=True, blank=True)
    status = models.CharField('Статус публикации', max_length=200, choices=STATUS_CHOICES, default="Published")
    likes = models.PositiveIntegerField('Лайки', default = 0)
    # M2O
    creator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True, # необязательно в БД
        blank=False, # обязательно в Django
        verbose_name="Автор поста",
        related_name="posts" # default == post_set
    )

    category = models.ManyToManyField(
        to='Category',
        blank=True,
        verbose_name='Категории',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

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

    name = models.CharField('Категория', max_length=50, null=True, blank=True)
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return self.comment_text[:20]


class Short(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    short_file = models.FileField('Short', upload_to='video_post/', null=True, blank=True)
    views_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Short'
        verbose_name_plural = 'Shorts'

    def __str__(self):
        return self.short_file


class SavedPost(models.Model):
    user = models.OneToOneField(verbose_name='User', to=User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, verbose_name='Saved post', related_name='saved_post')

    class Meta:
        verbose_name = 'Saved post'
        verbose_name_plural = 'Saved posts'

    def __str__(self):
        return f'{self.user} - {self.post}'







