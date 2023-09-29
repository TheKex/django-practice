from django.contrib import admin

from .models import Article, Scope, Tag


class ScopesInline(admin.TabularInline):
    model = Scope
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at"]
    inlines = (ScopesInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = (ScopesInline,)
