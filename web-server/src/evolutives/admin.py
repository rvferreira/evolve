from django.contrib import admin

# Register your models here.
from .models import Parameter, Code, Author, FitnessFunction

admin.site.register(FitnessFunction)
admin.site.register(Parameter)
admin.site.register(Code)
admin.site.register(Author)