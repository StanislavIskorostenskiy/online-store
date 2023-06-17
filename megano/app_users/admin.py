from django.contrib import admin
from app_users.models import UserProfile, Avatar


@admin.register(UserProfile)
class AllFieldsAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


@admin.register(Avatar)
class AllFieldsAvatar(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

