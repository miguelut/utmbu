from django.core.exceptions import ObjectDoesNotExist
from mbu.models import TimeBlock
from mbu.models import ScoutCourseInstance, Course
from pprint import PrettyPrinter
__author__ = 'michael'


class Schedule:

    def __init__(self, scout):
        self.scout = scout
        self.enrollments = self.get_enrollments()

    def get_enrollments(self):
        result = []
        timeblocks = TimeBlock.objects.all()
        for block in timeblocks:
            try:
                enrollment = self.scout.enrollments.get(timeblock=block)
                result.append(enrollment)
            except ObjectDoesNotExist:
                emptyinstance = ScoutCourseInstance()
                emptyinstance.timeblock = block
                emptyinstance.course = Course()
                emptyinstance.course.name = "Empty"
                result.append(emptyinstance)

        return result
