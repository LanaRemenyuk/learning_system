from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DateTimeField
from django.db.models.deletion import CASCADE


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
        help_text='Specify your email'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Name',
        help_text='1st name required'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last_name',
        help_text='2nd name required'
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Product name',
                            help_text='Specify your product name', )
    owner = models.ForeignKey(
        related_name='products',
        to=CustomUser,
        on_delete=CASCADE,
        verbose_name='Product owner',
        help_text='Specify the product owner'
    )
    subscriber = models.ManyToManyField(CustomUser,
                                        verbose_name='Subscriber',)
    description = models.TextField(
        verbose_name='Product description',
        help_text='Describe the product', )
    access_key = models.CharField(
        max_length=150,
        verbose_name='Secret key',
        help_text='Secret key required'
    )
    pub_date = DateTimeField(
        verbose_name='Pub date',
        auto_now_add=True,
    )


    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    product = models.ManyToManyField(Product, related_name="lessons",
                                verbose_name='Product',
                                help_text='Specify the product name'
                                    )
    name = models.CharField(max_length=200,
                            verbose_name='Lesson name',
                            help_text='Specify this lesson name', )
    link = models.URLField(
        max_length=128,
        db_index=True,
        unique=True,
    )
    duration = models.DurationField()
    pub_date = DateTimeField(
        verbose_name='Pub date',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Watched(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='watched',
        verbose_name='User'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='watched',
        verbose_name='Lesson'
    )
    time = models.DurationField()
    if_watched = models.BooleanField()
    last_watched = models.DateTimeField()

    def __str__(self):
        return self.lesson.name





