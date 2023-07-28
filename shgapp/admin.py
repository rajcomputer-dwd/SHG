from django.contrib import admin
from .models import BranchDetails
from .models import SocietyDetails
from .models import shgdetails
from .models import shgtransaction

# Register your models here.
admin.site.register(BranchDetails)
admin.site.register(SocietyDetails)
admin.site.register(shgdetails)
admin.site.register(shgtransaction) 