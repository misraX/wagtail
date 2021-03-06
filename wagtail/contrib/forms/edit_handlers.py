from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from wagtail.admin.edit_handlers import EditHandler


class BaseFormSubmissionsPanel(EditHandler):
    template = "wagtailforms/edit_handlers/form_responses_panel.html"

    def render(self):
        form_page_model = self.model
        form_submissions_model = form_page_model().get_submission_class()
        submissions = form_submissions_model.objects.filter(page=self.instance)
        submission_count = submissions.count()

        if not submission_count:
            return ''

        return mark_safe(render_to_string(self.template, {
            'self': self,
            'submission_count': submission_count,
            'last_submit_time': submissions.order_by('submit_time').last().submit_time,
        }))


class FormSubmissionsPanel:
    def __init__(self, heading=None):
        self.heading = heading

    def bind_to_model(self, model):
        heading = _('{} submissions').format(model.get_verbose_name())
        return type(str('_FormResponsesPanel'), (BaseFormSubmissionsPanel,), {
            'model': model,
            'heading': self.heading or heading,
        })
