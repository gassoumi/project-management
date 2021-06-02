from django.contrib import admin

from .models import Project, Task, Sprint, Discussion, \
    Comment, Document, Video, UserProject, Note, Problem


# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    # fields = ['objective', 'designation', 'created_at']
    list_display = ['id', 'code', 'designation', 'objective', 'created_at']


class ProjectUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'project',
                    'classification', 'is_scrum_master']


class SprintAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'project', 'desired_at', 'status']


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'note', 'user', 'date', 'ok', 'comment']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'start_at',
                    'end_at', 'sprint', 'user', 'status']


class ProblemAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'start_at', 'end_at',
                    'task', 'resolutionTools', 'cause', 'status']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'version', 'task', 'created_at', 'status',
                    'get_doc_file_name', 'get_doc_file_path']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Discussion)
admin.site.register(Comment)
#admin.site.register(Document, DocumentAdmin)
admin.site.register(Video)
admin.site.register(UserProject, ProjectUsersAdmin)
