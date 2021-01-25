from django.contrib import admin
from sbs.models.Athlete import Athlete
from sbs.models.DirectoryMember import DirectoryMember
from sbs.models.SportClubUser import SportClubUser
from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.Person import Person

admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"

admin.site.register(Athlete)
admin.site.register(DirectoryMember)
admin.site.register(SportClubUser)
admin.site.register(Coach)
admin.site.register(Judge)
admin.site.register(Person)