from django.contrib import admin
from job_portal.admin_actions import export_as_csv

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'company', 'email', 'contact_date')
  list_display_links = ('id', 'name')
  search_fields = ('name', 'email', 'company')
  list_per_page = 20

admin.site.register(Contact, ContactAdmin)
admin.site.add_action(export_as_csv, name='export_selected')