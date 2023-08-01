#from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
#class Profile(models.Model):
#    user = models.OneToOneField(
#        to=User,
#        on_delete=models.CASCADE
#    )
#    nickname = models.CharField(max_length=55)
#    description = models.TextField(null=True, blank=True)

from django.db import models

class Post(models.Model):
    STATUS_CHOICES = (('Published', 'Published'),
                      ('Unpublished', 'Unpublished'))

    name = models.CharField('Заголовок', max_length=80, null=True, blank=True)
    description = models.TextField('Описание', null=True)
    fhoto = models.ImageField('Фотография', upload_to='photo_post/', null=True, blank=True)
    status = models.CharField('Статус публикации', max_length=200, choices=STATUS_CHOICES)


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
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} - {self.rating}'


