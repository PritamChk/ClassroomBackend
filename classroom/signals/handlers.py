from .classroom_handlers import (
    create_allowed_students,
    create_allowed_teacher_for_classroom_level,
    create_allowed_teacher_for_classroom_level_with_check,
    create_sems_for_new_classroom,
)
from .college_handlers import (
    create_allowed_teacher,
    remove_teacher_profile_after_allowed_teacher_deletion,
    send_mail_after_create_allowed_teacher,
)
from .dba_handlers import create_allowed_dba
from .profile_handlers import create_profile
from .teacher_classroom_handlers import (
    assign_classroom_to_existing_teacher,
    auto_join_teacher_to_classes,
    remove_class_after_removal_of_assigned_teacher,
)
from .user_handlers import (
    delete_user_on_dba_delete,
    delete_user_on_student_delete,
    delete_user_on_teacher_delete,  # FIXME: not working
)
