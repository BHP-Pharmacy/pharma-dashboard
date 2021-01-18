from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DispenseModelWrapper(ModelWrapper):

    model = 'pharma_subject.dispense'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'dispense_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier', ]


    def patient(self):
        patient_cls = django_apps.get_model('pharma_subject.patient')

        try:
            patient_obj = patient_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except patient_cls.DoesNotExist:
            return None
        else:
            return patient_obj

    def latest_refill(self):
        refill_cls = django_apps.get_model('pharma_subject.dispenserefill')

        if self.object:
            refills = refill_cls.objects.filter(dispense=self.object).order_by('-refill_datetime')
            if refills:
                return refills[0].refill_datetime
        return None
