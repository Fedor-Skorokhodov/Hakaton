from django.contrib import admin
from .models import User, Meeting, Division, Question, Material, Vote, Topic

admin.site.register(User)
admin.site.register(Meeting)
admin.site.register(Division)
admin.site.register(Question)
admin.site.register(Material)
admin.site.register(Vote)
admin.site.register(Topic)

