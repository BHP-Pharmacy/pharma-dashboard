from django.apps import apps as django_apps
from arrow.arrow import Arrow
from django.apps import apps as django_apps
from django.conf import settings
from edc_label import Label
from pharma_subject.constants import TABLET, SYRUP, IM, IV, SUPPOSITORY, SOLUTION, CAPSULE


class PrescriptionLabel(Label):

    registered_subject_model = 'edc_registration.registeredsubject'
    label_template_name = None

    def __init__(self, dispense=None, item=None, user=None, label_template_name=None):
        self._registered_subject = None
        self.label_template_name = label_template_name or self.label_template_name
        super().__init__(label_template_name=self.label_template_name)
        self.item = item or 1
        self.dispense = dispense
        self.user = user
        self.label_name = self.dispense.subject_identifier


    @property
    def label_context(self):
        patient_cls = django_apps.get_model('pharma_subject.patient')
        profile_cls = django_apps.get_model('pharma_subject.profile')
        try:
            patient = patient_cls.objects.get(subject_identifier=self.dispense.subject_identifier)
        except patient_cls.DoesNotExist:
            label_context = {}
        else:
            label_context = {
                'telephone_number': patient.patient_site.telephone_number,
                'patient': patient.subject_identifier,
                'initials': patient.initials,
                'site':patient.patient_site.site_code,
                'sid':patient.patient_site.site_code,
                'concentration':self.dispense.concentration,
                'times_per_day': self.dispense.times_per_day,
                'drug_name': self.dispense.medication,
                'type': self.dispense.dispense_type.lower() + 's',
                'prepared_datetime': self.dispense.prepared_datetime.strftime("%d-%m-%y %H:%M"),
                'prepared_by': profile_cls.objects.get(user__username=self.user.username).initials,
                'storage_instructions': self.dispense.medication.storage_instructions,
                'protocol': self.dispense.medication.protocol,
                'weight': self.dispense.weight,
            }
            if self.dispense.dispense_type in [TABLET, CAPSULE, SUPPOSITORY]:
                label_context.update({
                    'number_of_tablets': self.dispense.number_of_tablets,
                    'total_number_of_tablets': self.dispense.total_number_of_tablets,
                })
            elif self.dispense.dispense_type in [SYRUP, SOLUTION]:
                label_context.update({
                    'number_of_teaspoons': self.dispense.dose,
                    'concentration': self.dispense.concentration,
                    'total_volume': self.dispense.total_volume,
                })
                if self.dispense.medication.protocol.name == 'Tatelo':
                    label_context.update({
                        'step': self.dispense.step
                    })
                elif self.dispense.medication.protocol.name == 'HPTN 084':
                    label_context.update({
                        'BMI': self.dispense.bmi,
                        'needle_size': self.dispense.bmi
                    })
            elif self.dispense.dispense_type in [IV, IM]:
                label_context.update({
                    'concentration': self.dispense.concentration,
                    'total_volume': self.dispense.total_volume,
                    'infusion': self.dispense.infusion_number,
                })
                if self.dispense.dispense_type == IV:
                    label_context.update({
                        'usage': 'Infuse (IV)intravenously'
                    })
                else:
                    label_context.update({
                        'usage': 'Inject intramuscularly(IM)'
                    })
        return label_context
