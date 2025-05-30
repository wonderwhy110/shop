# Generated by Django 4.1.13 on 2025-04-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField(max_length=200)),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='shop_produc_id_f21274_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='shop_produc_name_a2070e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created'], name='shop_produc_created_ef211c_idx'),
        ),
        migrations.AddIndex(
            model_name='reg',
            index=models.Index(fields=['username'], name='shop_reg_usernam_d9673f_idx'),
        ),
    ]
