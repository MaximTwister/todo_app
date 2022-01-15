from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_edit_date', models.DateTimeField(auto_now=True)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_todo_items', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self_todo_items', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='todo_items', to='todo_app.Tag')),
            ],
            options={
                'db_table': 'todo_item',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('telegram_id', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('usr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='account', serialize=False, to='auth.user')),
                ('group', models.ManyToManyField(blank=True, null=True, related_name='accounts', to='todo_app.Group')),
            ],
        ),
    ]
