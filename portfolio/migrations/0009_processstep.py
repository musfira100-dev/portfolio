from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_faq_defaults'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('icon', models.CharField(blank=True, help_text='Ek emoji, jaise 🧭 (khali chhodein to step ka number dikhega)', max_length=8)),
                ('points', models.TextField(blank=True, help_text='Optional. Har line mein ek point likhein.')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Process step',
                'verbose_name_plural': 'Process steps',
                'ordering': ['order', 'id'],
            },
        ),
    ]