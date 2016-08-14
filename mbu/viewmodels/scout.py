from django.core.exceptions import ObjectDoesNotExist
from mbu.models import TimeBlock
from mbu.models import ScoutCourseInstance, Course

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
                start_time = enrollment.timeblock.start_time.strftime('%I:%M %p')
                end_time = enrollment.timeblock.end_time.strftime('%I:%M %p')
                enr = Enrollment(start_time, end_time, enrollment.course)
                result.append(enr)
            except ObjectDoesNotExist:
                start_time = block.start_time.strftime('%I:%M %p')
                end_time = block.end_time.strftime('%I:%M %p')
                course = Course()
                course.name = ''
                emptyinstance = Enrollment(start_time, end_time, course)
                result.append(emptyinstance)

        return result


class Enrollment:
    def __init__(self, start_time, end_time, course):
        self.start_time = start_time
        self.end_time = end_time
        self.course = course
