from django.contrib import admin

from home.models import Main_Category, Category, Sub_Category, Project, Respond

admin.site.register(Respond)
admin.site.register(Project)
admin.site.register(Sub_Category)
admin.site.register(Category)
admin.site.register(Main_Category)
