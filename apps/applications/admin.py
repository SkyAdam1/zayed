from django.contrib import admin
from .models import Application, ApplicationComment, ApplicationReport , ApplicationRemark

admin.site.register(Application)
admin.site.register(ApplicationComment)
admin.site.register(ApplicationReport)
admin.site.register(ApplicationRemark)

