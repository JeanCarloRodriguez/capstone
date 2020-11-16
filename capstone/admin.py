from django.contrib import admin
from .models import User, Merchandise, AcquisitionCost

# Register your models here.
admin.site.register(User)
admin.site.register(Merchandise)
admin.site.register(AcquisitionCost)