class EmailCreds:
    def __init__(self) -> None:
        self.__mail_id__ = "django.dev.tmsl@gmail.com"
        self.EMAIL_HOST = "smtp.gmail.com"
        self.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        self.PORT = 587

    def get_mail_id(self) -> str:
        return self.__mail_id__
