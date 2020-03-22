# Generated by Django 3.0.4 on 2020-03-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewalletapp', '0008_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='static/css/profile_pic.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='jio',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vodafone',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
