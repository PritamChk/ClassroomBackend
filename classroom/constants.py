from django.db import models as m


class LEVEL_CHOICES(m.TextChoices):
    UnderGraduate = "Bachelors"
    PostGraduate = "Masters"


class SECTION_CHOICES(m.TextChoices):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
