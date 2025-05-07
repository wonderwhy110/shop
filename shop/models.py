from django.utils import timezone


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.hashers import make_password
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

from django.conf import settings



# Create your models here.
class Category(models.Model):

     name = models.CharField(max_length=200)
     slug = models.SlugField(max_length=200,
     unique=True)
     class Meta:
         ordering = ['name']
         indexes = [
         models.Index(fields=['name']),
         ]
         verbose_name = 'category'
         verbose_name_plural = 'categories'
     def __str__(self):
         return self.name

     def get_absolute_url(self):
         return reverse('shop:product_list_by_category',
                        args=[self.slug])


class Product(models.Model):
    # Поля модели
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='products_liked',
        blank=True
    )

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]


    def __str__(self):
        return self.name







class Reg(AbstractUser):
    # Дополнительные поля, если нужны
    pass

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'