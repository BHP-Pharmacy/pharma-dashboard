from django.conf import settings
from django.urls.conf import path, include, re_path
from edc_dashboard import UrlConfig

from .views import ListboardView, DispensaryListboardView, DispensePrintActionsView
from .views import ReportListboardView, StockListboardView
from .patterns import subject_identifier

app_name = 'pharma_dashboard'

patient_listboard_url_config = UrlConfig(
    url_name='patient_listboard_url',
    view_class=ListboardView,
    label='patient_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=None)

dispense_listboard_url_config = UrlConfig(
    url_name='dispense_listboard_url',
    view_class=DispensaryListboardView,
    label='dispense_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

stock_listboard_url_config = UrlConfig(
    url_name='stock_management_listboard_url',
    view_class=StockListboardView,
    label='stock_management_listboard',
    identifier_label='stock_id',
    identifier_pattern='')

report_listboard_url_config = UrlConfig(
    url_name='report_listboard_url',
    view_class=ReportListboardView,
    label='report_listboard',
    identifier_label='code',
    identifier_pattern='')


urlpatterns = [path(r'dispense_print/(?P<subject_identifier>[-\w]+)/(?P<dispense_pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
         DispensePrintActionsView.as_view(),
         name='print_url'), ]
urlpatterns += patient_listboard_url_config.listboard_urls
urlpatterns += dispense_listboard_url_config.listboard_urls
urlpatterns += stock_listboard_url_config.listboard_urls
urlpatterns += report_listboard_url_config.listboard_urls

if settings.APP_NAME == 'pharma_dashboard':

    from django.views.generic.base import RedirectView

    urlpatterns += [
        path('accounts/', include('edc_base.auth.urls')),
        path('edc_data_manager/', include('edc_data_manager.urls')),
        path('edc_device/', include('edc_device.urls')),
        path('edc_protocol/', include('edc_protocol.urls')),
        path('admininistration/', RedirectView.as_view(url='admin/'),
             name='administration_url'),
        path(r'', RedirectView.as_view(url='admin/'), name='home_url')]
