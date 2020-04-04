from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from status.forms import *
# Register your models here.
from .models import Priority
from .models import Region
from .models import StatusCategory
from .models import SubService
from .models import SubServiceServices
from .models import TicketLog


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'region_description',)
    search_fields = ['region_name', 'region_description', 'services__service_name']
    list_filter = (('services__subservice__ticket__category_status__status_category_tag', DropdownFilter),
                   ('services__service_name', DropdownFilter),
                   ('services__subservice__sub_service_name', DropdownFilter))
    ordering = ['region_name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_description',)
    search_fields = ['service_name', 'service_description', 'subservice__sub_service_name', 'region__region_name']
    list_filter = (('subservice__ticket__category_status__status_category_tag', DropdownFilter),
                   ('region__region_name', DropdownFilter),
                   ('subservice__sub_service_name', DropdownFilter))
    ordering = ['service_name']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('sub_service_name', 'sub_service_description',)
    search_fields = ['sub_service_name', 'sub_service_description', 'services__service_name',
                     'services__region__region_name']
    list_filter = (('ticket__category_status__status_category_tag', DropdownFilter),
                    ('services__region__region_name', DropdownFilter),
                   ('services', RelatedDropdownFilter))
    ordering = ['sub_service_name']


@admin.register(StatusCategory)
class StatusCategoryAdmin(admin.ModelAdmin):
    list_display = ('status_category_tag', 'status_category_color', 'status_category_color_hex',
                    'status_class_design')
    ordering = ['status_category_tag']


def notify_users(modeladmin, request, queryset):
    queryset.update(notify_action=True)
    # here we should call notify_user creating a query call with the ticket_id


notify_users.short_description = "Notify users about ticket"


def notify_action(obj):
    return obj


notify_action.short_description = 'Name'


class TicketHistoryInline(admin.StackedInline):
    model = TicketLog
    formset = TicketHistoryInlineFormset
    extra = 0
    ordering = ("action_date",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = ('ticket_id', 'sub_service', 'category_status', 'begin', 'end', 'notify_action',)
    # fields = ['business_service', 'service_category', ('begin', 'end'), 'action_description', 'action_notes']

    fieldsets = [
        ('Sub-Service on process', {'fields': ['ticket_id', 'sub_service', 'category_status']}),
        ('Date information', {'fields': ['begin', 'end']}),
        ('Additional Information', {'fields': ['action_description', 'action_notes']}),
        (None, {'fields': ['notify_action']}),
    ]

    inlines = [TicketHistoryInline]

    # readonly_fields = ['notify_action']

    search_fields = ['ticket_id', 'sub_service__sub_service_name', 'category_status__status_category_tag']
    list_filter = (('category_status', RelatedDropdownFilter),
                   ('sub_service__services__region__region_name', DropdownFilter),
                   ('sub_service__services__service_name', DropdownFilter),
                   ('sub_service', RelatedDropdownFilter))
    ordering = ['end']

    actions = [notify_users]

    form = TicketForm

    def save_formset(self, request, form, formset, change):
        if formset.cleaned_data:
            status_category = formset.cleaned_data[-1]['service_status']
            status_category_id = StatusCategory.objects.get(status_category_tag=status_category)
            form.instance.category_status_id = status_category_id.pk
            form.instance.save()
        formset.save()


@admin.register(Subscriber)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']
    ordering = ['name']

    readonly_fields = ['token']

    form = SubscriberForm


@admin.register(SubServiceServices)
class SubServiceServicesAdmin(admin.ModelAdmin):
    list_display = ('service', 'subservice', 'priority',)
    list_filter = (('priority', RelatedDropdownFilter),
                   ('subservice__ticket__category_status__status_category_tag', DropdownFilter),
                   ('service__region__region_name', DropdownFilter),
                   ('service', RelatedDropdownFilter),
                   ('subservice', RelatedDropdownFilter))
    search_fields = ['service', 'subservice', 'priority']
    ordering = ['service']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_tag', 'priority_color', 'priority_color_hex')
    ordering = ['priority_tag']


@admin.register(DomainList)
class DomainListAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'domain_description')
    search_fields = ['domain_name', 'domain_description']
    ordering = ['domain_name']
