from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'pharma_dashboard' else False

pharma_dashboard = Navbar(name='pharma_dashboard')

pharma_dashboard.append_item(
    NavbarItem(
        name='patients',
        title='Patients',
        label='patients',
        fa_icon='fa fa-user',
        url_name=settings.DASHBOARD_URL_NAMES[
            'patient_listboard_url'],
        no_url_namespace=no_url_namespace))

pharma_dashboard.append_item(
    NavbarItem(
        name='dispensary',
        title='Dispensary',
        label='dispensary',
        fa_icon='fa-medkit',
        url_name=settings.DASHBOARD_URL_NAMES[
            'dispense_listboard_url'],
        no_url_namespace=no_url_namespace))

pharma_dashboard.append_item(
    NavbarItem(
        name='stock_management',
        title='Stock Management',
        label='Stock Management',
        fa_icon='fa-area-chart',
        url_name=settings.DASHBOARD_URL_NAMES[
            'stock_management_listboard_url'],
        no_url_namespace=no_url_namespace))

pharma_dashboard.append_item(
    NavbarItem(
        name='report',
        title='Stock Report',
        label='report',
        fa_icon='fa-file-excel',
        url_name=settings.DASHBOARD_URL_NAMES[
            'report_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(pharma_dashboard)
