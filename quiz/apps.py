from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = 'quiz'


class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'

    def ready(self):
        import quiz.signals
