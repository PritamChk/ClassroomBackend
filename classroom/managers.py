# from django.db import models
# from django.db.models.query import QuerySet
# from .signals import classroom_updated

# # from .models import Classroom


# class ClassroomManager(QuerySet):
#     def update(self, **kwargs):
#         classroom_updated.send_robust(
#             self.__class__, file=kwargs["allowed_teacher_list"]
#         )
#         print("in classroom update")
#         return super().update(**kwargs)
