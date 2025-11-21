from django.contrib import admin
from .models import SatisfactionSurvey, Pin, Survey1, Survey2, Survey3


@admin.register(SatisfactionSurvey)
class SatisfactionSurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "clientType", "government", "visitDate", "sex", "age", "region", "submitted_at")
    search_fields = ("clientType", "government", "region", "officePerson", "serviceAvailed")
    list_filter = ("clientType", "government", "sex", "region", "visitDate")
    ordering = ("-submitted_at",)


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ("id", "code")
    search_fields = ("code",)
    ordering = ("id",)


@admin.register(Survey1)
class Survey1Admin(admin.ModelAdmin):
    list_display = ("intro_title", "transaction_type", "submit_text")
    search_fields = ("intro_title", "transaction_type")


@admin.register(Survey2)
class Survey2Admin(admin.ModelAdmin):
    list_display = ("id", "cc1_code", "cc2_code", "cc3_code")
    search_fields = ("cc1_question", "cc2_question", "cc3_question")


@admin.register(Survey3)
class Survey3Admin(admin.ModelAdmin):
    list_display = ("id", "instruction")