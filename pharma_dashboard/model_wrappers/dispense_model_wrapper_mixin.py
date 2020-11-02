from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .dispense_model_wrapper import DispenseModelWrapper


class DispenseModelWrapperMixin:

    dispense_model_wrapper_cls = DispenseModelWrapper

    @property
    def dispense_model_obj(self):
        """Returns a dispense model instance or None.
        """
        try:
            return self.dispense_cls.objects.get(
                **self.dispense_options)
        except ObjectDoesNotExist:
            return None

    @property
    def dispense(self):
        """Returns a wrapped saved or unsaved dispense.
        """
        model_obj = self.dispense_cls(**self.create_dispense_options)
        return self.dispense_model_wrapper_cls(model_obj=model_obj)

    @property
    def dispense_cls(self):
        return django_apps.get_model('pharma_subject.dispense')

    @property
    def create_dispense_options(self):
        """Returns a dictionary of options to create a new
        unpersisted dispense model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def dispense_options(self):
        """Returns a dictionary of options to get an existing
        dispense instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
