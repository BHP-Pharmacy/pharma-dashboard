from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DispenseModelWrapper(ModelWrapper):

    model = 'pharma_subject.dispense'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'patient_listboard_url')
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