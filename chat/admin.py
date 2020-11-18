from django.contrib import admin
from chat.models import *



class MessageInline(admin.StackedInline):
    model = Message
    extra = 0


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [MessageInline]


# Register your models here.
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Participant, ParticipantAdmin)

