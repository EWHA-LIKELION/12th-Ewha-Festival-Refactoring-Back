# Generated by Django 5.1.1 on 2024-09-26 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='event_type',
            field=models.CharField(blank=True, choices=[('ewhagreenFe', '다시 돌아온 네가 그린 그린은 이화그린'), ('artistShow', '아티스트 공연'), ('movie_fe', '야간 영화제'), ('nightMarket', '야시장'), ('tugOfWar', '줄다리기'), ('riceFe', '이화인한솥밥배부')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
