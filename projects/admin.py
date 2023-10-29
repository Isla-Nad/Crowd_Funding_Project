from projects.models import Project,Donation
from django.contrib import admin
from projects.models import Report,ReportComment,Review

admin.site.site_header = 'crowdfunding'
admin.site.site_title = 'crowdfunding'

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title','user','category','total_target'] 
    list_display_links = ['user','category']
    search_fields = ['title']
    list_filter = ['category','total_target']
    ...

admin.site.register(Project,ProjectAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['user','project','reason'] 
    list_filter = ['project']

admin.site.register(Report,ReportAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['user','reported_user','review','reason'] 
    list_filter = ['review']
    def reported_user(self,obj):
        return obj.review.user

admin.site.register(ReportComment,ReportAdmin)
admin.site.register(Donation)


