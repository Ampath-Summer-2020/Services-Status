from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import SubService, Ticket, StatusCategory,Service,TicketLog,SubServiceServices,Region
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .forms import SubscriberForm
from itertools import chain

# Create your views here.

#Services Status Visualization page
class ServicesStatusView(View):
    template_name = "status/services_status.html"
    def get(self, request, *args, **kwargs):

        # Getting most recent 5 tickets
        queryset = Ticket.objects.all().order_by('begin').reverse()[:5]

        context = {
            "ticket_list": queryset,
            "active_nav": 1
        }

        # Getting list of regions
        queryset = Region.objects.all()
        context['regions'] = queryset

        # Getting list of services
        services = []
        for region in queryset:
            services = list(dict.fromkeys(chain(services, region.services.all())))

        context['services_list'] = services

        # Getting list of status for legend
        queryset = StatusCategory.objects.all()
        context['category_list'] = queryset

        # Getting today's date
        today = datetime.now()
        list_of_five_days = [today]

        counter = 1
        while counter < 5:
            list_of_five_days.append(today-timedelta(days=counter))
            counter = counter+1


        context['days'] = list_of_five_days

        return render(request, self.template_name, context)

#Subscription page
class SubscriptionView(View):
    template_name = "status/subscription.html"

    def get(self, request, *args, **kwargs):
        context = {
            "active_nav": 2
        }

        form = SubscriberForm()
        context = {"form": form}

        # queryset = View.objects.all()
        context['region_list'] = {"Region1", "Region2"}

        queryset = Service.objects.all()
        context['services_list'] = queryset

        context['subscribed'] = False

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            form.save()
            context['subscribed'] = True
        return render(request, self.template_name, context)


#Services Status History Visualization page
class ServiceHistoryView(View):
    template_name = "status/ss_history_visualization.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {
            "active_nav": 1
        }
        if id is not None:
            obj = get_object_or_404(Service, id=id)
            context['object'] = obj

            #Getting all tickets affecting this service
            sub_service_service = SubServiceServices.objects.filter(service=obj)

            #Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for row in sub_service_service:
                queryset = Ticket.objects.filter(sub_service=row.subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            context['tickets_list'] = tickets_list


        return render(request, self.template_name, context)

#Services Status History Details page
class ServiceHistoryDetailsView(ListView):
    template_name = "status/sh_details.html"

    def get(self, request, id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        if id is not None:
            #Getting ticket instance
            obj = get_object_or_404(Ticket, id=id)
            context['object'] = obj

            #Getting list of ticket logs associated with this ticket
            queryset = TicketLog.objects.filter(service_history=obj)
            context['ticket_logs'] = queryset

            #Getting list of tickets associated with the service
            service_tickets = Ticket.objects.filter(sub_service=obj.sub_service).order_by('begin')

            #Pagination
            paginator = Paginator(service_tickets, 1)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj

        return render(request, self.template_name, context)