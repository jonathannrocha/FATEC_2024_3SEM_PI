
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True)),
                ('gmail', models.EmailField(max_length=100, unique=True)),
                ('telefone', models.CharField(max_length=15)),
                ('dataNascimento', models.DateField(blank=True, null=True)),
                ('typeUser', models.CharField(choices=[('admin', 'Admin'), ('mentor', 'Mentor'), ('mentorado', 'Mentorado')], default='mentorado', max_length=10)),
            ],
        ),
    ]