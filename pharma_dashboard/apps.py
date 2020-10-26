from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'pharma_dashboard'
    admin_site_name = 'pharma_subject_admin'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Pharmacy Subject Dashboard'
    institution = 'Botswana Harvard'
    disclaimer = 'BHP Pharmacy'
