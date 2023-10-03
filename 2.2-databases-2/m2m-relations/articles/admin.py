from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopesInlineFormset(BaseInlineFormSet):
    def clean(self):
        total_main_tags = 0
        for form in self.forms:
            total_main_tags += form.cleaned_data.get('is_main', 0)
            if total_main_tags > 1:
                raise ValidationError('Допустим только один основной тег')
        return super().clean()


class ScopesInline(admin.TabularInline):
    model = Scope
    formset = ScopesInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at"]
    inlines = (ScopesInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = (ScopesInline,)
