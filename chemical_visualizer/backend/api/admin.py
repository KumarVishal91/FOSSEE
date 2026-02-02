from django.contrib import admin

from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "uploaded_at", "row_count")
	search_fields = ("name",)
	ordering = ("-uploaded_at",)
