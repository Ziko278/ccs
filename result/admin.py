from django.contrib import admin
from result.models import *


class ResultAdmin(admin.ModelAdmin):
    search_fields = ['student__surname', 'student__last_name']


admin.site.register(ResultSettingModel)
admin.site.register(MidResultGradeModel)
admin.site.register(ResultModel, ResultAdmin)
admin.site.register(TextBasedResultModel)
admin.site.register(ResultBehaviourComputeModel)
admin.site.register(TextResultCategoryModel)
admin.site.register(TextResultModel)
