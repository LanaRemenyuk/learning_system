from django.contrib import admin
from .models import CustomUser, Lesson, Product, Watched


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email")
    search_fields = ("email", "username")
    list_filter = ("email", "username")
    empty_value_display = "-пусто-"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "link", "duration", "pub_date")
    search_fields = ("name",)
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "owner","description", "pub_date", "access_key")
    search_fields = ("name",)
    list_filter = ('name',)
    filter_horizontal = ('subscriber',)

    def amount_lessons(self, obj):
        return Lesson.objects.filter(product=obj).count()


@admin.register(Watched)
class WatchedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'time', 'if_watched', )
    search_fields = ('user', 'lesson')
    list_filter = ('user',)

