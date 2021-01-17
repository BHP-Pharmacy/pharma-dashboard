from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from .stock_item_model_wrapper import StockItemModelWrapper


class StockItemModelWrapperMixin:

    stock_item_model_wrapper_cls = StockItemModelWrapper

    @property
    def stock_item_model_obj(self):
        """Returns a stock item model instance or None.
        """
        try:
            return self.stock_item_cls.objects.get(
                **self.stock_item_options)
        except ObjectDoesNotExist:
            return None

    @property
    def stock_item(self):
        """Returns a wrapped saved or unsaved stock item.
        """
        model_obj = self.stock_item_model_obj or self.stock_item_cls(
            **self.create_stock_item_options)
        return self.stock_item_model_wrapper_cls(model_obj=model_obj)

    @property
    def stock_item_cls(self):
        return django_apps.get_model('procurement.stockitem')

    @property
    def create_stock_item_options(self):
        """Returns a dictionary of options to create a new
        unpersisted stock item model instance.
        """
        options = dict(
            code=self.code, )
        return options

    @property
    def stock_item_options(self):
        """Returns a dictionary of options to get an existing
        stock item instance.
        """
        options = dict(
            code=self.code, )
        return options
