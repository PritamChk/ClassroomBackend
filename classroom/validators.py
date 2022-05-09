from django.core.exceptions import ValidationError


def is_no_of_sem_even(value):
    if value % 2 == 0:
        return value
    else:
        raise ValidationError("for a course number of sems have to be even")
