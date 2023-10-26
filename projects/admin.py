from projects.models import Project
from django.contrib import admin

# Register your models here.
admin.site.register(Project)



#!
from projects.models import Report,ReportComment
admin.site.register(Report)
admin.site.register(ReportComment)
