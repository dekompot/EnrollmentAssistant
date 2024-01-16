import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} {self.name}"

    def __repr__(self):
        return f"{self.title} {self.name}"


class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    average = models.FloatField(default=0)


class UniWorker(models.Model):
    name = models.CharField(max_length=50)


class FieldOfStudies(models.Model):
    name = models.CharField(max_length=30)


class Studying(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)


# siatka zajec
class EnrollmentEdition(models.Model):
    # Change this to string
    academic_year = models.CharField(max_length=15)
    semester = models.IntegerField()
    field_of_studies = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)


class GridModification(models.Model):
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)


class Timetable(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)


# Add name here!
class CourseGroup(models.Model):
    name = models.CharField(max_length=20)
    number_of_choices = models.IntegerField()


class CourseType(models.TextChoices):
    LECTURE = "Lec", _("Lecture")
    PRACTICALS = "Pra", _("Practicals")
    LABORATORY = "Lab", _("Laboratory")
    PROJECT = "Pro", _("Project")
    SEMINARY = "Sem", _("Seminary")


class WeekType(models.TextChoices):
    EVERY_WEEK = "every", _("Every week")
    ODD_WEEK = "odd", _("Odd week")
    EVEN_WEEK = "even", _("Even week")


class DayOfWeek(models.TextChoices):
    MONDAY = "mon", _("Monday")
    TUESDAY = "tue", _("Tuesday")
    WEDNESDAY = "wed", _("Wednesday")
    THURSDAY = "thu", _("Thursday")
    FRIDAY = "fr", _("Friday")
    SATURDAY = "sat", _("Saturday")
    SUNDAY = "sun", _("Sunday")


class Course(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    ECTS = models.IntegerField()
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=3, choices=CourseType, default=CourseType.LECTURE)


# Create your models here.
class Group(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_type = models.CharField(max_length=5, choices=WeekType, default=WeekType.EVERY_WEEK)
    day_of_week = models.CharField(max_length=3, choices=DayOfWeek, default=DayOfWeek.MONDAY)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    building = models.CharField(max_length=30)
    hall = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.code} on {self.day_of_week} in {self.week_type} from ' \
               f'{self.start_time.strftime("%H:%M")} to {self.end_time.strftime("%H:%M")}'

    @property
    def durance(self):
        return int((self.end_time - self.start_time).total_seconds() / 60.0)

    def __lt__(self, other):
        return self.start_time < other.start_time if self.day == other.day else self.day.value < other.day.value

    def __gt__(self, other):
        return self.start_time > other.start_time if self.day == other.day else self.day.value > other.day.value

    def occurs_even(self):
        return self.week_type == WeekType.EVEN_WEEK or self.week_type == WeekType.EVERY_WEEK

    def occurs_odd(self):
        return self.week_type == WeekType.ODD_WEEK or self.week_type == WeekType.EVERY_WEEK


class Lecturing(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group_code = models.ForeignKey(Group, on_delete=models.CASCADE)


class EnrollmentRecord(models.Model):
    group_code = models.ForeignKey(Group, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)


class Basket(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)


class Preference(models.Model):
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    group_code = models.ForeignKey(Group, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)


class EnrollmentQueue(models.Model):
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)


class EnrollmentPermission(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    queue_id = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    is_permitted = models.BooleanField(default=False)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    is_permitted_earlier = models.BooleanField(default=False)


class QueueModification(models.Model):
    queue_id = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(UniWorker, on_delete=models.CASCADE)
