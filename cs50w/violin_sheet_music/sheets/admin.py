from django.contrib import admin

from sheets.models import Attempt, Sheet, User

# Register your models here.
admin.site.register(Sheet)
admin.site.register(Attempt)
admin.site.register(User)
