from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .dispense_model_wrapper_mixin import DispenseModelWrapperMixin

class PatientModelWrapper(DispenseModelWrapperMixin, ModelWrapper):

    model = 'pharma_subject.patient'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'patient_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier', ]

