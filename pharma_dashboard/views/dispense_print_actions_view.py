from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import ProcessFormView
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_label.job_result import JobResult
from edc_label.printers_mixin import PrintersMixin

from ..prescription_labels import PrescriptionLabels


class DispensePrintActionsView(EdcBaseViewMixin, PrintersMixin,
                               TemplateView, ProcessFormView):

    job_result_cls = JobResult
    template_name = 'pharma_dashboard/subject_record.html'
    prescription_labels_cls = PrescriptionLabels
    success_url = settings.DASHBOARD_URL_NAMES.get('dispense_listboard_url')
    print_selected_button = 'print_selected_labels'
    print_all_button = 'print_all_labels'
    print_prescription = 'print_prescription'
    checkbox_name = 'selected_presciption_names'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        patient_model_cls = django_apps.get_model('pharma_subject.patient')

        if kwargs.get('dispense_pk'):
            self.print_labels_action(dispense_pk=kwargs.get('dispense_pk'))
        try:
            self.patient = patient_model_cls.objects.get(subject_identifier=kwargs['subject_identifier'])
        except patient_model_cls.DoesNotExist:
            pass
        else:
            self.print_labels_action()
            response = HttpResponseRedirect(redirect_to=self.success_url)
        return context

    def print_labels_action(self, dispense_pk=None):
        labels = self.prescription_labels_cls(
            dispense_pk=self.kwargs.get('dispense_pk'),
            user=self.request.user)

        if labels.zpl_data:
            job_id = self.clinic_label_printer.stream_print(
                zpl_data=labels.zpl_data)
            job_result = self.job_result_cls(
                name=labels.label_template_name, copies=1, job_ids=[job_id],
                printer=self.clinic_label_printer)
            messages.success(self.request, job_result.message)
