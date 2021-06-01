from django.contrib import admin

from sbs.models.Competitiontype import Competitiontype
from sbs.models.Category import Category
from sbs.models.CompetitionStil import CompetitionStil
from sbs.models.ActivityType import ActivityType
from sbs.models.Competition import Competition
from sbs.models.Success import Success
from sbs.models.Weight import Weight
from sbs.models.JudgeRole import JudgeRole
admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"

admin.site.register(Competitiontype)
admin.site.register(Category)
admin.site.register(CompetitionStil)
admin.site.register(ActivityType)
admin.site.register(Competition)
admin.site.register(Success)
admin.site.register(Weight)
admin.site.register(JudgeRole)
