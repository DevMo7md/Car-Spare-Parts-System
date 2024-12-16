from django.apps import AppConfig

class CspAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CSP_app'

    def ready(self):
        import CSP_app.signals  # تأكد من وجود ملف signals.py في مجلد التطبيق