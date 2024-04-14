from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.db import models

from apps.blogApp.models import BlogCategory, CommentModel, ReactionModel,BlogModel
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_filter = ('category_name',)
    search_fields = ('category_name',)

admin.site.register(BlogCategory,CategoryAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','get_categories','getAuthorUsername')
    list_filter = ('category','author','last_updated')
    search_fields = ('title','category','author')

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


    def get_categories(self,obj):
        return ', '.join([category.category_name for category in obj.category.all()])
    get_categories.short_description = 'Categories'

    
    def getAuthorUsername(self,obj):
        return obj.author.user.username
    getAuthorUsername.short_description = 'Author'


admin.site.register(BlogModel,BlogAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('getPersonUsername','getBlogCommented','comment','date_commented')
    list_filter = ('blog',)
    search_fields = ('blog',)


    def getPersonUsername(self,obj):
        return obj.person.user.username
    getPersonUsername.short_description = 'Person'

    def getBlogCommented(self,obj):
        return obj.blog.title
    getBlogCommented.short_description = 'Blog Commented'



admin.site.register(CommentModel,CommentAdmin)


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('getPersonUsername','getBlogReacted','reaction','date_reacted')
    list_filter = ('reaction',)
    search_fields = ('blog',)


    def getPersonUsername(self,obj):
        return obj.person.user.username
    getPersonUsername.short_description = 'Person'

    def getBlogReacted(self,obj):
        return obj.blog.title
    getBlogReacted.short_description = 'Blog Reacted'


admin.site.register(ReactionModel,ReactionAdmin)
