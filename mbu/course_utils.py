from mbu.models import MeritBadgeUniversity, TimeBlock


def _get_overlapping_sessions(self):
    sessions = _get_sessions()
    overlapping_sessions = set()
    for session1 in sessions:
        for session2 in sessions:
            if session1 != session2:
                if self._sessions_overlap(session1, session2):
                    overlapping_sessions.add((session1.pk, session2.pk))
    return overlapping_sessions


def _get_sessions():
    mbu = MeritBadgeUniversity.objects.filter(current=True)
    sessions = TimeBlock.objects.filter(mbu=mbu)
    return sessions


def check_overlapping_enrollment(user, course_to_enroll):
    enrollments = user.enrollments.all()
    for enrollment in enrollments:
        if do_sessions_overlap(enrollment.session, course_to_enroll.session):
            return True
    return False


def do_sessions_overlap(session1, session2):
    no_overlap = session1.start_time < session2.start_time and session1.end_time <= session2.start_time \
              or session1.start_time >= session2.end_time and session1.end_time > session2.end_time
    return not no_overlap
