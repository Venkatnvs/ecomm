from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(AdminUser)
admin.site.register(CustomerUser)
admin.site.register(StaffUser)
admin.site.register(SellerUser)
admin.site.register(EditorType)