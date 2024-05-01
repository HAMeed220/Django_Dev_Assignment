from django.contrib import admin

# Register your models here.
from app.models import *

class CustmizeVendor(admin.ModelAdmin):
    list_display=['name','contact_details','address','email']
    list_display_links=['email']
    list_editable=['name','contact_details','address']
    list_filter=('name','contact_details','address','email')
    list_per_page=3


admin.site.register(Vendor,CustmizeVendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)