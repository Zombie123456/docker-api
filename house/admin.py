from django.contrib import admin
from house.models import House, BuildNum, Community, ImportLog


admin.site.register(House)
admin.site.register(BuildNum)
admin.site.register(Community)
admin.site.register(ImportLog)
