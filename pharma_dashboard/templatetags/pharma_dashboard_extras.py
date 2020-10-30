from django import template

register = template.Library()


@register.inclusion_tag('pharma_dashboard/buttons/patient_button.html')
def patient_button(model_wrapper):
    title = ['add  patient.']
    return dict(
        subject_identifier=model_wrapper.object.subject_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
