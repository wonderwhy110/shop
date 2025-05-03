from django.contrib import admin

# Register your models here.
from .models import Category, Product

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Reg  # Импортируйте вашу модель

# Для отображения всех пользователей (и staff, и обычных)
class RegAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Reg, RegAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
 list_display = ['name', 'slug']
 prepopulated_fields = {'slug': ('name',)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display = ['name', 'slug', 'price',
 'available', 'created', 'updated']
 list_filter = ['available', 'created', 'updated']
 list_editable = ['price', 'available']
 prepopulated_fields = {'slug': ('name',)}