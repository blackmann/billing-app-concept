from codecs import register

from django.contrib import admin
from django.template.context_processors import request

# from web.models import City, Client, ClientType, Country, Transmission, Zone


# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('title', 'client_type_name', 'city', )

#     def client_type_name(self, obj):
#         return obj.client_type.title


# @admin.register(Transmission)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('source', 'destination', 'created_on', )
#     exclude = ('created_by', )

#     def get_queryset(self, request):
#         qs = super(TransactionAdmin, self).get_queryset(request)

#         if request.user.is_superuser:
#             return qs

#         return qs.filter(created_by=request.user)


#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         super().save_model(request, obj, form, change)


# admin.site.register((ClientType, City, Country, Zone, ))

from web.models import DestOffice, DestRegion, Region, PostOffice, \
    InOutbound, MailDespatch, Transmission


class AuthoredAdmin(admin.ModelAdmin):
    exclude = ('created_by', )

    def get_queryset(self, request):
        qs = super(TransactionAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(MailDespatch, AuthoredAdmin)
admin.site.register(Transmission, AuthoredAdmin)

admin.site.register((DestOffice, DestRegion, Region, PostOffice,
                     InOutbound,))
