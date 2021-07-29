from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["headline", "short_description", "description", "image", "blank", "user"]


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["username", "text", "is_published", "post"]
    actions = ['make_published']

    @admin.action(description='Publish comment')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
