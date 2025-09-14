from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_LENGTH, MAX_LENGTH_TITLE, MAX_LENGTH_NAME

User = get_user_model()


class TimeStampedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:MAX_LENGTH_TITLE]


class Location(TimeStampedModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_LENGTH_NAME]


class Post(TimeStampedModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField(
        upload_to="posts/",
        verbose_name="Изображение",
        help_text="Загрузите изображение для публикации",
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:MAX_LENGTH_TITLE]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
        verbose_name='Добавлено',
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'коментарий'

    def __str__(self):
        return self.text[:MAX_LENGTH_TITLE]
