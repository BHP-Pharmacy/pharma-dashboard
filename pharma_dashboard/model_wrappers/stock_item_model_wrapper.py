from django.conf import settings
from edc_model_wrapper import ModelWrapper


class StockItemModelWrapper(ModelWrapper):

    model = 'pharma_subject.stockitem'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'report_listboard_url')
    next_url_attrs = ['code']
    querystring_attrs = ['code', ]
