# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django import template

from crispy_forms.helper import FormHelper

uni_formset_template = get_template('uni_form/uni_formset.html')
uni_form_template = get_template('uni_form/uni_form.html')

register = template.Library()

@register.filter(name='as_uni_form')
@register.filter(name='crispy')
def as_crispy_form(form):
    """ 
    The original and still very useful way to generate a div elegant form/formset::
    
        {% load crispy_forms_tags %}

        <form class="uniForm" action="post">
            {% csrf_token %}
            {{ myform|crispy }}
        </form>
    """
    if isinstance(form, BaseFormSet):
        if settings.DEBUG:
            template = get_template('uni_form/uni_formset.html')
        else:
            template = uni_formset_template
        c = Context({'formset': form})
    else:
        if settings.DEBUG:
            template = get_template('uni_form/uni_form.html')
        else:
            template = uni_form_template
        c = Context({'form': form})
    return template.render(c)

@register.filter(name='as_uni_errors')
@register.filter(name='as_crispy_errors')
def as_crispy_errors(form):
    """
    Renders only form errors the same way as django-crispy-forms::

        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}
    """
    if isinstance(form, BaseFormSet):
        template = get_template('uni_form/errors_formset.html')
        c = Context({'formset': form})
    else:
        template = get_template('uni_form/errors.html')
        c = Context({'form':form})
    return template.render(c)

@register.filter(name='as_uni_field')
@register.filter(name='as_crispy_field')
def as_crispy_field(field):
    """
    Renders a form field like a django-crispy-forms field::

        {% load crispy_forms_tags %}
        {{ form.field|as_crispy_field }}
    """
    template = get_template('uni_form/field.html')
    c = Context({'field':field})
    return template.render(c)
