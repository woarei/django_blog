# Generated by Django 2.0.3 on 2019-06-28 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='娃哈哈店长的个人技术博客，django_blog，django2.0+python3技术搭建。', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(default='娃哈哈店长的个人技术博客，django_blog，django2.0+python3技术搭建。', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
    ]
