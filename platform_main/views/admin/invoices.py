from django.http import HttpResponseRedirect, HttpRequest
from django.views.generic import ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper

from platform_main.models import Invoice
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin


class AdminListInvoices(StaffLoginRequiredMixin, ListView):
    template_name = 'v2/admin/invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all().filter(is_deleted=False).order_by('id')


class AdminInvoiceAccept(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, pk: int):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "notfound", "errors": "invoice not found"}, safe=False, status=404)
            # return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))
        invoice.paid = True
        invoice.save(update_fields=['paid'])
        invoice.user.edit_balance(invoice.amount)
        return JsonResponse({"message": "ok"}, safe=False)
        # return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))

    @staticmethod
    def get(req: HttpRequest, pk: int):
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))


class AdminInvoiceDelete(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, pk: int):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))
        invoice.is_deleted = True
        invoice.save(update_fields=['is_deleted'])
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))

    @staticmethod
    def get(req: HttpRequest, pk: int):
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))


class AdminDownloadInvoice(StaffLoginRequiredMixin, View):
    def get(self, req: HttpRequest, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))
        content = FileWrapper(invoice.generate_pdf())
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=invoice # %s.pdf' % str(pk)
        return response
