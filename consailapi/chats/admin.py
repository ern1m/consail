from django.contrib import admin

from consailapi.chats.models import Message, Thread


class MessageInline(admin.TabularInline):
    readonly_fields = ("uuid",)
    model = Message
    extra = 0


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = (MessageInline,)
