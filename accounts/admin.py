from django.contrib import admin

from sbs.models.Competitiontype import Competitiontype
from sbs.models.Category import Category
from sbs.models.CompetitionStil import CompetitionStil

admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"

admin.site.register(Competitiontype)
admin.site.register(Category)
admin.site.register(CompetitionStil)
