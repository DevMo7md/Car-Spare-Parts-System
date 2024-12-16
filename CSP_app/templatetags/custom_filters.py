from django import template
from babel.dates import format_datetime

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def date_in_arabic(value, format='full'):
    """
    تحويل التاريخ إلى اللغة العربية.
    :param value: كائن datetime
    :param format: تنسيق التاريخ ('full', 'long', 'medium', 'short')
    :return: تاريخ باللغة العربية
    """
    try:
        return format_datetime(value, format=format, locale='ar')
    except Exception as e:
        return value  # إذا حدث خطأ، يتم إرجاع القيمة الأصلية
