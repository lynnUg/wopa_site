from django.contrib import admin

# Register your models here.
from wopa_submitter.models import Assignment, Reading, Submission

admin.site.register(Assignment)
admin.site.register(Reading)
admin.site.register(Submission)
