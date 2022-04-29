from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import validate_slug
from .validators import year_validator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True,
                           verbose_name="biography",
                           )

    role = models.CharField(
        max_length=20,
        choices=ROLE,
        default=USER,
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name="categories")
    slug = models.SlugField(unique=True,
                            max_length=50,
                            blank=True,
                            null=True,
                            validators=[validate_slug])

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True,
                            verbose_name="genres")
    slug = models.SlugField(unique=True,
                            max_length=50,
                            blank=True,
                            null=True,
                            validators=[validate_slug])

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Genres'
        verbose_name = 'Genre'


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name="title",
                            )
    year = models.IntegerField(validators=[year_validator],
                               db_index=True)
    description = models.TextField(blank=True, default='не заполнено')
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Titles'
        verbose_name = 'Title'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('publication date', auto_now=True)

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('publication date', auto_now=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ('-pub_date',)
