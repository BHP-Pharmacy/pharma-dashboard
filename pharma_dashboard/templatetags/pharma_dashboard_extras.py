from django import template

register = template.Library()


@register.inclusion_tag('pharma_dashboard/buttons/patient_button.html')
def patient_button(model_wrapper):
    title = ['add  patient.']
    return dict(
        subject_identifier=model_wrapper.object.subject_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('pharma_dashboard/buttons/dispense_button.html')
def dispense_button(model_wrapper):
    title = ['dispense.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        href=model_wrapper.dispense.href,
        title=' '.join(title))
    
@register.inclusion_tag('pharma_dashboard/buttons/refill_button.html')
def refill_button(model_wrapper):
    title = ['refill.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        dispense_model_obj=model_wrapper.dispense_model_obj,
        title=' '.join(title))