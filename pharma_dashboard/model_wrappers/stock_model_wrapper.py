from django.apps import apps as django_apps
from django.conf import settings
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper
from pharma_dashboard.constants import (TABLET, SUPPOSITORY, CAPSULE, SOLUTION,
                                        SYRUP, IV, IM)


class StockModelWrapper(ModelWrapper):

    model = 'pharma_subject.stock'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'stock_management_listboard_url')
    next_url_attrs = ['stock_id']
    querystring_attrs = ['stock_id', ]

    @property
    def dispense_model_cls(self):
        return django_apps.get_model('pharma_subject.dispense')

    @property
    def average_mothly_consumption(self):
        overall_sum = 0
        curr_month = get_utcnow().month
        curr_year = get_utcnow().year
        for num in range(curr_month):
            month = num + 1
            overall_sum += self.total_monthly_dispense(month=month, year=curr_year)
        average = overall_sum/curr_month
        return average

    def total_monthly_dispense(self, month=None, year=None):
        disp_sum = 0

        dispenses = self.dispense_model_cls.objects.filter(
            medication__id=self.object.drug.id,
            prepared_datetime__month=month, prepared_datetime__year=year)

        for dispense in dispenses:
            if dispense.dispense_type in [TABLET, SUPPOSITORY, CAPSULE]:
                disp_sum += self.sum_by_type(dispense, "total_number_of_tablets")
            elif dispense.dispense_type in [IV, IM, SOLUTION, SYRUP]:
                disp_sum += self.sum_by_type(dispense, "total_volume")
        return disp_sum

    def sum_by_type(self, dispense_obj, dispense_field):
        sum_by_type = int(getattr(dispense_obj, dispense_field))
        refills = dispense_obj.dispenserefill_set.all()
        if refills:
            sum_by_type += (sum_by_type * len(refills))
        return sum_by_type
