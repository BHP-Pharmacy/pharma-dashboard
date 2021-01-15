from django.conf import settings
from edc_model_wrapper import ModelWrapper


class StockModelWrapper(ModelWrapper):

    model = 'pharma_subject.stock'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'stock_listboard_url')
    next_url_attrs = ['stock_id']
    querystring_attrs = ['stock_id', ]

