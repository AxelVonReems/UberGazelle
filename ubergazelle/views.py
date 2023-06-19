from flask_admin.contrib.sqla import ModelView
from wtforms import SelectMultipleField, validators

from regions import REGIONS


class MultipleSelect(SelectMultipleField):

    def pre_validate(self, form):
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class DriversAdmin(ModelView):
    form_columns = ('driver_telegram_id', 'work_regions', 'vehicle_type')
    column_labels = {
        'driver_telegram_id': 'Driver Telegram ID',
        'work_regions': 'Work Regions',
        'vehicle_type': 'Vehicle Type'
        }
    form_extra_fields = {
        'work_regions': MultipleSelect(
            'Work Regions', [validators.DataRequired()], choices=REGIONS,
            render_kw={"multiple": "multiple"}, coerce=int
            )
            }
