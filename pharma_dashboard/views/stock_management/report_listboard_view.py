import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import StockModelWrapper


class ReportListboardView(NavbarViewMixin, EdcBaseViewMixin,
                          ListboardFilterViewMixin, SearchFormViewMixin,
                          ListboardView):

    listboard_template = 'report_listboard_template'
    listboard_url = 'report_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = 'fa-area-chart'

    model = 'pharma_subject.stock'
    model_wrapper_cls = StockModelWrapper
    navbar_name = 'pharma_dashboard'
    navbar_selected_item = 'report'
    search_form_url = 'report_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            stock_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'code': kwargs.get('code')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
