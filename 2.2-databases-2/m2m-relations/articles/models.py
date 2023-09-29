from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег', related_name='scopes')
    is_main = models.BooleanField(verbose_name='Основной')

    class Meta:
        ordering = ('-is_main', 'tag__name')
        constraints = [
            models.UniqueConstraint(
                fields=['article'],
                condition=models.Q(is_main=True),
                name='unique_article_main_tag'
            ),
        ]
