from django.contrib import admin
from .models import *

class DemoAdmin(admin.ModelAdmin):
    list_display = ('name', 'Contributors', 'url', 'Technologies')

    def Contributors(self, obj):
        return ", ".join([x.__str__() for x in obj.constributors.all()])

    def Technologies(selfself, obj):
        return ", ".join([x.__str__() for x in obj.technologies.all()])

class FileAdmin(admin.ModelAdmin):
    list_display = ('FileName', 'RestrictedTo')
    def FileName(self, obj):
        return obj.file.name

    # def Size(self, obj):
    #     return obj.file.storage.size(obj.file.name)

    def RestrictedTo(self, obj):
        return ", ".join([x.__str__() for x in obj.members_allowed.all()])


admin.site.register(Project, DemoAdmin)
admin.site.register(ProjectStatus)
admin.site.register(DirectoryEntry)
admin.site.register(File, FileAdmin)
admin.site.register(Tag)


