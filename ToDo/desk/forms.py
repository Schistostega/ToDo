from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, Submit, Row, HTML

from .models import Project, Task

CONTAINER_CSS_CLASS = 'm-auto w-50 border rounded text-center p-3 text-white'
FIELDSET_CSS_CLASS = 'form-group'
FIELD_CSS_CLASS = 'bg-dark text-white border-light text-left'
BUTTON_CSS_CLASS = 'btn btn-dark border-light'
ROW_BUTTON_HOLDER = 'w-50 m-auto d-flex justify-content-around'
ROW_JUSTIFY_CONTENT_AROUND = 'd-flex justify-content-around'
CANCEL_HYPERLINK_HTML = "<a class='btn btn-dark' href='{% url 'desk:project_list' %}'>Cancel</a>"


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Arguments: button_label, form_legend are obtained from views across a get_form_kwargs function.
        """
        self.button_label = kwargs.pop('button_label')
        self.form_legend = kwargs.pop('form_legend')
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    self.form_legend,  # 1th arg -- form legend
                    Field('name', css_class=FIELD_CSS_CLASS, autocomplete='off'),
                    css_class=FIELDSET_CSS_CLASS
                ),
                Row(
                    Submit('submit', self.button_label, css_class=BUTTON_CSS_CLASS),
                    HTML(CANCEL_HYPERLINK_HTML),
                    css_class=ROW_BUTTON_HOLDER
                ),
                css_class=CONTAINER_CSS_CLASS
            )
        )

    class Meta:
        model = Project
        fields = ('name', )


class TaskForm(forms.ModelForm):
    """
    Arguments: button_label, form_legend, user(current user) are obtained from views across a get_form_kwargs function.
    """
    def __init__(self, *args, **kwargs):
        self.button_label = kwargs.pop('button_label')
        self.form_legend = kwargs.pop('form_legend')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=self.user)
        self.fields['date_created'] = forms.DateTimeField(initial=timezone.now)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    self.form_legend,  # 1th arg -- form legend
                    Field('title', css_class=FIELD_CSS_CLASS, autocomplete='off'),
                    Field('description', css_class=FIELD_CSS_CLASS, autocomplete='off'),
                    Row(
                        Field('date_created', css_class=FIELD_CSS_CLASS),
                        Field('deadline', css_class=FIELD_CSS_CLASS),
                        css_class=ROW_JUSTIFY_CONTENT_AROUND
                    ),
                    Field('project', css_class=FIELD_CSS_CLASS),
                    css_class=FIELDSET_CSS_CLASS
                ),
                Row(
                    Submit('submit', self.button_label, css_class=BUTTON_CSS_CLASS),
                    HTML(CANCEL_HYPERLINK_HTML),
                    css_class=ROW_BUTTON_HOLDER
                ),
                css_class=CONTAINER_CSS_CLASS
            )
        )

    class Meta:
        model = Task
        fields = ('title', 'description', 'date_created', 'deadline', 'project')
