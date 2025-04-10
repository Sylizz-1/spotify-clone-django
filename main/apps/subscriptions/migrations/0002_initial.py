# Generated by Django 5.1.6 on 2025-03-21 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptionmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_subscriptions', to='subscriptions.subscriptionplan'),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptionmember',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='subscriptions.usersubscription'),
        ),
        migrations.AddField(
            model_name='paymenttransaction',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='subscriptions.usersubscription'),
        ),
        migrations.AlterUniqueTogether(
            name='subscriptionmember',
            unique_together={('subscription', 'user')},
        ),
    ]
