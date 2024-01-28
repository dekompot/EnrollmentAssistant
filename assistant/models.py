import uuid

from django.db import models
from django.db.models import UniqueConstraint
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

    def __str__(self):
        return f"Student(id={self.id}, name={self.name}, average={self.average})"

    def __repr__(self):
        return self.__str__()


class UniWorker(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"UniWorker(name={self.name})"

    def __repr__(self):
        return self.__str__()


class FieldOfStudies(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"FieldOfStudies(id={self.id}, name={self.name})"

    def __repr__(self):
        return self.__str__()


class Studying(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)

    def __str__(self):
        return f"Studying(student_id={self.student}, field_of_study={self.field_of_study})"

    def __repr__(self):
        return self.__str__()


# siatka zajec
class EnrollmentEdition(models.Model):
    # Change this to string
    id = models.CharField(max_length=30, primary_key=True)
    academic_year = models.CharField(max_length=15)
    semester = models.IntegerField()
    field_of_studies = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)

    def __str__(self):
        return f"EnrollmentEdition(id={self.id}, academic_year={self.academic_year}, semester={self.semester}, field_of_studies={self.field_of_studies})"

    def __repr__(self):
        return self.__str__()


class GridModification(models.Model):
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)

    def __str__(self):
        return f"GridModification(enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


class Timetable(models.Model):
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    UniqueConstraint(fields=['enrollment_edition', 'student'], name='timetable_primary_keys')

    def __str__(self):
        return f"Timetable(id = {self.id}, student_id={self.student}, enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


# Add name here!
class CourseGroup(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"CourseGroup(code={self.code}, name={self.name})"

    def __repr__(self):
        return self.__str__()


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

    @classmethod
    def lt(cls, day1, day2):
        days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return days_of_week.index(day1) < days_of_week.index(day2)

    @classmethod
    def gt(cls, day1, day2):
        days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return days_of_week.index(day1) > days_of_week.index(day2)


class Course(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    ECTS = models.IntegerField()
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, blank=True, null=True)
    course_type = models.CharField(max_length=3, choices=CourseType, default=CourseType.LECTURE)

    def __str__(self):
        return f"Course(code={self.code}, name={self.name}, ECTS={self.ECTS}, course_group={self.course_group}, course_type={self.course_type})"

    def __repr__(self):
        return self.__str__()


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
    available_seats = models.IntegerField(default=16)

    def __str__(self):
        return f'on {self.day_of_week} in {self.week_type} from ' \
               f'{self.start_time.strftime("%H:%M")} to {self.end_time.strftime("%H:%M")}'

    @property
    def durance(self):
        return int((self.end_time - self.start_time).total_seconds() / 60.0)

    def __lt__(self, other):
        return self.start_time < other.start_time if self.day_of_week == other.day_of_week\
            else DayOfWeek.lt(self.day_of_week, other.day_of_week)

    def __gt__(self, other):
        return self.start_time > other.start_time if self.day_of_week == other.day_of_week\
            else DayOfWeek.gt(self.day_of_week, other.day_of_week)

    def occurs_even(self):
        return self.week_type == WeekType.EVEN_WEEK or self.week_type == WeekType.EVERY_WEEK

    def occurs_odd(self):
        return self.week_type == WeekType.ODD_WEEK or self.week_type == WeekType.EVERY_WEEK

    def intervenes_with(self, other):
        return self.start_time < other.end_time and self.end_time > other.start_time



class Lecturing(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lecturing(teacher_id={self.teacher}, group_code={self.group})"

    def __repr__(self):
        return self.__str__()


class EnrollmentRecord(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)



    def __str__(self):
        return f"EnrollmentRecord(group_code={self.group}, timetable={self.timetable})"

    def __repr__(self):
        return self.__str__()

class Basket(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Basket(student_id={self.student})"

    def __repr__(self):
        return self.__str__()

class Preference(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"Preference(basket_id={self.basket}, group_code={self.group}, priority={self.priority})"

    def __repr__(self):
        return self.__str__()

class EnrollmentQueue(models.Model):
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)

    def __str__(self):
        return f"EnrollmentQueue(enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


class EnrollmentPermission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    queue = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    is_permitted_earlier = models.BooleanField(default=False)

    def __str__(self):
        return f"EnrollmentPermission(student_id={self.student}, queue_id={self.queue}, date_from={self.date_from}, date_to={self.date_to}, is_permitted_earlier={self.is_permitted_earlier})"

    def __repr__(self):
        return self.__str__()

    def is_in_date(self, other):
        return self.date_from <= other <= self.date_to


class QueueModification(models.Model):
    queue = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    worker = models.ForeignKey(UniWorker, on_delete=models.CASCADE)

    def __str__(self):
        return f"QueueModification(queue_id={self.queue}, worker_id={self.worker})"

    def __repr__(self):
        return self.__str__()


class Exchange(models.Model):
    enrollment_record_from = models.ForeignKey(EnrollmentRecord, related_name='exchange_from_set',
                                               on_delete=models.CASCADE)
    enrollment_record_to = models.ForeignKey(EnrollmentRecord, related_name='exchange_to_set', on_delete=models.CASCADE, blank=True, null=True)
    succeeded = models.BooleanField(default=False)

    def __str__(self):
        return f"Exchange(enrollment_record_from={self.enrollment_record_from}, enrollment_record_to={self.enrollment_record_to}, succeeded={self.succeeded})"

    def __repr__(self):
        return self.__str__()