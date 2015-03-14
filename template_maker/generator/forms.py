from wtforms import widgets, DateField

class DatePickerWidget(widgets.TextInput):
    '''
    TextInput widget that adds a 'datepicker' class to the html input
    element; this makes it easy to write a jQuery selector that adds a
    UI widget for date picking.
    '''
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'datepicker %s' % c
        return super(DatePickerWidget, self).__call__(field, **kwargs)

class DatePickerField(DateField):
    widget = DatePickerWidget()
