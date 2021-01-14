from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from .labels import PrescriptionLabel
from .constants import CAPSULE, SOLUTION, SUPPOSITORY, SYRUP, TABLET, IM, IV


class PrescriptionLabels:

    label_cls = PrescriptionLabel
    label_template_name = None

    def __init__(self, dispense_pk=None, user=None):
        zpl_datas = []
        dispense = self.get_dispensary(
            dispense_pk=dispense_pk)

        label_name = self.label_name(dispense.dispense_type)

        label = self.label_cls(
            dispense=dispense, user=user,
            label_template_name=label_name)
        zpl_datas.append(label.render_as_zpl_data(copies=1))
        self.zpl_data = b''.join(zpl_datas)

    def get_dispensary(self, dispense_pk=None):

        dispense_model_cls = django_apps.get_model('pharma_subject.dispense')
        try:
            dispense_obj = dispense_model_cls.objects.get(pk=dispense_pk)
        except dispense_model_cls.DoesNotExist:
            pass
        else:
            return dispense_obj

    def label_name(self, name):
        if name == TABLET:
            return 'dispense_label_tablet'
        elif name == SYRUP:
            return 'dispense_label_syrup'
        elif name == IV:
            return 'dispense_label_iv'
        elif name == IM:
            return 'dispense_label_iv'
        elif name == SUPPOSITORY:
            return 'dispense_label_suppository'
        elif name == SOLUTION:
            return 'dispense_label_syrup'
        elif name == CAPSULE:
            return 'dispense_label_capsule'

