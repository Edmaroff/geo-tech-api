from django.contrib import admin

from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = (
        "ne",
        "address",
        "latitude",
        "longitude",
        "status",
        "gsm",
        "umts",
        "lte",
    )
    list_filter = ("status", "gsm", "umts", "lte")
    search_fields = ("ne", "address")
    ordering = ("ne",)
    list_per_page = 20  # Пагинация в админке
