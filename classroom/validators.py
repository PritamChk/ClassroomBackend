from datetime import date
from django.core.exceptions import ValidationError


def is_no_of_sem_even(value):
    if value % 2 == 0:
        return value
    else:
        raise ValidationError("for a course number of sems have to be even")


def pdf_file_size_lt_5mb(value):
    limit_no = 5
    limit = limit_no * 1024 * 1024
    if value.size > limit:
        raise ValidationError(f"File too large. Size should not exceed {limit_no} Mb.")


def assignment_date_gte_today(date_val: date):
    if date_val < date.today():
        raise ValidationError(
            f"Assignment due date- [{date_val:%d-%m-%Y}] can not be less than current date - {(date.today()):%d-%m-%Y}"
        )
    return date_val
