from django.contrib import admin
from .models import Application, ApplicationComment, ApplicationReport

admin.site.register(Application)
admin.site.register(ApplicationComment)
admin.site.register(ApplicationReport)
