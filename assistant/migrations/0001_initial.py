# Generated by Django 5.0.1 on 2024-01-23 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentEdition',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('academic_year', models.CharField(max_length=15)),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FieldOfStudies',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('average', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UniWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('ECTS', models.IntegerField()),
                ('course_type', models.CharField(choices=[('Lec', 'Lecture'), ('Pra', 'Practicals'), ('Lab', 'Laboratory'), ('Pro', 'Project'), ('Sem', 'Seminary')], default='Lec', max_length=3)),
                ('course_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assistant.coursegroup')),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentedition')),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('succeeded', models.BooleanField(default=False)),
                ('enrollment_record_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_from_set', to='assistant.enrollmentrecord')),
                ('enrollment_record_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exchange_to_set', to='assistant.enrollmentrecord')),
            ],
        ),
        migrations.AddField(
            model_name='enrollmentedition',
            name='field_of_studies',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.fieldofstudies'),
        ),
        migrations.CreateModel(
            name='GridModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentedition')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('code', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('week_type', models.CharField(choices=[('every', 'Every week'), ('odd', 'Odd week'), ('even', 'Even week')], default='every', max_length=5)),
                ('day_of_week', models.CharField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fr', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='mon', max_length=3)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('building', models.CharField(max_length=30)),
                ('hall', models.CharField(max_length=30)),
                ('available_seats', models.IntegerField(default=16)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.course')),
                ('enrollment_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentedition')),
            ],
        ),
        migrations.AddField(
            model_name='enrollmentrecord',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.group'),
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=0)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.basket')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.group')),
            ],
        ),
        migrations.CreateModel(
            name='EnrollmentPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_permitted', models.BooleanField(default=False)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('is_permitted_earlier', models.BooleanField(default=False)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentqueue')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.student')),
            ],
        ),
        migrations.AddField(
            model_name='basket',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.student'),
        ),
        migrations.CreateModel(
            name='Studying',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_of_study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.fieldofstudies')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.student')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentedition')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.student')),
            ],
        ),
        migrations.AddField(
            model_name='enrollmentrecord',
            name='timetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.timetable'),
        ),
        migrations.CreateModel(
            name='QueueModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.enrollmentqueue')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.uniworker')),
            ],
        ),
    ]
