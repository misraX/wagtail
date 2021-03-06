from django.template.loader import render_to_string

from wagtail.admin.compare import ForeignObjectComparison
from wagtail.admin.edit_handlers import BaseChooserPanel

from .widgets import AdminImageChooser


class BaseImageChooserPanel(BaseChooserPanel):
    object_type_name = "image"

    @classmethod
    def widget_overrides(cls):
        return {cls.field_name: AdminImageChooser}

    @classmethod
    def get_comparison_class(cls):
        return ImageFieldComparison


class ImageChooserPanel:
    def __init__(self, field_name):
        self.field_name = field_name

    def bind_to_model(self, model):
        return type(str('_ImageChooserPanel'), (BaseImageChooserPanel,), {
            'model': model,
            'field_name': self.field_name,
        })


class ImageFieldComparison(ForeignObjectComparison):
    def htmldiff(self):
        image_a, image_b = self.get_objects()

        return render_to_string("wagtailimages/widgets/compare.html", {
            'image_a': image_a,
            'image_b': image_b,
        })
