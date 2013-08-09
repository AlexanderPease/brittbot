from django.contrib import admin
from companies.models import Company, Investor, USV_Member, Correspondence, Location, Note, Tag

#class CompanyAdmin(admin.ModelAdmin):
#    fields = ['name', 'investors', 'url', 'angel_id']

admin.site.register(Company)
admin.site.register(Investor)
admin.site.register(USV_Member)
admin.site.register(Correspondence)
admin.site.register(Location)
admin.site.register(Note)
admin.site.register(Tag)


