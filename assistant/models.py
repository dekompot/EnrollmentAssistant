import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    """
    Represents a teacher in the system.

    Attributes:
    - name (str): The name of the teacher.
    - title (str): The title of the teacher.

    """

    name = models.CharField(max_length=50)
    title = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} {self.name}"

    def __repr__(self):
        return f"{self.title} {self.name}"


class Student(models.Model):
    """
    Represents a student in the system.

    Attributes:
    - id (str): The unique identifier for the student.
    - name (str): The name of the student.
    - average (float): The average performance of grades of the student.
    """

    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    average = models.FloatField(default=0)

    def __str__(self):
        return f"Student(id={self.id}, name={self.name}, average={self.average})"

    def __repr__(self):
        return self.__str__()


class UniWorker(models.Model):
    """
    Represents a worker in the university.

    Attributes:
    - name (str): The name of the university worker.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"UniWorker(name={self.name})"

    def __repr__(self):
        return self.__str__()


class FieldOfStudies(models.Model):
    """
    Represents a field of study.

    Attributes:
    - id (str): The unique identifier for the field of study.
    - name (str): The name of the field of study.
    """
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"FieldOfStudies(id={self.id}, name={self.name})"

    def __repr__(self):
        return self.__str__()


class Studying(models.Model):
    """
    Represents the relationship between a student and a field of study.

    Attributes:
    - student (Student): The student in the relationship.
    - field_of_study (FieldOfStudies): The field of study in the relationship.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)

    def __str__(self):
        return f"Studying(student_id={self.student}, field_of_study={self.field_of_study})"

    def __repr__(self):
        return self.__str__()


class EnrollmentEdition(models.Model):
    """
    Represents an edition of enrollment. Specific for a given semester and field of study

    Attributes:
    - id (str): The unique identifier for the enrollment edition.
    - academic_year (str): The academic year of the edition.
    - semester (int): The semester of the edition.
    - field_of_studies (FieldOfStudies): The associated field of studies.
    """

    id = models.CharField(max_length=30, primary_key=True)
    academic_year = models.CharField(max_length=15)
    semester = models.IntegerField()
    field_of_studies = models.ForeignKey(FieldOfStudies, on_delete=models.CASCADE)

    def __str__(self):
        return f"EnrollmentEdition(id={self.id}, academic_year={self.academic_year}, semester={self.semester}, field_of_studies={self.field_of_studies})"

    def __repr__(self):
        return self.__str__()


class GridModification(models.Model):
    """
    Represents a modification in the enrollment grid.

    Attributes:
    - enrollment_edition (EnrollmentEdition): The enrollment edition associated with the modification.
    """
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)

    def __str__(self):
        return f"GridModification(enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


class Timetable(models.Model):
    """
    Represents the timetable for a student in a specific enrollment edition.

    Attributes:
    - enrollment_edition (EnrollmentEdition): The enrollment edition associated with the timetable.
    - student (Student): The student for whom the timetable is created.
    """
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    UniqueConstraint(fields=['enrollment_edition', 'student'], name='timetable_primary_keys')

    def __str__(self):
        return f"Timetable(id = {self.id}, student_id={self.student}, enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


# Add name here!
class CourseGroup(models.Model):
    """
    Represents a group of courses.

    Attributes:
    - code (str): The unique code for the course group.
    - name (str): The name of the course group.
    """
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"CourseGroup(code={self.code}, name={self.name})"

    def __repr__(self):
        return self.__str__()


class CourseType(models.TextChoices):
    """
    Enumerates different types of courses.
    """
    LECTURE = "Lec", _("Lecture")
    PRACTICALS = "Pra", _("Practicals")
    LABORATORY = "Lab", _("Laboratory")
    PROJECT = "Pro", _("Project")
    SEMINARY = "Sem", _("Seminary")


class WeekType(models.TextChoices):
    """
    Enumerates different types of weeks for courses.
    """
    EVERY_WEEK = "every", _("Every week")
    ODD_WEEK = "odd", _("Odd week")
    EVEN_WEEK = "even", _("Even week")


class DayOfWeek(models.TextChoices):
    """
    Enumerates different days of the week.
    """
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
    """
    Represents a course.

    Attributes:
    - code (str): The unique code for the course.
    - name (str): The name of the course.
    - ECTS (int): The European Credit Transfer and Accumulation System credits for the course.
    - course_group (CourseGroup): The course group to which the course belongs (optional).
    - course_type (str): The type of the course.
    """
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
    """
    Model representing a group for a specific course within an enrollment edition.

    Attributes:
    - code (str): The unique code identifying the group.
    - enrollment_edition (EnrollmentEdition): The enrollment edition to which the group belongs.
    - course (Course): The course associated with the group.
    - week_type (str): The type of weeks the group occurs (choices: 'every', 'odd', 'even').
    - day_of_week (str): The day of the week on which the group occurs (choices: 'mon', 'tue', ..., 'sun').
    - start_time (datetime): The start time of the group.
    - end_time (datetime): The end time of the group.
    - building (str): The building where the group takes place.
    - hall (str): The hall within the building where the group takes place.
    - available_seats (int): The number of available seats in the group.

    Methods:
    - __str__(): Returns a string representation of the group indicating its day, week type, and time range.
    - durance(): Returns the duration of the group in minutes.
    - __lt__(other): Compares two groups based on their start times and days of the week.
    - __gt__(other): Compares two groups based on their start times and days of the week.
    - occurs_even(): Checks if the group occurs in even weeks.
    - occurs_odd(): Checks if the group occurs in odd weeks.
    - intervenes_with(other): Checks if the group time intervenes with another group's time.
    """

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
        """
        Returns the duration of the group in minutes.

        Usage Example:
        ```
        group = Group.objects.get(pk=1)
        duration = group.durance
        print(duration)
        ```
        Output: 120
        """
        return int((self.end_time - self.start_time).total_seconds() / 60.0)

    def __lt__(self, other):
        """
        Compares two groups based on their start times and days of the week.

        Usage Example:
        ```
        group1 = Group.objects.get(pk=1)
        group2 = Group.objects.get(pk=2)
        result = group1.__lt__(group2)
        print(result)
        ```
        Output: True if group1 starts earlier than group2, considering their days of the week.

        Returns:
        - bool: True if the current group is less than the other group, False otherwise.
        """
        return self.start_time < other.start_time if self.day_of_week == other.day_of_week \
            else DayOfWeek.lt(self.day_of_week, other.day_of_week)

    def __gt__(self, other):
        """
        Compares two groups based on their start times and days of the week.

        Usage Example:
        ```
        group1 = Group.objects.get(pk=1)
        group2 = Group.objects.get(pk=2)
        result = group1.__gt__(group2)
        print(result)
        ```
        Output: True if group1 starts later than group2, considering their days of the week.

        Returns:
        - bool: True if the current group is greater than the other group, False otherwise.
        """
        return self.start_time > other.start_time if self.day_of_week == other.day_of_week \
            else DayOfWeek.gt(self.day_of_week, other.day_of_week)

    def occurs_even(self):
        """
       Checks if the group occurs in even weeks.

       Usage Example:
       ```
       group = Group.objects.get(pk=1)
       result = group.occurs_even()
       print(result)
       ```
       Output: True if the group occurs in even weeks, False otherwise.

       Returns:
       - bool: True if the group occurs in even weeks, False otherwise.
       """
        return self.week_type == WeekType.EVEN_WEEK or self.week_type == WeekType.EVERY_WEEK

    def occurs_odd(self):
        """
        Checks if the group occurs in odd weeks.

        Usage Example:
        ```
        group = Group.objects.get(pk=1)
        result = group.occurs_odd()
        print(result)
        ```
        Output: True if the group occurs in odd weeks, False otherwise.

        Returns:
        - bool: True if the group occurs in odd weeks, False otherwise.
        """
        return self.week_type == WeekType.ODD_WEEK or self.week_type == WeekType.EVERY_WEEK

    def intervenes_with(self, other):
        """
        Checks if the group time intervenes with another group's time.

        Usage Example:
        ```
        group1 = Group.objects.get(pk=1)
        group2 = Group.objects.get(pk=2)
        result = group1.intervenes_with(group2)
        print(result)
        ```
        Output: True if the time of group1 intervenes with the time of group2, False otherwise.

        Returns:
        - bool: True if the time of the current group intervenes with the time of the other group, False otherwise.
        """
        return self.day_of_week == other.day_of_week and self.start_time < other.end_time and self.end_time > other.start_time


class Lecturing(models.Model):
    """
        Model representing a lecturing relationship between a teacher and a group.

        Attributes:
        - teacher (Teacher): The teacher associated with the lecturing relationship.
        - group (Group): The group associated with the lecturing relationship.
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lecturing(teacher_id={self.teacher}, group_code={self.group})"

    def __repr__(self):
        return self.__str__()


class EnrollmentRecord(models.Model):
    """
    Model representing the enrollment record of a student in a group.

    Attributes:
    - group (Group): The group associated with the enrollment record.
    - timetable (Timetable): The timetable associated with the enrollment record.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)

    def __str__(self):
        return f"EnrollmentRecord(group_code={self.group}, timetable={self.timetable})"

    def __repr__(self):
        return self.__str__()


class Basket(models.Model):
    """
    Model representing a basket associated with a student.

    Attributes:
    - student (Student): The student associated with the basket.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Basket(student_id={self.student})"

    def __repr__(self):
        return self.__str__()


class Preference(models.Model):
    """
    Model representing a preference for a group associated with a basket.

    Attributes:
    - basket (Basket): The basket associated with the preference.
    - group (Group): The group associated with the preference.
    - priority (int): The priority of the preference (default is 0). Higher is more preferable
    """
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"Preference(basket_id={self.basket}, group_code={self.group}, priority={self.priority})"

    def __repr__(self):
        return self.__str__()


class EnrollmentQueue(models.Model):
    """
    Model representing an enrollment queue associated with an enrollment edition.

    Attributes:
    - enrollment_edition (EnrollmentEdition): The enrollment edition associated with the queue.
    """
    enrollment_edition = models.ForeignKey(EnrollmentEdition, on_delete=models.CASCADE)

    def __str__(self):
        return f"EnrollmentQueue(enrollment_edition={self.enrollment_edition})"

    def __repr__(self):
        return self.__str__()


class EnrollmentPermission(models.Model):
    """
    Model representing an enrollment permission for a student in a queue.

    Attributes:
    - student (Student): The student associated with the enrollment permission.
    - queue (EnrollmentQueue): The queue associated with the enrollment permission.
    - date_from (datetime): The starting date for the permission.
    - date_to (datetime): The ending date for the permission.
    - is_permitted_earlier (bool): Indicates if the student is permitted earlier (default is False).

    Constraints:
    - UniqueConstraint(fields=['student', 'queue'], name='enrollment_permission_primary_keys'):
      Ensures that the combination of student and queue is unique.

    Methods:
    - is_in_date(other): Checks if a given date is within the range of the permission.

    Note: This class represents the permission granted to a student for enrollment in a specific queue for a defined period.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    queue = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    is_permitted_earlier = models.BooleanField(default=False)

    UniqueConstraint(fields=['student', 'queue'], name='enrollment_permission_primary_keys')

    def __str__(self):
        return f"EnrollmentPermission(student_id={self.student}, queue_id={self.queue}, date_from={self.date_from}, date_to={self.date_to}, is_permitted_earlier={self.is_permitted_earlier})"

    def __repr__(self):
        return self.__str__()

    def is_in_date(self, other):
        return self.date_from <= other <= self.date_to


class QueueModification(models.Model):
    """
    Model representing a modification in an enrollment queue made by a worker.

    Attributes:
    - queue (EnrollmentQueue): The queue associated with the modification.
    - worker (UniWorker): The worker associated with the modification.
    """
    queue = models.ForeignKey(EnrollmentQueue, on_delete=models.CASCADE)
    worker = models.ForeignKey(UniWorker, on_delete=models.CASCADE)

    def __str__(self):
        return f"QueueModification(queue_id={self.queue}, worker_id={self.worker})"

    def __repr__(self):
        return self.__str__()


class Exchange(models.Model):
    """
    Represents an exchange of enrollment records between two students.

    Attributes:
    - enrollment_record_from (EnrollmentRecord): The source enrollment record.
    - enrollment_record_to (EnrollmentRecord): The target enrollment record (optional) - set if exchange was successful.
    - succeeded (bool): Indicates if the exchange was successful.
    """

    enrollment_record_from = models.ForeignKey(EnrollmentRecord, related_name='exchange_from_set',
                                               on_delete=models.CASCADE)
    enrollment_record_to = models.ForeignKey(EnrollmentRecord, related_name='exchange_to_set', on_delete=models.CASCADE,
                                             blank=True, null=True)
    succeeded = models.BooleanField(default=False)

    def __str__(self):
        return f"Exchange(enrollment_record_from={self.enrollment_record_from}, enrollment_record_to={self.enrollment_record_to}, succeeded={self.succeeded})"

    def __repr__(self):
        return self.__str__()
