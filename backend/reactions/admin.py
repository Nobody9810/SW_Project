from django.contrib import admin
from .models import UserReaction

@admin.register(UserReaction)
class UserReactionAdmin(admin.ModelAdmin):
    list_display = ['reaction_type', 'content_type', 'object_id', 'created_at']
    list_filter = ['reaction_type', 'content_type', 'created_at']

    date_hierarchy = 'created_at'