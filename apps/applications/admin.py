from django.contrib import admin

from .models import (Application, ApplicationComment, ApplicationRemark,
                     ApplicationReport, DesignatedExpert)

admin.site.register(Application)
admin.site.register(ApplicationComment)
admin.site.register(ApplicationReport)
admin.site.register(ApplicationRemark)
admin.site.register(DesignatedExpert)
